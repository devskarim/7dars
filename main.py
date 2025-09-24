from aiogram import Dispatcher, Bot, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)
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


class Register(StatesGroup):
    name = State()
    phone = State()
    location = State()


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
        keyboard=[
            [KeyboardButton(text="🇺🇿 uz"), KeyboardButton(text="🇺🇸 en")],
            [KeyboardButton(text="🇷🇺 ru"), KeyboardButton(text="🇸🇦 ar")],
        ],
        resize_keyboard=True,
    )

    await message.answer(text, reply_markup=lang)


@dp.message(F.text == "🇺🇿 uz")
async def lan_uz(message: Message):
    name_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Register")]], resize_keyboard=True
    )

    await message.answer(f"🔑 Kirish uchun ro‘yxatdan o‘ting.", reply_markup=name_kb)


@dp.message(F.text == "Register")
async def start_register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer(
        f"Iltimos toliq ismningizni kiriting .", reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.set_state(Register.phone)
    name = message.text

    await state.update_data(name = message.text)

    phone_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Telefon raqamni ulashish.", request_contact=True)]
        ],
        resize_keyboard=True,
    )
    await message.answer(
        f"{name} Telefon raqamingizni kiriting.",
        reply_markup=phone_kb,
    )


@dp.message(Register.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.set_state(Register.location)
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone = phone)

    location_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍Joylashuvni yuborish", request_location=True)]
        ],resize_keyboard=True
    )

    await message.answer(
        "Telefon qabul qilindi\nAdressni Kiriting.", reply_markup=location_kb
        )


@dp.message(Register.location) 
async def get_location(message:Message, state:FSMContext): 

    if message.location: 
        await state.update_data(
            location = {
                "latitude": message.location.latitude,
                "longitude": message.location.longitude
            }
        )
    else: 
        await state.update_data(location = message.text)

    data = await state.get_data() 
    name = data.get("name") 
    phone = data.get("phone")
    location = data.get("location") 

    await message.answer(
        f"✅ Ma'lumotlar saqlandi!\n\n"
        f"👤 Ism: {name}\n"
        f"📞 Telefon: {phone}\n"
        f"📍 Joylashuv: {location}",reply_markup=ReplyKeyboardRemove()
    )


@dp.message(F.text == "🇺🇸 en")
async def lan_en(message: Message):
    name_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Register")]], resize_keyboard=True
    )

    await message.answer("🔑 Please register to continue.", reply_markup=name_kb)


@dp.message(F.text == "Register")
async def start_register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer(
        "Please enter your full name.", reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.set_state(Register.phone)
    name = message.text
    await state.update_data(name=name)

    phone_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Share phone number", request_contact=True)]
        ],
        resize_keyboard=True,
    )

    await message.answer(
        f"Thank you {name}! Please share or type your phone number.",
        reply_markup=phone_kb,
    )


@dp.message(Register.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.set_state(Register.location)
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)

    location_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Send Location", request_location=True)]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Phone number received.\nPlease share your address or location.",
        reply_markup=location_kb
    )


@dp.message(Register.location)
async def get_location(message: Message, state: FSMContext):
    if message.location:
        await state.update_data(
            location={
                "latitude": message.location.latitude,
                "longitude": message.location.longitude
            }
        )
    else:
        await state.update_data(location=message.text)

    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")
    location = data.get("location")

    await message.answer(
        f"✅ Your information has been saved!\n\n"
        f"👤 Name: {name}\n"
        f"📞 Phone: {phone}\n"
        f"📍 Location: {location}",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(F.text == "🇷🇺 ru")
async def lan_ru(message: Message):
    name_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Регистрация")]], resize_keyboard=True
    )

    await message.answer("🔑 Пожалуйста, зарегистрируйтесь, чтобы продолжить.", reply_markup=name_kb)


@dp.message(F.text == "Регистрация")
async def start_register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer(
        "Введите ваше полное имя.", reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.set_state(Register.phone)
    name = message.text
    await state.update_data(name=name)

    phone_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Отправить номер телефона", request_contact=True)]
        ],
        resize_keyboard=True,
    )

    await message.answer(
        f"Спасибо, {name}! Пожалуйста, отправьте или введите ваш номер телефона.",
        reply_markup=phone_kb,
    )


@dp.message(Register.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.set_state(Register.location)
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)

    location_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Отправить местоположение", request_location=True)]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Номер телефона получен.\nПожалуйста, отправьте адрес или местоположение.",
        reply_markup=location_kb
    )


@dp.message(Register.location)
async def get_location(message: Message, state: FSMContext):
    if message.location:
        await state.update_data(
            location={
                "latitude": message.location.latitude,
                "longitude": message.location.longitude
            }
        )
    else:
        await state.update_data(location=message.text)

    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")
    location = data.get("location")

    await message.answer(
        f"✅ Ваши данные сохранены!\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📍 Местоположение: {location}",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(F.text == "🇸🇦 ar")
async def lan_ar(message: Message):
    name_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="تسجيل")]], resize_keyboard=True
    )

    await message.answer("🔑 من فضلك، قم بالتسجيل للمتابعة.", reply_markup=name_kb)


@dp.message(F.text == "تسجيل")
async def start_register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer(
        "الرجاء إدخال اسمك الكامل.", reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.set_state(Register.phone)
    name = message.text
    await state.update_data(name=name)

    phone_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 إرسال رقم الهاتف", request_contact=True)]
        ],
        resize_keyboard=True,
    )

    await message.answer(
        f"شكراً لك، {name}! الرجاء إرسال أو إدخال رقم هاتفك.",
        reply_markup=phone_kb,
    )


@dp.message(Register.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.set_state(Register.location)
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)

    location_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 إرسال الموقع", request_location=True)]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "تم استلام رقم الهاتف.\nالرجاء إرسال الموقع أو كتابة العنوان.",
        reply_markup=location_kb
    )


@dp.message(Register.location)
async def get_location(message: Message, state: FSMContext):
    if message.location:
        await state.update_data(
            location={
                "latitude": message.location.latitude,
                "longitude": message.location.longitude
            }
        )
    else:
        await state.update_data(location=message.text)

    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")
    location = data.get("location")

    await message.answer(
        f"✅ تم حفظ بياناتك بنجاح!\n\n"
        f"👤 الاسم: {name}\n"
        f"📞 الهاتف: {phone}\n"
        f"📍 الموقع: {location}",
        reply_markup=ReplyKeyboardRemove()
    )



async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
