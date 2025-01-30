import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           CallbackQuery)
from config import API_TOKEN
from imei_checker import check_imei
from database import add_user_to_whitelist, is_user_allowed, create_table


logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher()


create_table()


def generate_start_buttons():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Проверить IMEI",
                              callback_data="check_imei")],
        [InlineKeyboardButton(text="ℹ️ Как работает бот?",
                              callback_data="how_it_works")]
    ])
    return keyboard


# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id

    add_user_to_whitelist(user_id)

    keyboard = generate_start_buttons()
    await message.answer("👋 Привет! Я бот для проверки IMEI. Выберите действие:", reply_markup=keyboard)


# Обработка нажатий на кнопки
@dp.callback_query()
async def process_callback(callback: CallbackQuery):
    data = callback.data

    if data == "check_imei":
        await callback.message.answer("📱 Отправьте мне IMEI для проверки.")
    elif data == "how_it_works":
        await callback.message.answer("ℹ️ Этот бот проверяет IMEI через API imeicheck.net.\nПросто отправьте мне IMEI, и я покажу вам информацию.")

    await callback.answer()


# Обработка сообщений с IMEI
@dp.message()
async def process_imei(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, есть ли пользователь в белом списке
    if not is_user_allowed(user_id):
        await message.answer("🚫 У вас нет доступа к боту.")
        return

    imei = message.text.strip()

    # Проверяем, что IMEI состоит из 15 цифр
    if not imei.isdigit() or len(imei) != 15:
        await message.answer("❌ Некорректный IMEI. Введите 15-значный IMEI.")
        return

    # Отправляем запрос в сервис IMEI
    result = await check_imei(imei)

    if "error" in result:
        await message.answer(f"⚠️ Ошибка при проверке IMEI: {result['error']}")
    else:
        info = result.get("data", {})
        response_text = f"📲 *Результат проверки IMEI {imei}:*\n\n"
        for key, value in info.items():
            response_text += f"🔹 *{key.capitalize()}*: {value}\n"

        await message.answer(response_text, parse_mode="Markdown")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
