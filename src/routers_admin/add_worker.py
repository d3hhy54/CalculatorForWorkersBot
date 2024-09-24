import aiofiles
import json
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from src.initialisation import ADMIN_ID
from src import keyboard as nav


router = Router()
router.message.filter(
    F.from_user.id == ADMIN_ID
)
router.callback_query.filter(
    F.from_user.id == ADMIN_ID
)

class AddWorkerParams(StatesGroup):
    number = State()

@router.callback_query(F.data == "add_worker")
async def add_worker_start(call: CallbackQuery, state: FSMContext):
    answer = await call.message.edit_text(
        "Для добавления работника отправьте его контакт(через скрепку)"
        " либо отправьте его номер телефона. Важно: "
        "номер телефона должен быть без плюсов, скобок, дефисов.",
        reply_markup=nav.back_to_admin()
    )
    await state.update_data(id=answer.message_id)
    await state.set_state(AddWorkerParams.number)

@router.message(AddWorkerParams.number, F.contact | F.text.isdigit())
async def number_chosen(message: Message, state: FSMContext):
    async with aiofiles.open("database.json", "r") as db:
        base = json.loads(await db.read())

    if message.contact:
        phone = message.contact.phone_number
        if phone.startswith("+"):
            phone = phone[1:]
        base.get("workers").append(str(phone))
    else:
        base.get("workers").append(message.text)

    async with aiofiles.open("database.json", "w") as db:
        await db.write(json.dumps(base, indent=2, ensure_ascii=False))

    await message.answer(
        "Работник успешно добавлен!",
        reply_markup=nav.back_to_admin()
    )
    await state.clear()

@router.message(AddWorkerParams.number)
async def number_chosen(message: Message, state: FSMContext):
    id = (await state.get_data()).get("id")
    await message.answer(
        "Предерживайтесь условиям вашего ответа! Бот требует таких форматов.",
        reply_markup=nav.back_to_admin(),
        reply_to_message_id=id
    )