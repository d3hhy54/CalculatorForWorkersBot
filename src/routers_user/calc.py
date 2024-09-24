from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiofiles
import json
from src import keyboard as nav

router = Router()

class CalcSetting(StatesGroup):
    os = State()
    breaking = State()
    brand = State()
    analysis_device = State()

@router.callback_query(F.data == "calc_start")
async def calc_start(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text(
        "Выберите OS устройства:",
        reply_markup=nav.os_chosen("user_menu")
    )
    await state.set_state(CalcSetting.os)

@router.callback_query(CalcSetting.os)
async def after_os_chosen(call: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(os=call.data)
    await call.message.edit_text(
        "Какая поломка?",
        reply_markup=await nav.breaking_chosen(call.data, "user_menu")
    )
    await state.set_state(CalcSetting.breaking)

@router.callback_query(CalcSetting.breaking)
async def after_breaking_chosen(call: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(breaking=call.data)
    data = await state.get_data()
    await call.message.edit_text(
        "Как разбирается?",
        reply_markup=await nav.display_or_lid_for_item_chosen(data.get('os'), call.data, "user_menu")
    )
    await state.set_state(CalcSetting.analysis_device)

@router.callback_query(CalcSetting.analysis_device)
async def after_analysis_device_chosen(call: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(analysis_device=call.data)
    data = await state.get_data()
    await call.message.edit_text(
        "Какой бренд?",
        reply_markup=await nav.brand_for_selection(data.get('os'), data.get('breaking'), call.data, "user_menu")
    )
    await state.set_state(CalcSetting.brand)

@router.callback_query(CalcSetting.brand)
async def after_brand_chosen(call: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(brand=call.data)
    data = await state.get_data()
    async with aiofiles.open("database.json", "r") as file:
        info = json.loads(await file.read()).get('items').get(data.get('os')).get(data.get('breaking'))\
        .get(data.get("analysis_device")).get(data.get('brand'))
    text = ("Информация по предоставленным данным:\n\n"
            f"Минимальная стоимость: {info.get('price_min')}R\n"
            f"Максимальная стоимость: {info.get('price_max')}R\n"
            f"Наценка: {info.get('markup')}R")
    await call.message.edit_text(
        text,
        reply_markup=nav.back_to_user()
    )
    await state.clear()
