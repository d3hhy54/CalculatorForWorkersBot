from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(
    token=os.getenv("TOKEN_BOT"),
    default=DefaultBotProperties(
        parse_mode="HTML"
    )
)

dp = Dispatcher(storage=MemoryStorage())
ADMIN_ID = None
