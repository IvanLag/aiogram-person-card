import handlers
from bot_setup import bot
from aiogram import  Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlite_db import create_customers_db


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print("Bot is running...")
    await create_customers_db()


if __name__ == '__main__':
    handlers.setup(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)