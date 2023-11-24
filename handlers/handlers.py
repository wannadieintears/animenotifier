import aiohttp
from keyboards import keyboards
import settings
from aiogram.types import Message
from aiogram import F, Router
import asyncpg
from aiogram.fsm.context import FSMContext
from utils.states import Add_next_message, Delete_next_message

router = Router()

@router.message(F.text.lower() == "/start")
async def start(message: Message):
    await message.answer("I'm bot for notifications of then ew anime episodes on gogoanimehd.io!",
                         reply_markup=keyboards.kb)


@router.message(F.text.lower() == "add a title")
async def get_add_title(message: Message, state: FSMContext):
    await state.set_state(Add_next_message.mes)
    await message.answer("Tell me what a title do you wanna add?")


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

    query = f"INSERT INTO titles (user_id, title) VALUES ({message.from_user.id}, '{message.text}');"
    async with connect.transaction():
        await connect.execute(query)
        await message.answer(f"{message.text} is successfully added", reply_markup=keyboards.kb)
    await connect.close()


@router.message(F.text.lower() == "delete a title")
async def get_add_title(message: Message, state: FSMContext):
    await state.set_state(Delete_next_message.mes)
    await message.answer("Tell me what a title do you wanna delete?")


@router.message(Delete_next_message.mes)
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
        await message.answer(f"Your titles: {titles}", reply_markup=keyboards.kb)
    await connect.close()


@router.message()
async def what(message: Message):
    await message.answer("I didn't understand you :3")