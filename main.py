from aiogram import Dispatcher, Bot, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)
from aiogram.filters import CommandStart
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


translations = {
    "uz": {
        "start": "Assalomu alaykum. Xush kelibsiz! 💫\nIltimos, tilni tanlang 👇",
        "register_btn": "Ro'yxatdan o'tish",
        "ask_name": "Iltimos, to‘liq ismingizni kiriting.",
        "ask_phone": "{} Telefon raqamingizni kiriting.",
        "ask_location": "Telefon qabul qilindi.\nManzilingizni yuboring.",
        "saved": "✅ Ma'lumotlar saqlandi!\n\n👤 Ism: {}\n📞 Telefon: {}\n📍 Joylashuv: {}",
        "share_phone_btn": "📞 Telefon raqamni ulashish.",
        "share_location_btn": "📍 Joylashuvni yuborish",
    },
    "en": {
        "start": "Hello. Welcome! 💫\nPlease select a language 👇",
        "register_btn": "Register",
        "ask_name": "Please enter your full name.",
        "ask_phone": "Thank you, {}! Please share or type your phone number.",
        "ask_location": "Phone number received.\nPlease share your location.",
        "saved": "✅ Your information has been saved!\n\n👤 Name: {}\n📞 Phone: {}\n📍 Location: {}",
        "share_phone_btn": "📞 Share phone number",
        "share_location_btn": "📍 Send location",
    },
    "ru": {
        "start": "Здравствуйте. Добро пожаловать! 💫\nПожалуйста, выберите язык 👇",
        "register_btn": "Регистрация",
        "ask_name": "Введите ваше полное имя.",
        "ask_phone": "Спасибо, {}! Пожалуйста, отправьте или введите ваш номер телефона.",
        "ask_location": "Номер телефона получен.\nПожалуйста, отправьте адрес или местоположение.",
        "saved": "✅ Ваши данные сохранены!\n\n👤 Имя: {}\n📞 Телефон: {}\n📍 Местоположение: {}",
        "share_phone_btn": "📞 Отправить номер телефона",
        "share_location_btn": "📍 Отправить местоположение",
    },
    "ar": {
        "start": "مرحباً. أهلاً وسهلاً! 💫\nيرجى اختيار اللغة 👇",
        "register_btn": "تسجيل",
        "ask_name": "الرجاء إدخال اسمك الكامل.",
        "ask_phone": "شكراً لك، {}! الرجاء إرسال أو إدخال رقم هاتفك.",
        "ask_location": "تم استلام رقم الهاتف.\nالرجاء إرسال الموقع أو كتابة العنوان.",
        "saved": "✅ تم حفظ بياناتك بنجاح!\n\n👤 الاسم: {}\n📞 الهاتف: {}\n📍 الموقع: {}",
        "share_phone_btn": "📞 إرسال رقم الهاتف",
        "share_location_btn": "📍 إرسال الموقع",
    },
}


@dp.message(CommandStart())
async def start_commit(message: Message, state: FSMContext):
    lang_code = message.from_user.language_code
    lang = lang_code if lang_code in translations else "en"
    await state.update_data(lang=lang)

    lang_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 uz"), KeyboardButton(text="🇺🇸 en")],
            [KeyboardButton(text="🇷🇺 ru"), KeyboardButton(text="🇸🇦 ar")],
        ],
        resize_keyboard=True,
    )

    await message.answer(translations[lang]["start"], reply_markup=lang_kb)


@dp.message(F.text.in_(["🇺🇿 uz", "🇺🇸 en", "🇷🇺 ru", "🇸🇦 ar"]))
async def choose_language(message: Message, state: FSMContext):
    lang = message.text.split()[-1]  
    await state.update_data(lang=lang)

    data = translations[lang]
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=data["register_btn"])]],
        resize_keyboard=True
    )

    await message.answer("🔑", reply_markup=kb)


@dp.message()
async def register_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    t = translations[lang]

    current_state = await state.get_state()

    if message.text == t["register_btn"]:
        await state.set_state(Register.name)
        await message.answer(t["ask_name"], reply_markup=ReplyKeyboardRemove())

    elif current_state == Register.name:
        await state.update_data(name=message.text)
        await state.set_state(Register.phone)

        phone_kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=t["share_phone_btn"], request_contact=True)]],
            resize_keyboard=True
        )

        await message.answer(t["ask_phone"].format(message.text), reply_markup=phone_kb)

    elif current_state == Register.phone:
        phone = message.contact.phone_number if message.contact else message.text
        await state.update_data(phone=phone)
        await state.set_state(Register.location)

        location_kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=t["share_location_btn"], request_location=True)]],
            resize_keyboard=True
        )

        await message.answer(t["ask_location"], reply_markup=location_kb)

    elif current_state == Register.location:
        if message.location:
            await state.update_data(
                location={
                    "latitude": message.location.latitude,
                    "longitude": message.location.longitude,
                }
            )
        else:
            await state.update_data(location=message.text)

        data = await state.get_data()
        await message.answer(
            t["saved"].format(data["name"], data["phone"], data["location"]),
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
