from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для счетчиков
meters_type_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💧 Холодная вода", callback_data="meter_cold")],
        [InlineKeyboardButton(text="🔥 Горячая вода", callback_data="meter_hot")],
        [InlineKeyboardButton(text="⚡ Электричество", callback_data="meter_electricity")],
        [InlineKeyboardButton(text="📊 Все показания", callback_data="meter_all")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="meter_cancel")]
    ]
)

# Клавиатура для подачи показаний
submit_meter_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="meter_submit")],
        [InlineKeyboardButton(text="✏️ Изменить", callback_data="meter_edit")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="meter_cancel")]
    ]
)