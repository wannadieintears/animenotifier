import aiohttp
from keyboards import keyboards
import settings
from aiogram.types import Message
from aiogram import F, Router
import asyncpg
from aiogram.fsm.context import FSMContext
from utils.states import Add_next_message, Delete_next_message
from bs4 import BeautifulSoup as bs
import asyncio
from main import bot

router = Router()

@router.message(F.text.lower() == "/start")
async def start(message: Message):
    await message.answer("I'm bot for notifications of then ew anime episodes on gogoanimes.to!",
                         reply_markup=keyboards.kb)


@router.message(F.text.lower() == "add a title")
async def get_add_title(message: Message, state: FSMContext):
    await state.set_state(Add_next_message.mes)
    await message.answer("Tell me what a title do you wanna add? Please, write in the exact way"
                         " how the title is written on the site!")


@router.message(Add_next_message.mes)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(mes=message.text)
    await state.clear()

    connect = await asyncpg.connect(
        host=settings.host,
        port=settings.port,
        user=settings.user,
        password=settings.password,
        database=settings.database
    )

    replaced = message.text.replace("'", "")
    query1 = f"INSERT INTO titles (user_id, title) VALUES ({message.from_user.id}, '{replaced}')"
    query2 = f"SELECT * FROM titles WHERE user_id = {message.from_user.id};"
    query3 = f"INSERT INTO titles (user_id, title, notification) VALUES" \
             f" ({message.from_user.id}, '{message.text}', 1);"

    async with connect.transaction():
        notification = await connect.fetch(query2)
        if 'notification' in notification:
            notification = notification[0]['notification']
            if notification == 1:
                await connect.execute(query3)
            else:
                await connect.execute(query1)
        else:
            await connect.execute(query1)
        await message.answer(f"{replaced} is successfully added!", reply_markup=keyboards.kb)
    await connect.close()


@router.message(F.text.lower() == "delete a title")
async def get_delete_title(message: Message, state: FSMContext):
    await state.set_state(Delete_next_message.mes)
    await message.answer("Tell me what a title do you wanna delete? Please, write in the exact way"
                         " how the title is written in database!")


@router.message(Delete_next_message.mes)
async def delete_title(message: Message, state: FSMContext):
    await state.update_data(mes=message.text)
    await state.clear()

    connect = await asyncpg.connect(
        host=settings.host,
        port=settings.port,
        user=settings.user,
        password=settings.password,
        database=settings.database
    )

    query = f"DELETE FROM titles WHERE user_id = {message.from_user.id} AND title = '{message.text}';"

    async with connect.transaction():
        await connect.execute(query)
        await message.answer(f"{message.text} is successfully deleted", reply_markup=keyboards.kb)
    await connect.close()


@router.message(F.text.lower() == "show titles")
async def show(message: Message):
    connect = await asyncpg.connect(
        host=settings.host,
        port=settings.port,
        user=settings.user,
        password=settings.password,
        database=settings.database
    )

    query = f"SELECT * FROM titles WHERE user_id = {message.from_user.id};"

    async with connect.transaction():
        titles = await connect.fetch(query)
        titles = '\n'.join([title['title'] for title in titles])
        await message.answer(f"Your titles:\n{titles}", reply_markup=keyboards.kb)
    await connect.close()


@router.message(F.text.lower() == "on")
async def set_on(message: Message):
    connect = await asyncpg.connect(
        host=settings.host,
        port=settings.port,
        user=settings.user,
        password=settings.password,
        database=settings.database
    )

    query = f"UPDATE titles SET notification = 1 WHERE user_id = {message.from_user.id};"

    async with connect.transaction():
        await connect.execute(query)
        await message.answer("Notifications are successfully turned on!", reply_markup=keyboards.kb)
    await connect.close()


@router.message(F.text.lower() == "off")
async def set_on(message: Message):
    connect = await asyncpg.connect(
        host=settings.host,
        port=settings.port,
        user=settings.user,
        password=settings.password,
        database=settings.database
    )

    query = f"UPDATE titles SET notification = 0 WHERE user_id = {message.from_user.id};"

    async with connect.transaction():
        await connect.execute(query)
        await message.answer("Notifications are successfully turned off!", reply_markup=keyboards.kb)
    await connect.close()


@router.message(F.text.lower() == "parse")
async def parse(message: Message):
    url = "https://gogoanimes.to"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = bs(html, "html.parser")
            title = soup.find('p', class_="name").text
            episode = soup.find('p', class_="episode").text

    connect = await asyncpg.connect(
        host=settings.host,
        port=settings.port,
        user=settings.user,
        password=settings.password,
        database=settings.database
    )

    replaced = title.replace("'", "")
    query1 = f"SELECT * FROM last WHERE id = 1;"
    query2 = f"SELECT * FROM titles WHERE title = '{replaced}' AND notification = 1;"
    query3 = f"UPDATE last SET last = '{replaced}' WHERE id = 1;"

    async with connect.transaction():
        last = await connect.fetch(query1)
        last = last[0]['last']
        users = await connect.fetch(query2)
        users = [user['user_id'] for user in users]

        if replaced != last:
            for user in users:
                await bot.send_message(user, f"{episode} of {replaced} is out!", reply_markup=keyboards.kb)
            await connect.execute(query3)

    await connect.close()
    await asyncio.sleep(5)
    await parse(message)


@router.message()
async def what(message: Message):
    await message.answer("I didn't understand you :3")