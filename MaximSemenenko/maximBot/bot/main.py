import asyncio
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем handlers
from handlers.user_handlers import router as user_router
from handlers.application_handlers import router as application_router
from handlers.meters_handlers import router as meters_router
from database.db import Database  # Импортируем класс, а не функцию

load_dotenv()

async def main():
    try:
        bot = Bot(token=os.getenv('BOT_TOKEN'))
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        # Подключаем все routers
        dp.include_router(user_router)
        dp.include_router(application_router)
        dp.include_router(meters_router)
        
        # Инициализируем базу данных - создаем экземпляр и вызываем метод
        db = Database()
        await db.create_pool()  # Теперь это метод экземпляра
        
        print("✅ Бот запущен!")
        await dp.start_polling(bot)
        
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")

if __name__ == '__main__':
    asyncio.run(main())