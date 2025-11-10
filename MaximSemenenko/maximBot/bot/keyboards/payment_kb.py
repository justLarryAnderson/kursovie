from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для платежей
payment_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить онлайн", callback_data="pay_online")],
        [InlineKeyboardButton(text="📊 История платежей", callback_data="payment_history")],
        [InlineKeyboardButton(text="🧾 Квитанция", callback_data="payment_receipt")]
    ]
)