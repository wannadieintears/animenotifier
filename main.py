import asyncio
from aiogram import Bot, Dispatcher
import settings
from handlers import handlers

bot = Bot(settings.token)
dp = Dispatcher()

async def main():
    dp.include_routers(
        handlers.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())