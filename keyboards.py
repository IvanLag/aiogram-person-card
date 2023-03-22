from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


kb_start = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[['/create']])
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[['/cancel']])
