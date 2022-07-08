from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ParseMode
from keyboards.inline.main_inline import messenger_keyboards
from utils.db_api.database import get_user, get_lang, get_links


@dp.callback_query_handler(text='messenger', state='*')
async def messengers(call: CallbackQuery, state: FSMContext):
    texts = ''
    await state.finish()
    user_id = call.from_user.id
    user = await get_user(user_id)
    lang = await get_lang(user_id)
    links = await get_links()

    if lang == 'uz':
        texts = 'Ijtimoi sahifalarimiz'
    elif lang == 'en':
        texts = 'Our social pages'
    elif lang == 'ru':
        texts = 'Наши страницы в социальных сетях'
    text = f"<b>{texts}</b>\n\n"
    n = 1
    for link in links:
        text += f"<b>{link.name}</b> ➡️ {link.url}\n\n"
    markup = await messenger_keyboards(lang)
    await call.message.edit_text(text=text, reply_markup=markup, parse_mode=ParseMode.HTML)
