from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.main_inline import back_button, main_cart_button
from .cart import cart_fun, confirm_fun, address_name_fun
from loader import _
from utils.db_api.database import *


@dp.callback_query_handler(text="back_main", state="name_cart")
async def back_cart(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    await cart_fun(call)


@dp.callback_query_handler(text="back_main", state="phone_cart")
async def back_name(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer(_("Enter your name..."), reply_markup=back_button)
    await state.set_state("name_cart")


@dp.callback_query_handler(text="back_main", state="email_cart")
async def back_phone(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer(_("Enter the number in international format\nFor example: +998901234567"),
                              reply_markup=back_button)
    await state.set_state("phone_cart")


@dp.callback_query_handler(text="back_main", state="company_name")
async def back_email(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer(_("Enter your email..."), reply_markup=back_button)
    await state.set_state("email_cart")


@dp.callback_query_handler(text="back_main", state="address")
async def back_company(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer(_("Enter your company name..."), reply_markup=back_button)
    await state.set_state("company_name")


@dp.callback_query_handler(text="back_main", state="confirm_state")
async def back_address(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user = await get_user(user_id)
    await state.finish()
    purchases = await get_purchase(user)
    total = 0
    final_total = 0
    text = ""
    if purchases:
        await call.answer()
        i = 1
        for purchase in purchases:
            item = purchase.product
            if user.lang == "ru":
                item_name = item.name_ru
                category_name = item.category_name_ru
            else:
                item_name = item.name
                category_name = item.category_name
            amount = purchase.amount
            price = purchase.product.price
            total = int(amount) * price
            text += f'<b>{i}) {category_name}\n   └{item_name}</b> {amount} x {price} = {total} $\n\n'
            i += 1
            final_total += total
        markup = await main_cart_button(purchases, lang=await get_lang(user_id))
        text += "Total: " + str(final_total) + " $"
        await call.message.edit_text(text=text, reply_markup=markup)
