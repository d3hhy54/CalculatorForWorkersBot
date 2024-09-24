from initialisation import *
from src.routers_user.start import router as start_user
from src.routers_user.calc import router as calc_user
from src.routers_user.utils import router as utils_user
from src.routers_admin.start import router as start_admin
from src.routers_admin.get_database import router as get_file
from src.routers_admin.add_worker import router as add_worker
from src.routers_admin.add_departament import router as add_departament
from src.routers_admin.change_departament import router as change_departament
from src.routers_admin.utils import router as utils_admin
from middleware import BanMiddleware
import asyncio
import logging

async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(utils_user, calc_user, start_user, start_admin, get_file,
                       utils_admin, add_worker, add_departament, change_departament)
    dp.message.outer_middleware(BanMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
