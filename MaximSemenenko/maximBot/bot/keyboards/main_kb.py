from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏠 Моя квартира"), KeyboardButton(text="💰 Задолженность")],
        [KeyboardButton(text="📊 Показания счетчиков"), KeyboardButton(text="🔧 Мои заявки")],
        [KeyboardButton(text="📝 Подать заявку"), KeyboardButton(text="ℹ️ Контакты")]
    ],
    resize_keyboard=True
)

# Кнопка отмены
cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]],
    resize_keyboard=True
)