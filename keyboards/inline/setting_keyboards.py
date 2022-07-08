from loader import _
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData


async def settings_markup(lang):
    texts = []
    if lang == 'uz':
        texts = ['Ismni o\'zgartirish', 'Raqamni o\'zgartirish', 'Tilni o\'zgartirish', 'Bosh menyu']
    elif lang == 'en':
        texts = ['Change name', 'Change phone number', 'Change language', 'Back menu']
    elif lang == 'ru':
        texts = ['Изменить имя', 'Изменить номер телефона', 'Изменить язык', 'Назад к меню']

    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=f"✏️{texts[0]}", callback_data="change_name"),
                InlineKeyboardButton(text=f"📲{texts[1]}", callback_data="change_phone"),
            ],
            [
                InlineKeyboardButton(text=f"🔄{texts[2]}", callback_data="change_language"),
                InlineKeyboardButton(text=f"◀️{texts[3]}", callback_data="back_home"),
            ],
        ]
    )
    return markup


async def back_settings(lang):
    text = ''
    if lang == 'uz':
        text = '🔙 Orqaga'
    elif lang == 'en':
        text = '🔙 Back'
    elif lang == 'ru':
        text = '🔙 Назад'
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text=f"{text}", callback_data="bact_settings"),
            ],
        ]
    )

    return markup
