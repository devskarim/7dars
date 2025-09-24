from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove,KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext 
from aiogram.fsm.state import State, StatesGroup 
from environs import Env

import logging
import asyncio

env = Env()
env.read_env()

dp = Dispatcher()
TOKEN = env.str("TOKEN")


@dp.message(CommandStart())
async def start_commit(message: Message):
    lang = message.from_user.language_code
    if lang == "uz":
        text = "Assalomu alaykum.  Xush kelibsiz! 💫 \nIltimos tilni tanlang 👇"
    elif lang == "ru":
        text = "Здравствуйте. Добро пожаловать! 💫 \nПожалуйста, выберите язык 👇"
    elif lang == "en":
        text = "Hello. Welcome! 💫 \nPlease select a language 👇"
    elif lang == "ar":
        text = "مرحباً. أهلاً وسهلاً! 💫 \nيرجى اختيار اللغة 👇"
    elif lang == "tr":
        text = "Merhaba. Hoş geldiniz! 💫 \nLütfen dili seçin 👇"
    elif lang == "es":
        text = "Hola. ¡Bienvenido! 💫 \nPor favor seleccione un idioma 👇"
    else:
        text = "Hello. Welcome! 💫 \nPlease select a language 👇"

    lang = ReplyKeyboardMarkup(
        keyboard= [
            [KeyboardButton(text="🇺🇿 uz"), KeyboardButton(text="🇺🇸 en")],
            [KeyboardButton(text="🇷🇺 ru"), KeyboardButton(text="🇸🇦 ar")]
				],resize_keyboard=True
		)

    await message.answer(text, reply_markup=lang)


@dp.message(F.text=="🇺🇿 uz")
async def lan_uz(message:Message): 
    name_kb =ReplyKeyboardMarkup(
        keyboard= [
            [KeyboardButton(text="Register:")]
				],resize_keyboard=True
		)
    
    await message.answer(f"🔑 Kirish uchun ro‘yxatdan o‘ting.",reply_markup=name_kb)
		



async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
