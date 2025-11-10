from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.database.db import Database
from bot.keyboards.application_kb import application_type_kb, application_manage_kb
from bot.keyboards.main_kb import main_kb, cancel_kb

router = Router()

class ApplicationState(StatesGroup):
    choosing_type = State()
    entering_description = State()

@router.message(F.text == "📝 Подать заявку")
async def start_application(message: types.Message, state: FSMContext):
    await message.answer(
        "🚨 Выберите тип заявки:",
        reply_markup=application_type_kb
    )
    await state.set_state(ApplicationState.choosing_type)

@router.message(F.text == "🔧 Мои заявки")
async def my_applications(message: types.Message):
    db = Database()
    user_id = message.from_user.id
    applications = await db.get_user_applications(user_id)
    
    if not applications:
        await message.answer("📭 У вас нет активных заявок")
        return
    
    response = "📋 Ваши заявки:\n\n"
    for app in applications:
        status_emoji = "✅" if app['status'] == 'completed' else "🔄" if app['status'] == 'in_progress' else "⏳"
        response += f"{status_emoji} {app['type']}: {app['description']}\nСтатус: {app['status']}\n\n"
    
    await message.answer(response)

@router.callback_query(F.data.startswith("app_"))
async def process_application_type(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "app_cancel":
        await callback.message.edit_text("❌ Создание заявки отменено")
        await state.clear()
        return
    
    application_types = {
        "app_plumbing": "🚰 Сантехника",
        "app_electric": "⚡ Электрика", 
        "app_heating": "🔥 Отопление",
        "app_cleaning": "🧹 Уборка",
        "app_repair": "🔨 Ремонт"
    }
    
    app_type = application_types.get(callback.data)
    if app_type:
        await state.update_data(application_type=app_type)
        await callback.message.edit_text(
            f"📝 Вы выбрали: {app_type}\n"
            f"Опишите проблему подробно:",
            reply_markup=None
        )
        await state.set_state(ApplicationState.entering_description)
    
    await callback.answer()

@router.message(ApplicationState.entering_description)
async def process_application_description(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await message.answer("❌ Создание заявки отменено", reply_markup=main_kb)
        await state.clear()
        return
    
    data = await state.get_data()
    app_type = data['application_type']
    
    # Сохраняем заявку в базу
    db = Database()
    user_id = message.from_user.id
    await db.create_application(user_id, app_type, message.text)
    
    await message.answer(
        f"✅ Заявка создана!\n\n"
        f"Тип: {app_type}\n"
        f"Описание: {message.text}\n\n"
        f"Мы свяжемся с вами в ближайшее время.",
        reply_markup=main_kb
    )
    await state.clear()