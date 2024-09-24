import aiofiles
import json
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from transliterate import translit
from src.initialisation import ADMIN_ID
from src import keyboard as nav

router = Router()
router.message.filter(
    F.from_user.id == ADMIN_ID
)
router.callback_query.filter(
    F.from_user.id == ADMIN_ID
)

class AddingSetting(StatesGroup):
    os = State()
    breaking = State()
    brand = State()
    display_or_lid = State()
    min = State()
    max = State()
    markup = State()

@router.callback_query(F.data == "add_departament")
async def add_departament_start(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Выберите OS телефона:",
        reply_markup=nav.os_chosen()
    )
    await state.set_state(AddingSetting.os)

@router.callback_query(AddingSetting.os)
async def after_os_chosen(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Введите поломку:\n\nПример: АКБ, замена дисплея и т.д.",
        reply_markup=nav.back_to_admin()
    )
    await state.update_data(os=call.data)
    await state.set_state(AddingSetting.breaking)

@router.message(AddingSetting.breaking)
async def after_breaking_chosen(message: Message, state: FSMContext):
    await state.update_data(breaking=translit(message.text.replace(" ", "_"), reversed=True))
    await message.answer(
        "Устройство разбирается с крышки или с экрана?",
        reply_markup=nav.display_or_lid_chosen()
    )
    await state.set_state(AddingSetting.display_or_lid)

@router.callback_query(AddingSetting.display_or_lid)
async def after_display_or_lid_chosen(call: CallbackQuery, state: FSMContext):
    await state.update_data(display_or_lid=call.data)
    await call.message.edit_text(
        "Введите название бренда на английском или нажмите \"Для всех брендов\"",
        reply_markup=nav.brand_chosen()
    )
    await state.set_state(AddingSetting.brand)

@router.message(AddingSetting.brand)
async def after_brand_chosen(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await message.answer(
        "Введите минимальную стоимость услуги:",
        reply_markup=nav.back_to_admin()
    )
    await state.set_state(AddingSetting.min)

@router.callback_query(AddingSetting.brand)
async def after_brand_chosen(call: CallbackQuery, state: FSMContext):
    await state.update_data(brand=call.data)
    await call.message.edit_text(
        "Введите минимальную стоимость услуги:",
        reply_markup=nav.back_to_admin()
    )
    await state.set_state(AddingSetting.min)

@router.message(AddingSetting.min)
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
    await state.set_state(AddingSetting.max)

@router.message(AddingSetting.max)
async def after_min_price_chosen(message: Message, state: FSMContext):
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
    await state.set_state(AddingSetting.markup)

@router.message(AddingSetting.markup)
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

    db["items"][data.get("os")].setdefault(data.get("breaking"), {}).setdefault(data.get("display_or_lid"), {}).setdefault(data.get("brand"), {})

    db["items"][data.get("os")][data.get("breaking")][data.get("display_or_lid")][data.get("brand")]["price_max"] = data.get("price_max")
    db["items"][data.get("os")][data.get("breaking")][data.get("display_or_lid")][data.get("brand")]["price_min"] = data.get("price_min")
    db["items"][data.get("os")][data.get("breaking")][data.get("display_or_lid")][data.get("brand")]["markup"] = data.get("markup")

    async with aiofiles.open("database.json", "w") as file:
        await file.write(json.dumps(db, indent=2, ensure_ascii=False))

    await state.clear()
    await message.answer("Отлично, вы добавили отдел!", reply_markup=nav.back_to_admin())