from typing import Union
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ParseMode, ReplyKeyboardRemove
from loader import dp, _, bot
from utils.db_api.database import get_user, get_lang, get_user_orders
from keyboards.inline.main_inline import back_to_home


@dp.callback_query_handler(text='history', state='*')
async def get_orders(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.from_user.id
    lang = await get_lang(user_id)
    text = ''
    i = 1
    offers = await get_user_orders(user_id)
    for offer in offers:
        text += f"{offer}) {offer.purchases}\n" \
                f"      Total: {offer.total} uzs\n\n"
        i += 1
    markup = await back_to_home(lang)
    await state.set_state('offers')
    await call.message.edit_text(text=text, reply_markup=markup, parse_mode=ParseMode.HTML)


