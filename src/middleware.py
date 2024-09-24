from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject
import aiofiles
import json

class BanMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        # async with aiofiles.open("database.json", "r") as db:
        #     users = json.loads(await db.read()).get("users")

        # for user in users:
        #     if user.get(str(data.get("event_from_user").id)) == "banned":
        #         return
        return await handler(event, data)
