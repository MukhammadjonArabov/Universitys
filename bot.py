import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
USERNAME = os.getenv("BOT_USERNAME")
API_URL = "http://127.0.0.1:8000/university-api/bot/sync-user/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = [
        [KeyboardButton(text="Telefon raqamni ulashish", request_contact=True)]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(
        "Xush kelibsiz! Saytda ro'yxatdan o'tish uchun telefon raqamingizni ulashing.",
        reply_markup=keyboard
    )

@dp.message(F.contact)
async def contact_handler(message: types.Message):
    contact = message.contact
    # Fallback to empty string if username or names are None
    data = {
        "telegram_id": message.from_user.id,
        "phone_number": contact.phone_number,
        "first_name": message.from_user.first_name or "",
        "last_name": message.from_user.last_name or "",
        "username": message.from_user.username or f"user_{message.from_user.id}"
    }
    
    print(f"DEBUG: Sending data to API: {data}")
    
    try:
        response = requests.post(API_URL, json=data)
        print(f"DEBUG: API Response Code: {response.status_code}")
        print(f"DEBUG: API Response Body: {response.text}")
        
        if response.status_code == 200:
            res_data = response.json()
            code = res_data.get("verification_code")
            await message.answer(
                f"Sizning tasdiqlash kodingiz: {code}\n"
                f"Ushbu kodni saytga kiriting.",
                reply_markup=types.ReplyKeyboardRemove()
            )
        else:
            await message.answer(f"Xatolik yuz berdi (Status: {response.status_code}). Iltimos keyinroq urinib ko'ring.")
    except Exception as e:
        print(f"DEBUG: Exception during API call: {e}")
        await message.answer(f"API bilan bog'lanishda xatolik: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
