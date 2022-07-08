from loader import _
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.database import *


async def pay_type(lang):
    text = []
    if lang == 'uz':
        text = ['Click', 'Payme', 'Orqaga']
    elif lang == 'ru':
        text = ['Click', 'Payme', 'Назад']
    elif lang == 'en':
        text = ['Click', 'Payme', 'Back']

    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=f"💳 {text[0]}", callback_data="click"),
                InlineKeyboardButton(text=f"💰 {text[1]}", callback_data="payme"),
            ],
            [
                InlineKeyboardButton(text=f"🔙 {text[2]}", callback_data="back_choose"),
            ]
        ]
    )
    return markup


async def money_type(lang):
    text = []
    if lang == 'uz':
        text = ['Naqd pul orqali', 'Online', 'Orqaga']
    elif lang == 'ru':
        text = ['Наличными', 'Online', 'Back']
    elif lang == 'en':
        text = ['In cash', 'Online', 'Назад']

    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=f"💴 {text[0]}", callback_data="offline"),
                InlineKeyboardButton(text=f"💳 {text[1]}", callback_data="online"),
            ],
            [
                InlineKeyboardButton(text=f"🔙 {text[2]}", callback_data="cart"),
            ]
        ]
    )
    return markup


async def location_send(lang):
    text = []
    if lang == 'uz':
        text = ['Joylashuvni ulashish', 'Oldingi manzillar']
    elif lang == 'ru':
        text = ['Отправить местоположение', 'Предыдущие адреса']
    elif lang == 'en':
        text = ['Send location', 'Previous addresses']
    mrk = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bt = KeyboardButton(f'📍 {text[0]}', request_location=True)
    btn = KeyboardButton(f'🔂 {text[1]}')
    mrk.add(bt, btn)

    return mrk


async def location_keys(user_id, lang):
    locs = await get_address(user_id)
    markup = InlineKeyboardMarkup(row_width=3)
    text = []
    if lang == 'uz':
        text = ['Orqaga']
    elif lang == 'ru':
        text = ['Назад']
    elif lang == 'en':
        text = ['Back']

    if locs:
        for i in locs:
            markup.row(InlineKeyboardButton(text=f"{i.name}", callback_data=f'loc_{i.id}'))
        markup.row(InlineKeyboardButton(text=f"◀️{text[0]}", callback_data='back_to_address'))
        return markup
    else:
        return None


async def confirm_address(lang):
    text = []
    if lang == 'uz':
        text = ['Taqdiqlash', 'Qayta jo\'natish', 'Orqaga']
    elif lang == 'ru':
        text = ['Подтвердить', 'Отправить повторно', 'Назад']
    elif lang == 'en':
        text = ['Confirm', 'Send again', 'Back']
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=f"✅ {text[0]}", callback_data="confirm"),
                InlineKeyboardButton(text=f"🔄 {text[1]}", callback_data="cancel"),
            ],
            [
                InlineKeyboardButton(text=f"🔙 {text[2]}", callback_data="back_to_addres"),
            ]
        ]
    )
    return markup
