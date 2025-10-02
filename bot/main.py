import asyncio

from aiogram import Bot, Dispatcher

from bot.handlers import router
from bot.conf import settings


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
