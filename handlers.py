from keyboards import kb_start, kb_cancel
from bot_setup import SPREADSHEET_ID
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from sqlite_db import create_profile, edit_profile
from filters import NameCheck, PhoneCheck
from google_sheets import GoogleSheet, create_profile_gs, edit_profile_gs


gs = GoogleSheet(spreadsheet_id=SPREADSHEET_ID)

class ProfileStatesGroup(StatesGroup):
    name = State()
    phone = State()


async def start_command(message: types.Message):
    await message.answer("Чтобы записать данные нажмите на кнопку '/create'", reply_markup=kb_start)
    await message.delete()
    await create_profile(message.from_user.id)
    await create_profile_gs(gs, message.from_user.id)



async def cancel_command(message: types.Message, state: FSMContext):
    if state is None:
        return
    
    await state.finish()
    await message.reply("Вы прервали создание записи!", reply_markup=kb_start)


async def create_command(message: types.Message):
    await message.answer("Как вас зовут?", reply_markup=kb_cancel)
    await ProfileStatesGroup.name.set()


async def check_name(message: types.Message):
    await message.reply("Имя введено не корректно..")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    
    await message.reply("Спасибо, имя записано\nКакой ваш номер телефона ?")
    await ProfileStatesGroup.next()


async def check_phone(message: types.Message):
    await message.reply("Номер телефона введен не корректно..")


async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await edit_profile(state, message.from_user.id)
    await edit_profile_gs(gs, state, message.from_user.id)
    
    await message.reply("Спасибо, данные записаны", reply_markup=kb_start)
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(cancel_command, commands=['cancel'], state='*')
    dp.register_message_handler(create_command, commands=['create'])
    dp.register_message_handler(load_name, NameCheck(), state=ProfileStatesGroup.name)
    dp.register_message_handler(load_phone, PhoneCheck(), state=ProfileStatesGroup.phone)

    dp.register_message_handler(check_name, state=ProfileStatesGroup.name)

    dp.register_message_handler(check_phone, state=ProfileStatesGroup.phone)
    
    