import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
import logging

from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.database import db_helper
from app.database.models import Base

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()


async def create_tables() -> AsyncEngine:
    """
        Создание таблиц в базе данных.
    """
    engine = db_helper.engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_tables()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
