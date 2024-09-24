from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiofiles
import json
from src.initialisation import ADMIN_ID
from src import keyboard as nav

router = Router()
router.message.filter(
    F.from_user.id == ADMIN_ID
)
router.callback_query.filter(
    F.from_user.id == ADMIN_ID
)

class ChangingSetting(StatesGroup):
    os = State()
    breaking = State()
    brand = State()
    display_or_lid = State()
    min = State()
    max = State()
    markup = State()

@router.callback_query(F.data == "change_departament")
async def change_departament_start(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Выберите OS устройства:",
        reply_markup=nav.os_chosen()
    )
    await state.set_state(ChangingSetting.os)

@router.callback_query(ChangingSetting.os)
async def os_chosen(call: CallbackQuery, state: FSMContext):
    await state.update_data(os=call.data)
    await call.message.edit_text(
        "Выберите поломку:",
        reply_markup=await nav.breaking_chosen(call.data)
    )
    await state.set_state(ChangingSetting.breaking)

@router.callback_query(ChangingSetting.breaking)
async def breaking_chosen(call: CallbackQuery, state: FSMContext):
    await state.update_data(breaking=call.data)
    data = await state.get_data()
    async with aiofiles.open("database.json", "r") as file:
        db = json.loads(await file.read())
    if not db['items'].get(data.get('os')).get(call.data):
        await call.answer("Там ничего нет! Используйте кнопку\"Добавить отдел\".", show_alert=True)
        return
    await call.message.edit_text(
        "Как разбирается?",
        reply_markup=await nav.display_or_lid_for_item_chosen(data.get('os'), call.data)
    )
    await state.set_state(ChangingSetting.display_or_lid)

@router.callback_query(ChangingSetting.display_or_lid)
async def display_or_lid_chosen(call: CallbackQuery, state: FSMContext):
    await state.update_data(display_or_lid=call.data)
    data = await state.get_data()

    await call.message.edit_text(
        "Выберите бренд устройства:",
        reply_markup=await nav.brand_for_selection(data.get('os'), data.get('breaking'), call.data)
    )
    await state.set_state(ChangingSetting.brand)

@router.callback_query(ChangingSetting.brand)
async def brand_chosen(call: CallbackQuery, state: FSMContext):
    await state.update_data(brand=call.data)
    await call.message.edit_text(
        "Введите новое значение минимальной стоимости:",
        reply_markup=nav.back_to_admin()
    )
    await state.set_state(ChangingSetting.min)

@router.message(ChangingSetting.min)
async def after_min_price_chosen(message: Message, state: FSMContext):
    try:
        price_min = int(message.text)
    except:
        await message.answer(
            "Введите только целое число!",
            reply_markup=nav.back_to_admin()
        )
        return
    await state.update_data(price_min=price_min)
    await message.answer(
        "Введите максимальную стоимость услуги:",
        reply_markup=nav.back_to_admin()
    )
    await state.set_state(ChangingSetting.max)

@router.message(ChangingSetting.max)
async def after_max_price_chosen(message: Message, state: FSMContext):
    try:
        price_max = int(message.text)
    except:
        await message.answer(
            "Введите только целое число!",
            reply_markup=nav.back_to_admin()
        )
        return
    await state.update_data(price_max=price_max)
    await message.answer(
        "Введите наценку услуги: ",
        reply_markup=nav.back_to_admin()
    )
    await state.set_state(ChangingSetting.markup)

@router.message(ChangingSetting.markup)
async def after_markup_chosen(message: Message, state: FSMContext):
    try:
        markup = int(message.text)
    except:
        await message.answer(
            "Введите только целое число!",
            reply_markup=nav.back_to_admin()
        )
        return
    await state.update_data(markup=markup)
    data = await state.get_data()

    async with aiofiles.open("database.json", "r") as file:
        db = json.loads(await file.read())

    db["items"][data.get("os")][data.get("breaking")][data.get("display_or_lid")][data.get("brand")][
        "price_max"] = data.get("price_max")
    db["items"][data.get("os")][data.get("breaking")][data.get("display_or_lid")][data.get("brand")][
        "price_min"] = data.get("price_min")
    db["items"][data.get("os")][data.get("breaking")][data.get("display_or_lid")][data.get("brand")][
        "markup"] = data.get("markup")

    async with aiofiles.open("database.json", "w") as file:
        await file.write(json.dumps(db, indent=2, ensure_ascii=False))

    await state.clear()
    await message.answer(
        "Операция прошла успешно!",
        reply_markup=nav.back_to_admin()
    )