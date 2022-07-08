from typing import Union
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ParseMode, ReplyKeyboardRemove
from loader import dp, _, bot
from utils.db_api.database import get_item, get_category_by_name, get_user, get_lang
from keyboards.inline.offers import *


@dp.callback_query_handler(text='offer_feedback', state='*')
async def feedback(call: CallbackQuery, state: FSMContext):
    texts = []
    await state.finish()
    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = await get_lang(user_id)
    if lang == 'uz':
        texts = ['Iltimos taklif va fikrlaringizni yozib qoldirin. Biz unga albatta uni bajarishga harakat qilamiz']
    elif lang == 'en':
        texts = ['Please leave your suggestions and comments. We will definitely try to make him do it']
    elif lang == 'ru':
        texts = ['Пожалуйста, напишите ваши предложения и мнения. Мы обязательно попробуем его заставить']

    markup = await offer_keys(lang)
    await state.set_state('offers')
    await call.message.edit_text(text=texts[0], reply_markup=markup, parse_mode=ParseMode.HTML)


@dp.callback_query_handler(text='back_offer', state='offers')
async def back_offer(call: CallbackQuery, state: FSMContext):
    texts = []
    await state.finish()
    user_id = call.from_user.id
    lang = await get_lang(user_id)
    if lang == 'uz':
        texts = ['Iltimos taklif va fikrlaringizni yozib qoldirin. Biz unga albatta uni bajarishga harakat qilamiz']
    elif lang == 'en':
        texts = ['Please leave your suggestions and comments. We will definitely try to make him do it']
    elif lang == 'ru':
        texts = ['Пожалуйста, напишите ваши предложения и мнения. Мы обязательно попробуем его заставить']

    markup = await offer_keys(lang)
    await state.set_state('offers')
    await call.message.edit_text(text=texts[0], reply_markup=markup, parse_mode=ParseMode.HTML)


@dp.callback_query_handler(text='send_offer', state='offers')
async def get_offer(call: CallbackQuery, state: FSMContext):
    texts = []
    user_id = call.from_user.id
    lang = await get_lang(user_id)
    if lang == 'uz':
        texts = ['Iltimos taklif va fikrlaringizni yozib qoldirin']
    elif lang == 'en':
        texts = ['Please leave your suggestions and comments']
    elif lang == 'ru':
        texts = ['Пожалуйста, напишите ваши предложения и мнения']

    markup = await offer_back(lang)
    await call.message.edit_text(text=texts[0], reply_markup=markup, parse_mode=ParseMode.HTML)


@dp.message_handler(state='offers')
async def get_message(message: Message, state: FSMContext):
    texts = []
    user_id = message.from_user.id
    lang = await get_lang(user_id)
    if lang == 'uz':
        texts = ['Iltimos taklif va fikrlaringizni yozib qoldirin. Biz unga albatta uni bajarishga harakat qilamiz',
                 'Murojaatingiz qabul qilindi']
    elif lang == 'en':
        texts = ['Please leave your suggestions and comments. We will definitely try to make him do it',
                 'Your message has been received']
    elif lang == 'ru':
        texts = ['Пожалуйста, напишите ваши предложения и мнения. Мы обязательно попробуем его заставить',
                 'Ваше сообщение получено']
    text = f"{texts[1]} ✅\n\n" \
           f"{texts[0]}"
    markup = await offer_keys(lang)
    await state.set_state('offers')
    await message.answer(text=text, reply_markup=markup, parse_mode=ParseMode.HTML)
