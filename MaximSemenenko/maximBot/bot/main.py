import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Импортируем handlers
from bot.handlers.user_handlers import router as user_router
from bot.handlers.application_handlers import router as application_router
from bot.handlers.meters_handlers import router as meters_router
from bot.database.db import create_pool

load_dotenv()

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Подключаем все routers
    dp.include_router(user_router)
    dp.include_router(application_router)
    dp.include_router(meters_router)
    
    await create_pool()
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())