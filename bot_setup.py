from aiogram import Bot
from os import environ


token = environ.get('TOKEN')
admin_id = environ.get('ADMIN')
DB_NAME = "person_db.db"
SPREADSHEET_ID = environ.get('SPREADSHEET_ID')


bot = Bot(token)