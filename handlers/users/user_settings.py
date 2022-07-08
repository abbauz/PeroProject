from typing import Union
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ParseMode, ReplyKeyboardRemove
from keyboards.inline.main_inline import menu_button, languages_markup, contact_btn, back_to_home, about_us_btn
from keyboards.inline.menu_button import menu_cd, categories_keyboard, items_keyboard, item_keyboard
from loader import dp, _, bot
from utils.db_api.database import get_item, get_category_by_name, get_user, get_lang
from keyboards.inline.setting_keyboards import settings_markup, back_settings
from utils.db_api import database as commands
import phonenumbers


@dp.callback_query_handler(text="settings", state='*')
async def show_certificate(call: types.CallbackQuery, state: FSMContext):
    texts = []
    await state.finish()
    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = await get_lang(user_id)
    if lang == 'uz':
        texts = ['Ismingiz', 'Telefon raqamingiz', 'Tanlamgan til', '🇺🇿uz']
    elif lang == 'en':
        texts = ['Your name', 'Your phone', 'Language', '🇺🇸en']
    elif lang == 'ru':
        texts = ['Ваше имя', 'Ваш телефон', 'Выбранный язык', '🇷🇺ru']

    text = f"\n👤 <b>{texts[0]}</b>: {user.name}\n\n" \
           f"📞 <b>{texts[1]}</b>: {user.phone}\n\n" \
           f"🖋 <b>{texts[2]}</b>: {texts[3]}\n\n"
    markup = await settings_markup(lang)
    await state.set_state('settings')
    await call.message.edit_text(text=text, reply_markup=markup, parse_mode=ParseMode.HTML)


@dp.callback_query_handler(text="change_language", state='*')
async def change_language_fun(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    markup = await languages_markup()
    await call.message.edit_text(
        "O'zingizga kerakli tilni tanlang!\n\nChoose your language!\n\nВыберите удобный Вам язык!.",
        reply_markup=markup)
    await state.set_state('settings')


@dp.callback_query_handler(state='settings', text_contains="lang")
async def change_lang_fun(call: types.CallbackQuery):
    await call.answer()
    lang = call.data[-2:]
    print(call.data[-2:])
    user = await get_user(call.from_user.id)
    user.lang = lang
    user.save()
    await call.message.delete()
    texts = []
    if lang == 'uz':
        texts = ['Ismingiz', 'Telefon raqamingiz', 'Tanlamgan til', '🇺🇿uz']
    elif lang == 'en':
        texts = ['Your name', 'Your phone', 'Language', '🇺🇸en']
    elif lang == 'ru':
        texts = ['Ваше имя', 'Ваш телефон', 'Выбранный язык', '🇷🇺ru']

    text = f"\n👤 <b>{texts[0]}</b>: {user.name}\n\n" \
           f"📞 <b>{texts[1]}</b>: {user.phone}\n\n" \
           f"🖋 <b>{texts[2]}</b>: {texts[3]}\n\n"
    markup = await settings_markup(lang)
    await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup, parse_mode=ParseMode.HTML)


@dp.callback_query_handler(state='settings', text="change_name")
async def change_language_fun(call: types.CallbackQuery, state: FSMContext):
    texts = ""
    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = await get_lang(user_id)
    markup = await back_settings(lang)
    if lang == 'uz':
        texts = "Ismingizni kiriting 👇"
    elif lang == 'en':
        texts = "Enter your name 👇"
    elif lang == 'ru':
        texts = "Введите ваше имя 👇"

    await call.message.edit_text(text=texts, reply_markup=markup)


@dp.message_handler(state="settings")
async def change_language_fun(message: types.Message, state: FSMContext):
    await state.finish()
    name = message.text
    user_id = message.from_user.id
    user = await get_user(user_id)
    user.name = name
    user.save()
    lang = user.lang
    texts = []
    if lang == 'uz':
        texts = ['Ismingiz', 'Telefon raqamingiz', 'Tanlamgan til', '🇺🇿uz']
    elif lang == 'en':
        texts = ['Your name', 'Your phone', 'Language', '🇺🇸en']
    elif lang == 'ru':
        texts = ['Ваше имя', 'Ваш телефон', 'Выбранный язык', '🇷🇺ru']

    text = f"\n👤 <b>{texts[0]}</b>: {user.name}\n\n" \
           f"📞 <b>{texts[1]}</b>: {user.phone}\n\n" \
           f"🖋 <b>{texts[2]}</b>: {texts[3]}\n\n"
    markup = await settings_markup(lang)
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup, parse_mode=ParseMode.HTML)


@dp.callback_query_handler(text="change_phone")
async def change_lang(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = user.lang
    text = ''
    if lang == 'uz':
        text = 'Telefon raqamingizni xalqaro formatda kiriting\nMasalan: +998901234567'
    elif lang == 'ru':
        text = 'Введите номер в международном формате\nНапример: +998901234567'
    elif lang == 'en':
        text = 'Enter the number in international format\nFor example: +998901234567'
    menu = await back_settings(lang=lang)
    await call.message.edit_text(text=_(f"{text}"), reply_markup=menu)
    await state.set_state("phone_update")


@dp.message_handler(state="phone_update")
async def get_confirm_secret_phone(message: types.Message, state: FSMContext):
    phone = message.text
    try:
        my_number = phonenumbers.parse(f"{phone}", "GB")
        if phonenumbers.is_valid_number(my_number):
            user_id = message.from_user.id
            user = await get_user(user_id)
            lang = user.lang
            text = ''
            if lang == 'uz':
                text = 'Telefon raqamingizga yuborilhan kodni kiriting'
            elif lang == 'ru':
                text = 'Введите код, отправленный на ваш номер телефона'
            elif lang == 'en':
                text = 'Enter the code sent to your phone number'
            await state.update_data(phone=phone)
            markup = await back_settings(lang)
            await bot.send_message(chat_id=message.from_user.id, text=_(f"{text}"), reply_markup=markup)
            await state.set_state('check_number_update')
        else:
            await message.answer(_("For example: +998901234567"))
            await state.set_state("phone_update")
    except Exception as exx:
        print(exx)
        await message.answer(_("Enter the number in international format\nFor example: +998901234567"))
        await state.set_state("phone_update")


@dp.message_handler(state='check_number_update')
async def check_numbers(message: types.Message, state: FSMContext):
    code = message.text
    user_id = message.from_user.id
    user = await commands.get_user(user_id)
    data = await state.get_data()
    lang = user.lang
    if code in ['🔙 Orqaga', '🔙 Back', '🔙 Назад']:
        text = ''
        if lang == 'uz':
            text = 'Telefon raqamingizni xalqaro formatda kiriting\nMasalan: +998901234567'
        elif lang == 'ru':
            text = 'Введите номер в международном формате\nНапример: +998901234567'
        elif lang == 'en':
            text = 'Enter the number in international format\nFor example: +998901234567'
        await message.answer(text=_(f"{text}"), reply_markup=ReplyKeyboardRemove())
        await state.set_state("phone_update")
    elif code == '1122':
        phone = data.get("phone")
        await state.finish()
        name = message.from_user.full_name
        user.phone = phone
        user.save()
        texts = []
        txt = ''
        if lang == 'uz':
            txt = 'Ma\'lumotlar saqlandi'
            texts = ['Ismingiz', 'Telefon raqamingiz', 'Tanlamgan til', '🇺🇿uz']
        elif lang == 'en':
            txt = 'Data saved'
            texts = ['Your name', 'Your phone', 'Language', '🇺🇸en']
        else:
            txt = 'Данные сохранены'
            texts = ['Ваше имя', 'Ваш телефон', 'Выбранный язык', '🇷🇺ru']

        text = f"\n👤 <b>{texts[0]}</b>: {user.name}\n\n" \
               f"📞 <b>{texts[1]}</b>: {user.phone}\n\n" \
               f"🖋 <b>{texts[2]}</b>: {texts[3]}\n\n"
        markup = await settings_markup(lang)
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup, parse_mode=ParseMode.HTML)
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
        await state.set_state('check_number_update')


@dp.callback_query_handler(text="bact_settings", state='*')
async def change_lang(call: types.CallbackQuery, state: FSMContext):
    texts = []
    user_id = call.from_user.id
    await state.finish()
    user = await get_user(user_id)
    lang = await get_lang(user_id)
    if lang == 'uz':
        texts = ['Ismingiz', 'Telefon raqamingiz', 'Tanlamgan til', '🇺🇿uz']
    elif lang == 'en':
        texts = ['Your name', 'Your phone', 'Language', '🇺🇸en']
    elif lang == 'ru':
        texts = ['Ваше имя', 'Ваш телефон', 'Выбранный язык', '🇷🇺ru']

    text = f"\n👤 <b>{texts[0]}</b>: {user.name}\n\n" \
           f"📞 <b>{texts[1]}</b>: {user.phone}\n\n" \
           f"🖋 <b>{texts[2]}</b>: {texts[3]}\n\n"
    markup = await settings_markup(lang)
    await call.message.edit_text(text=text, reply_markup=markup, parse_mode=ParseMode.HTML)
