import asyncio, os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers import router

load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
