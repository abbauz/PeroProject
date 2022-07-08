from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.inline.main_inline import menu_button, languages_markup, contact_btn, back_to_home, about_us_btn
from utils.db_api import database as commands
from loader import dp, _, bot
import validators
from utils.db_api.database import get_about_us, get_user, get_lang
import phonenumbers
from filters.admin_filter import IsAdmin


@dp.message_handler(IsAdmin(), content_types=types.ContentType.DOCUMENT)
async def send_file_id(message: types.Message):
    await message.answer(f"FILE ID:\n\n<pre>{message.document.file_id}</pre>")


@dp.message_handler(IsAdmin(), content_types=types.ContentType.PHOTO)
async def send_image_id(message: types.Message):
    await message.answer(f"Image ID:\n\n<pre>{message.photo[-1].file_id}</pre>")


@dp.message_handler(IsAdmin(), content_types=types.ContentType.VIDEO)
async def send_vide_id(message: types.Message):
    await message.answer(f"Vide ID:\n\n<pre>{message.video.file_id}</pre>")


@dp.callback_query_handler(text="back_home", state='*')
async def back_home_fun(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    await call.message.delete()
    user_id = call.from_user.id
    lang = await get_lang(user_id)
    text = ''
    if lang == 'uz':
        text = 'Xush kelibsiz👋.\nBuyurtma berish uchun Mahsulotlar tugmasini bosing!'
    elif lang == 'ru':
        text = 'Добро пожаловать👋.\nНажмите кнопку Товары, чтобы заказать!'
    elif lang == 'en':
        text = 'Welcome👋.\nClick the Products button to order!'
    menu = await menu_button(lang=await commands.get_lang(user_id))
    await call.message.answer(_(f"{text}"), reply_markup=menu)


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    user = await commands.get_user(user_id)
    if user:
        text = ''
        if user.is_active:
            lang = await get_lang(user_id)
            if lang == 'uz':
                text = 'Xush kelibsiz👋.\nBuyurtma berish uchun Mahsulotlar tugmasini bosing!'
            elif lang == 'ru':
                text = 'Добро пожаловать👋.\nНажмите кнопку Товары, чтобы заказать!'
            elif lang == 'en':
                text = 'Welcome👋.\nClick the Products button to order!'
            menu = await menu_button(lang=await commands.get_lang(user_id))
            await message.answer(_(f"{text}"), reply_markup=menu)
        else:
            markup = await languages_markup()
            await message.answer("Choose your language!\n\nВыберите удобный Вам язык!.",
                                 reply_markup=markup)
            await state.set_state("get_lang")
    else:
        markup = await languages_markup()
        await message.answer("Choose your language!\n\nВыберите удобный Вам язык!.",
                             reply_markup=markup)
        await state.set_state("get_lang")


@dp.callback_query_handler(text_contains="lang", state="get_lang")
async def change_lang(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user_id = call.from_user.id
    await call.message.edit_reply_markup()
    lang = call.data[-2:]
    await state.update_data(lang=lang)
    text = ''
    if lang == 'uz':
        text = 'Telefon raqamingizni xalqaro formatda kiriting\nMasalan: +998901234567'
    elif lang == 'ru':
        text = 'Введите номер в международном формате\nНапример: +998901234567'
    elif lang == 'en':
        text = 'Enter the number in international format\nFor example: +998901234567'
    await commands.add_user(user_id=user_id, name=call.from_user.full_name, phone="", lang=lang)
    await state.update_data(name=call.from_user.full_name)
    await call.message.answer(text=_(f"{text}"))
    await state.set_state("phone")


@dp.message_handler(state="phone")
async def get_confirm_secret_phone(message: types.Message, state: FSMContext):
    phone = message.text
    try:
        my_number = phonenumbers.parse(f"{phone}", "GB")
        if phonenumbers.is_valid_number(my_number):
            # user_id = message.from_user.id
            data = await state.get_data()
            lang = data.get("lang")
            menu = await contact_btn(lang=lang)
            text = ''
            if lang == 'uz':
                text = 'Telefon raqamingizga yuborilhan kodni kiriting'
            elif lang == 'ru':
                text = 'Введите код, отправленный на ваш номер телефона'
            elif lang == 'en':
                text = 'Enter the code sent to your phone number'
            await state.update_data(phone=phone)
            await bot.send_message(chat_id=message.from_user.id, text=_(f"{text}"), reply_markup=menu)
            await state.set_state('check_number')
        else:
            data = await state.get_data()
            lang = data.get("lang")
            text = ''
            if lang == 'uz':
                text = 'Telefon raqamingizni xalqaro formatda kiriting\nMasalan: +998901234567'
            elif lang == 'ru':
                text = 'Введите номер в международном формате\nНапример: +998901234567'
            elif lang == 'en':
                text = 'Enter the number in international format\nFor example: +998901234567'
            await message.answer(_(f"{text}"))
            await state.set_state("phone")
    except Exception as exx:
        print(exx)
        data = await state.get_data()
        lang = data.get("lang")
        text = ''
        if lang == 'uz':
            text = 'Telefon raqamingizni xalqaro formatda kiriting\nMasalan: +998901234567'
        elif lang == 'ru':
            text = 'Введите номер в международном формате\nНапример: +998901234567'
        elif lang == 'en':
            text = 'Enter the number in international format\nFor example: +998901234567'

        await message.answer(_(f"{text}"))
        await state.set_state("phone")


@dp.message_handler(state='check_number')
async def check_numbers(message: types.Message, state: FSMContext):
    code = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get('lang')
    if code in ['🔙 Orqaga', '🔙 Back', '🔙 Назад']:
        text = ''
        if lang == 'uz':
            text = 'Telefon raqamingizni xalqaro formatda kiriting\nMasalan: +998901234567'
        elif lang == 'ru':
            text = 'Введите номер в международном формате\nНапример: +998901234567'
        elif lang == 'en':
            text = 'Enter the number in international format\nFor example: +998901234567'
        await message.answer(text=_(f"{text}"), reply_markup=ReplyKeyboardRemove())
        await state.set_state("phone")
    elif code == '1122':
        user = await commands.get_user(user_id)
        name = message.from_user.full_name
        phone = data.get("phone")
        await state.finish()
        user.name = name
        user.phone = phone
        user.is_active = True
        user.save()
        text = ''
        txt = ''
        if lang == 'uz':
            text = 'Xush kelibsiz👋.\nBuyurtma berish uchun Mahsulotlar tugmasini bosing!'
            txt = 'Ma\'lumotlar saqlandi'
        elif lang == 'ru':
            text = 'Добро пожаловать👋.\nНажмите кнопку Товары, чтобы заказать!'
            txt = 'Данные сохранены'
        elif lang == 'en':
            text = 'Welcome👋.\nClick the Products button to order!'
            txt = 'Data saved'
        menu = await menu_button(lang=await commands.get_lang(user_id))
        await message.answer(text=_(f"{txt}"), reply_markup=ReplyKeyboardRemove())
        await message.answer(_(f"{text}"), reply_markup=menu)
    else:
        text = ''
        if lang == 'uz':
            text = 'Telefon raqamingizga yuborilhan kodni kiriting'
        elif lang == 'ru':
            text = 'Введите код, отправленный на ваш номер телефона'
        elif lang == 'en':
            text = 'Enter the code sent to your phone number'
        menu = await contact_btn(lang=lang)
        await message.answer(text=_(f"{text}"), reply_markup=menu)
        await state.set_state('check_number')


@dp.callback_query_handler(text="about_us")
async def about_us_fun(call: types.CallbackQuery):
    about_us = await get_about_us()
    if about_us:
        await call.answer()
        photo = about_us.logo
        user = await get_user(call.from_user.id)
        await call.message.delete()
        markup = await about_us_btn(lang=await commands.get_lang(call.from_user.id))
        if user:
            if user.lang == "ru":
                await call.message.answer_photo(photo=photo, caption=about_us.description_ru, reply_markup=markup)
            else:
                await call.message.answer_photo(photo=photo, caption=about_us.description_en, reply_markup=markup)
    else:
        user_id = call.from_user.id
        text = ''
        lang = await get_lang(user_id)
        if lang == 'uz':
            text = 'Hozircha bo\'sh!'
        elif lang == 'ru':
            text = 'Пусто пока'
        elif lang == 'en':
            text = 'Nothing else'

        await call.answer(_(f"{text}"), show_alert=True)


@dp.callback_query_handler(text="back_about_us")
async def back_to_about_us(call: types.CallbackQuery):
    await call.answer()
    about_us = await get_about_us()
    photo = about_us.logo
    user = await get_user(call.from_user.id)
    await call.message.delete()
    markup = await about_us_btn(lang=await commands.get_lang(call.from_user.id))
    if user:
        if user.lang == "ru":
            await call.message.answer_photo(photo=photo, caption=about_us.description_ru, reply_markup=markup)
        elif user.lang == 'en':
            await call.message.answer_photo(photo=photo, caption=about_us.description_en, reply_markup=markup)
        else:
            await call.message.answer_photo(photo=photo, caption=about_us.description_uz, reply_markup=markup)
