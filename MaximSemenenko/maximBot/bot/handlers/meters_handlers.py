from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.database.db import Database
from bot.keyboards.meters_kb import meters_type_kb, submit_meter_kb
from bot.keyboards.main_kb import main_kb, cancel_kb

router = Router()

class MeterState(StatesGroup):
    choosing_type = State()
    entering_value = State()

@router.message(F.text == "📊 Показания счетчиков")
async def meters_menu(message: types.Message):
    db = Database()
    user_id = message.from_user.id
    meters = await db.get_user_meters(user_id)
    
    response = "📊 Ваши счетчики:\n\n"
    for meter in meters:
        response += f"• {meter['type']}: {meter['value']}\n"
    
    response += "\nВыберите действие:"
    await message.answer(response, reply_markup=meters_type_kb)

@router.callback_query(F.data.startswith("meter_"))
async def process_meter_action(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "meter_cancel":
        await callback.message.edit_text("❌ Действие отменено")
        await state.clear()
        return
    
    elif callback.data == "meter_all":
        db = Database()
        user_id = callback.from_user.id
        meters = await db.get_user_meters(user_id)
        
        response = "📊 Все показания счетчиков:\n\n"
        for meter in meters:
            response += f"• {meter['type']}: {meter['value']}\n"
        
        await callback.message.edit_text(response)
    
    elif callback.data in ["meter_cold", "meter_hot", "meter_electricity"]:
        meter_types = {
            "meter_cold": "💧 Холодная вода",
            "meter_hot": "🔥 Горячая вода", 
            "meter_electricity": "⚡ Электричество"
        }
        
        meter_type = meter_types[callback.data]
        await state.update_data(meter_type=meter_type)
        await callback.message.edit_text(
            f"Введите текущие показания для {meter_type}:\n"
            f"(только цифры, например: 125.50)",
            reply_markup=None
        )
        await state.set_state(MeterState.entering_value)
    
    await callback.answer()

@router.message(MeterState.entering_value)
async def process_meter_value(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await message.answer("❌ Ввод показаний отменен", reply_markup=main_kb)
        await state.clear()
        return
    
    try:
        value = float(message.text)
        data = await state.get_data()
        meter_type = data['meter_type']
        
        await message.answer(
            f"✅ Показания приняты:\n"
            f"Тип: {meter_type}\n"
            f"Значение: {value}",
            reply_markup=main_kb
        )
        
        # Сохраняем в базу
        db = Database()
        user_id = message.from_user.id
        await db.update_meter(user_id, meter_type, value)
        
        await state.clear()
        
    except ValueError:
        await message.answer("❌ Неверный формат. Введите число (например: 125.50)")