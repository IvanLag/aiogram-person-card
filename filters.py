import re
from aiogram.dispatcher.filters import Filter
from aiogram import types


class NameCheck(Filter):
    key = 'is_name'
    name_check_pattern = re.compile(r"^[а-яА-ЯёЁa-zA-Z_. ]+$")

    async def check(self, message: types.Message) -> bool:
        return self.name_check_pattern.match(message.text)
    

class PhoneCheck(Filter):
    key = 'is_phone'
    phone_check_pattern = re.compile(r"^(\+|)[0-9]+$")


    async def check(self, message: types.Message) -> bool:
        return self.phone_check_pattern.match(message.text)