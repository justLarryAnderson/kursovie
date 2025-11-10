from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для типов заявок
application_type_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🚰 Сантехника", callback_data="app_plumbing")],
        [InlineKeyboardButton(text="⚡ Электрика", callback_data="app_electric")],
        [InlineKeyboardButton(text="🔥 Отопление", callback_data="app_heating")],
        [InlineKeyboardButton(text="🧹 Уборка", callback_data="app_cleaning")],
        [InlineKeyboardButton(text="🔨 Ремонт", callback_data="app_repair")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="app_cancel")]
    ]
)

# Клавиатура для управления заявками
application_manage_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📋 Мои заявки", callback_data="my_applications")],
        [InlineKeyboardButton(text="📝 Новая заявка", callback_data="new_application")]
    ]
)