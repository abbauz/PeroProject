from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData


async def offer_keys(lang):
    texts = []
    if lang == 'uz':
        texts = ['Qoldirish', 'Bosh menyu']
    elif lang == 'en':
        texts = ['Send', 'Back menu']
    elif lang == 'ru':
        texts = ['Отправлять', 'Назад к меню']

    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=f"✍️ {texts[0]}", callback_data="send_offer"),
                InlineKeyboardButton(text=f"◀️ {texts[1]}", callback_data="back_home"),
            ]
        ]
    )
    return markup


async def offer_back(lang):
    texts = []
    if lang == 'uz':
        texts = ['Qoldirish', 'Orqaga']
    elif lang == 'en':
        texts = ['Send', 'Back']
    elif lang == 'ru':
        texts = ['Отправлять', 'Назад ']

    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=f"◀️ {texts[1]}", callback_data="back_offer"),
            ]
        ]
    )
    return markup

