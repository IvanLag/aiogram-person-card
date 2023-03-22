from aiogram import Bot
from os import environ


token = environ.get('TOKEN')
admin_id = environ.get('ADMIN')


bot = Bot(token)