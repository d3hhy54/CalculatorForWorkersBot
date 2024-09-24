from aiogram import Router, F
from aiogram.types import CallbackQuery
from src import keyboard as nav
from src.initialisation import ADMIN_ID

router = Router()
router.message.filter(
    F.from_user.id == ADMIN_ID
)

@router.callback_query(F.data == "start_admin")
async def start_admin_panel(call: CallbackQuery) -> None:
    await call.message.edit_text(
        "Приветствую вас, администратор. "
        "Для использования панели используйте кнопки, прикреплённые к этому сообщению.",
        reply_markup=nav.admin()
    )