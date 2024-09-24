from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from transliterate import translit
from src.initialisation import ADMIN_ID
import aiofiles
import json

def get_contact() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="Отправить контакт", request_contact=True)
            ]
        ]
    )

def admin() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить работника", callback_data="add_worker")
            ],
            [
                InlineKeyboardButton(text="Добавить отдел", callback_data="add_departament"),
                InlineKeyboardButton(text="Изменить отдел", callback_data="change_departament")
            ],
            [
                InlineKeyboardButton(text="Получить файл базы данных", callback_data="get_database")
            ]
        ]
    )

def back_to_admin() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад", callback_data="admin_menu")
            ]
        ]
    )

def os_chosen(returning: str = "admin_menu") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="IOS", callback_data="Apple"),
                InlineKeyboardButton(text="Android", callback_data="Android")
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data=returning)
            ]
        ]
    )

def display_or_lid_chosen() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="С крышки", callback_data="lid"),
                InlineKeyboardButton(text="С экрана", callback_data="display")
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="admin_menu")
            ]
        ]
    )

def brand_chosen() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Для всех брендов", callback_data="all")
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="admin_menu")
            ]
        ]
    )

async def breaking_chosen(os: str, returning: str = "admin_menu") -> InlineKeyboardMarkup:
    async with aiofiles.open("database.json", "r") as file:
        items = json.loads(await file.read()).get("items").get(os)

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=translit(item.replace("_", " "), 'ru', reversed=False), callback_data=item) for item in items.keys()
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data=returning)
            ]
        ]
    )


async def display_or_lid_for_item_chosen(os: str, breaking: str, returning: str = "admin_menu") -> InlineKeyboardMarkup:
    async with aiofiles.open("database.json", "r") as file:
        tests = json.loads(await file.read()).get('items').get(os).get(breaking)

    buttons = [
        InlineKeyboardButton(text='С крышки', callback_data='lid') if tests.get('lid') else None,
        InlineKeyboardButton(text='С экрана', callback_data='display') if tests.get('display') else None
    ]
    for i, button in enumerate(buttons):
        if button is None:
            del buttons[i]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            buttons,
            [
                InlineKeyboardButton(text='Назад', callback_data=returning)
            ]
        ]
    )

async def brand_for_selection(os: str, breaking: str, analysis_device: str, returning: str = "admin_menu") -> InlineKeyboardMarkup:
    async with aiofiles.open("database.json", "r") as file:
        brands = json.loads(await file.read()).get('items').get(os).get(breaking).get(analysis_device)

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=brand if brand != "all" else "Для всех брендов", callback_data=brand) for brand in brands
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data=returning)
            ]
        ]
    )

def calculator(id: int) -> InlineKeyboardMarkup:
    buttons = [
        [
                InlineKeyboardButton(text="Начать", callback_data="calc_start")
        ],
        [
                InlineKeyboardButton(text='Админ панель', callback_data="start_admin")
        ] if id == ADMIN_ID else None
    ]
    for index, button in enumerate(buttons):
        if button is None:
            del buttons[index]


    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

def back_to_user() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data='user_menu')
            ]
        ]
    )