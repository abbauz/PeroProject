from typing import Union
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ParseMode, ReplyKeyboardRemove
from keyboards.inline.main_inline import back_to_home, cashback_keyboard
from loader import dp, _, bot
from utils.db_api.database import get_user, get_lang, get_cash, get_cashback



@dp.callback_query_handler(text="cashback", state='*')
async def show_certificate(call: types.CallbackQuery, state: FSMContext):
    texts = []
    await state.finish()
    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = await get_lang(user_id)
    cash = await get_cashback(user_id)
    cashbacks = await get_cash(user_id)
    if lang == 'uz':
        texts = ['Jami keshbeklar', 'Qachondan', 'Qachongacha', 'Miqdori', 'Hozirda']
    elif lang == 'en':
        texts = ['All cashbacks', 'From', 'Until', 'The amount', 'At the moment']
    elif lang == 'ru':
        texts = ['Все кэшбэки', 'C', 'До', 'Kоличество', 'B настоящее время']
    text = f"<b>{texts[0]}</b>: {cash}\n\n"
    n = 1
    for cashback in cashbacks:
        text += f"{n}) <b>{texts[1]}</b>: {cashback.begin_date}\n   " \
                f"  <b>{texts[2]}</b>: {cashback.end_date}\n   " \
                f"  <b>{texts[3]}</b>: {cashback.count}%\n\n"
    text += f"<b>{texts[4]}</b>: {cash}%"
    markup = await cashback_keyboard(lang)
    await call.message.edit_text(text=text, reply_markup=markup)
    await state.set_state('cashback')
