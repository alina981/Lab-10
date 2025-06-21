import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import router
import sqlite3
from dotenv import load_dotenv

load_dotenv()


# Синхронная версия (без async)
def init_db():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            birth_date TEXT,
            phone TEXT,
            bank TEXT
        )
    ''')

    conn.commit()
    conn.close()


async def main():
    # Инициализируем базу данных (синхронный вызов)
    init_db()

    bot = Bot(token="8075714721:AAF053-mBOuGP_AxzPUXeaLhABQM04CIgJE")
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')
    except Exception as e:
        print(f'Произошла ошибка: {e}')