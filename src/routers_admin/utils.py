from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from src.initialisation import ADMIN_ID
from src import keyboard as nav

router = Router()
router.callback_query.filter(
    F.from_user.id == ADMIN_ID
)

@router.callback_query(F.data == "admin_menu")
async def returning_admin_menu(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    await state.clear()
    await call.message.answer(
        "Приветствую вас, администратор. "
        "Для использования панели используйте кнопки, прикреплённые к этому сообщению.",
        reply_markup=nav.admin()
    )