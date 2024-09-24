from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import text, hbold, hitalic
from src.keyboard import calculator

router = Router()

@router.callback_query(F.data == "user_menu")
async def returning_user_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        text(
            hbold(f"Приветствую тебя, {call.from_user.full_name}!\n\n"),
            "Используй ",
            hitalic("кнопку, прикрепленную к этому сообщению "),
            "что бы посчитать стоимость услуги!",
            sep=""
        ),
        reply_markup=calculator()
    )