from aiogram import Router, F
from src.initialisation import ADMIN_ID
from aiogram.types import CallbackQuery, BufferedInputFile
from src.keyboard import back_to_admin

router = Router()
router.message.filter(
    F.from_user.id == ADMIN_ID
)

@router.callback_query(F.data == "get_database")
async def answer_file_database(call: CallbackQuery) -> None:
    await call.message.delete()
    await call.message.answer_document(
        document=BufferedInputFile.from_file("database.json"),
        caption="Файл базы данных перед вами.\n\nВажно: Apple -> продукция Apple, Android -> продукция Android. "
                "Ключи price_min, price_max, markup отвечают за минимальную, максимальную стоимость услуги и наценку.",
        parse_mode=None,
        reply_markup=back_to_admin()
    )