import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import text, hbold, hitalic
import aiofiles
import json
import src.keyboard as nav

router = Router()

class Contact(StatesGroup):
    contact = State()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    async with aiofiles.open("database.json", "r") as db:
        base = json.loads(await db.read())

    users = base.get("users")
    check = [user for user in users if user.get(str(message.from_user.id))]
    if any(check):
        if check[0].get(str(message.from_user.id)) == "unknown":
            await message.answer(
                "Приветствую, предоставьте ваш номер телефона для аутентификации.",
                reply_markup=nav.get_contact()
            )
            await state.set_state(Contact.contact)
            return
        elif check[0].get(str(message.from_user.id)) == "banned":
            await message.answer(
                "Приветствую, предоставьте ваш номер телефона для аутентификации."
                " Может быть вы появились в списке работников.",
                reply_markup=nav.get_contact()
            )
            await state.set_state(Contact.contact)
            return
        await message.answer(
            text(
                hbold(f"Приветствую тебя, {message.from_user.full_name}!\n\n"),
                "Используй ",
                hitalic("кнопку, прикрепленную к этому сообщению "),
                "что бы посчитать стоимость услуги!",
                sep=""
            ),
            reply_markup=nav.calculator(message.from_user.id)
        )
    else:
        base["users"].append({str(message.from_user.id): "unknown"})
        async with aiofiles.open("database.json", "w") as db:
            await db.write(json.dumps(base, indent=2, ensure_ascii=False))
        await message.answer(
            "Приветствую, предоставьте ваш номер телефона для аутентификации.",
            reply_markup=nav.get_contact()
        )

        await state.set_state(Contact.contact)

@router.message(Contact.contact, F.contact)
async def authentication(message: Message, state: FSMContext) -> None:
    print(message.contact.phone_number)
    if message.contact.user_id != message.from_user.id:
        await message.answer("Это не ваш контакт!")
        return

    async with aiofiles.open("database.json", "r") as db:
        base = json.loads(await db.read())

    for index, user in enumerate(base.get("users")):
        if user.get(str(message.from_user.id)) is not None:
            i = index
            break

    phone = message.contact.phone_number
    if phone.startswith("+"):
        phone = phone[1:]

    if phone not in base.get("workers"):
        base["users"][i][str(message.from_user.id)] = "banned"
        await message.answer(
            "Вы не прошли аутентификацию. Ваш аккаунт забанен.",
            reply_markup=ReplyKeyboardRemove()
        )
        logging.info(f"Banned user: id={message.from_user.id}, phone={message.contact.phone_number}")
    else:
        base["users"][i][str(message.from_user.id)] = "worker"
        await message.answer("Добро пожаловать!", reply_markup=ReplyKeyboardRemove())

    async with aiofiles.open("database.json", "w") as db:
        await db.write(json.dumps(base, indent=4, ensure_ascii=False))
    await state.clear()

