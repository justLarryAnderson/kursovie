from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.database.db import Database
from bot.keyboards.main_kb import main_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🏠 Добро пожаловать в систему ЖКХ!\n"
        "Выберите нужный раздел:",
        reply_markup=main_kb
    )

@router.message(F.text == "🏠 Моя квартира")
async def my_apartment(message: types.Message):
    db = Database()
    user_id = message.from_user.id
    data = await db.get_user_apartment_info(user_id)
    
    if data:
        response = (
            f"🏠 Ваша квартира:\n"
            f"• Номер: {data['apartment_number']}\n"
            f"• Владелец: {data['full_name']}\n"
            f"• Телефон: {data['phone_number']}"
        )
    else:
        response = "❌ Информация о квартире не найдена"
    
    await message.answer(response)

@router.message(F.text == "💰 Задолженность")
async def debt_info(message: types.Message):
    db = Database()
    user_id = message.from_user.id
    debt = await db.get_debt(user_id)
    
    response = (
        f"💰 Ваша задолженность:\n"
        f"• Текущий долг: {debt or 0} руб.\n"
        f"• Срок оплаты: до 10 числа каждого месяца"
    )
    await message.answer(response)

@router.message(F.text == "ℹ️ Контакты")
async def contacts(message: types.Message):
    contacts_text = (
        "📞 Контакты Управляющей компании:\n\n"
        "• Телефон: +7 (495) 123-45-67\n"
        "• Email: uk@dom.ru\n"
        "• Адрес: ул. Примерная, д. 1\n"
        "• График работы: Пн-Пт 9:00-18:00\n\n"
        "⚡ Аварийная служба: +7 (495) 987-65-43"
    )
    await message.answer(contacts_text)