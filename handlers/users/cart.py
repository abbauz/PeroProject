from aiogram.types import ReplyKeyboardRemove

from backend.models import Order
from geopy.geocoders import Nominatim
from handlers.users.menu_handler import list_categories
from keyboards.inline.main_inline import main_cart_button, plus_minus_data, confirm_end, back_button
from keyboards.inline.menu_button import categories_keyboard
from loader import dp, bot, _
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.db_api.database import get_user, get_purchase, get_purchase_by_id, delete_purchase, update_purchase, \
    get_lang, get_address, add_address, add_cash, get_cashback
from keyboards.inline.buy_keyboards import *
from utils.date_time_format import df


@dp.callback_query_handler(text="cart", state='*')
async def cart_fun(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user = await get_user(user_id)
    await state.finish()
    purchases = await get_purchase(user)
    total = 0
    cash = await get_cashback(user_id)
    cash_total = 0
    final_total = 0
    text = ""
    if purchases:
        await call.answer()
        i = 1
        for purchase in purchases:
            if purchase.product:
                item = purchase.product
                price = purchase.product.price
            else:
                item = purchase.productA
                price = purchase.productA.price
            if user.lang == "ru":
                item_name = item.name_ru
                category_name = item.category_name_ru
            else:
                item_name = item.name
                category_name = item.category_name
            amount = purchase.amount
            total = int(purchase.total)
            text += f'<b>{i}) {category_name}\n   └{item_name}</b> {amount} x {price} = {total} $\n\n'
            i += 1
            final_total += total
            cash_total = final_total - final_total * cash/100
        markup = await main_cart_button(purchases, lang=await get_lang(user_id))
        text += "Total: " + str(final_total) + " uzs"
        text += f"Cashback = {cash} % " + f" ➡️{cash_total} uzs"
        await call.message.edit_text(text=text, reply_markup=markup)
    else:
        await call.answer(_("You haven't products in your cart 🤷‍♂️"), show_alert=True)


@dp.callback_query_handler(plus_minus_data.filter())
async def plus_minus_fun(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    purchase_id = callback_data.get("purchase_id")
    key = callback_data.get("key")
    purchase = await get_purchase_by_id(purchase_id)
    user_id = call.from_user.id
    user = await get_user(user_id)
    purchases = await get_purchase(user)
    cash = await get_cashback(user_id)
    total = 0
    cash_total = 0
    final_total = 0
    text = ""
    if key == "minus" and purchase.amount == 1:
        await delete_purchase(int(purchase_id))

    if key == "minus" and purchase.amount > 1:
        purchase.amount -= 1
        purchase.save()

    if key == "plus":
        purchase.amount += 1
        purchase.save()
    i = 1
    for purchase in purchases:
        if purchase.product:
            item = purchase.product
            price = purchase.product.price
        else:
            item = purchase.productA
            price = purchase.productA.price
        if user.lang == "ru":
            item_name = item.name_ru
            category_name = item.category_name_ru
        else:
            item_name = item.name
            category_name = item.category_name
        amount = purchase.amount
        total = int(purchase.total)
        text += f'<b>{i}) {category_name}\n   └{item_name}</b> {amount} x {price} = {total} $\n\n'
        i += 1
        final_total += total
    cash_total = final_total - final_total * cash / 100
    markup = await main_cart_button(purchases, lang=await get_lang(user_id))
    text += "Total: " + str(final_total) + " uzs"
    text += f"Cashback = {cash} % " + f" ➡️{cash_total} uzs"
    await call.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(text="back_to_menu_page")
async def back_to_menu_page(call: types.CallbackQuery):
    await call.answer()
    await list_categories(call.message)


# @dp.message_handler(state='get_location')
# async def confirm_fun(call: types.CallbackQuery, state: FSMContext):


@dp.callback_query_handler(text="confirm")
async def confirm_fun(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user = await get_user(call.from_user.id)
    lang = user.lang
    text = []
    if lang == 'uz':
        text = ['To\'lov turini tanlang']
    elif lang == 'ru':
        text = ['Выберите тип оплаты']
    elif lang == 'en':
        text = ['Select the payment type']
    markup = await money_type(lang)
    await call.message.delete()
    await call.message.answer(_(f"{text[0]}"), reply_markup=markup)
    await state.set_state("get_type")


@dp.callback_query_handler(state="get_type")
async def confirm_fun(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    type_pay = call.data
    await state.update_data(type_pay=type_pay)
    if type_pay == 'offline':
        user = await get_user(call.from_user.id)
        lang = user.lang
        text = []
        if lang == 'uz':
            text = ['Yetkazish manzilini jo\'nating']
        elif lang == 'ru':
            text = ['Отправьте адрес доставки']
        elif lang == 'en':
            text = ['Please send your delivery address']
        markup = await location_send(lang)
        await call.message.delete()
        await bot.send_message(text=text[0], chat_id=call.from_user.id, reply_markup=markup)
        await state.set_state('get_address')
    elif type_pay == 'online':
        user = await get_user(call.from_user.id)
        lang = user.lang
        text = []
        if lang == 'uz':
            text = ['To\'lov turini tanlang']
        elif lang == 'ru':
            text = ['Выберите тип оплаты']
        elif lang == 'en':
            text = ['Select the payment type']
        markup = await pay_type(lang)
        await call.message.delete()
        await call.message.answer(_(f"{text[0]}"), reply_markup=markup)
        await state.set_state("card_type")


@dp.callback_query_handler(state="card_type")
async def confirm_fun(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user = await get_user(call.from_user.id)
    lang = user.lang
    text = []
    if lang == 'uz':
        text = ['Yetkazish manzilini jo\'nating']
    elif lang == 'ru':
        text = ['Отправьте адрес доставки']
    elif lang == 'en':
        text = ['Please send your delivery address']
    markup = await location_send(lang)
    await state.update_data(card_type=call.data)
    await call.message.delete()
    await call.message.answer(_(f"{text[0]} 👇"), reply_markup=markup)
    await state.set_state("get_address")


@dp.message_handler(content_types=types.ContentType.LOCATION, state='get_address')
async def get_location_address(message: types.Message, state: FSMContext):
    location = message.location
    geolocator = Nominatim(user_agent="geoapiExercises")
    Latitude = str(location.latitude)
    Longitude = str(location.longitude)
    location = geolocator.geocode(Latitude + "," + Longitude)
    data = location.raw.get('display_name')
    data = data.split(',')
    name = f"{data[0]} {data[1]} {data[2]}"
    user = await get_user(message.from_user.id)
    lang = user.lang
    text = []
    if lang == 'uz':
        text = 'Manzilni tasdiqlaysizmi?'
    elif lang == 'ru':
        text = 'Вы подтверждаете адрес?'
    elif lang == 'en':
        text = 'Do you confirm the location?'
    await state.update_data(latitude=Latitude, longitude=Longitude, name=name,
                            display_name=location.raw.get('display_name'))
    await message.answer(text=location.raw.get('display_name'), reply_markup=ReplyKeyboardRemove())
    markup = await confirm_address(lang)
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
    await state.set_state('confirm_address')


@dp.message_handler(content_types=types.ContentType.TEXT, state='get_address')
async def get_loc(message: types.Message, state: FSMContext):
    command = message.text
    if command in ['🔂 Oldingi manzillar', '🔂 Предыдущие адреса', '🔂 Previous addresses']:
        locations = await get_address(message.from_user.id)
        if locations:
            user = await get_user(message.from_user.id)
            lang = user.lang
            text = []
            if lang == 'uz':
                text = ['Kerakli mazilni tanlang', 'Manzillar']
            elif lang == 'ru':
                text = ['Выберите нужное место', 'Адреса']
            elif lang == 'en':
                text = ['Choose the desired mazil', 'Addresses']
            markup = await location_keys(user_id=message.from_user.id, lang=lang)
            await message.answer(text=text[1], reply_markup=ReplyKeyboardRemove())
            await bot.send_message(text=text[0], chat_id=message.from_user.id, reply_markup=markup)
            await state.set_state('get_location')
        else:
            user = await get_user(message.from_user.id)
            lang = user.lang
            text = []
            if lang == 'uz':
                text = 'Manzillar ro\'yxati bo\'sh'
            elif lang == 'ru':
                text = 'Список адресов пустой'
            elif lang == 'en':
                text = 'The address list is empty'
            await message.answer(text)


@dp.callback_query_handler(text_contains="loc", state='get_location')
async def get_locat(call: types.CallbackQuery, state: FSMContext):
    loc_id = call.data.split('_')
    loc_id = loc_id[1]
    location = await get_address_by_id(loc_id)
    geolocator = Nominatim(user_agent="geoapiExercises")
    Latitude = str(location.latitude)
    Longitude = str(location.longitude)
    location = geolocator.geocode(Latitude + "," + Longitude)
    data = location.raw.get('display_name')
    data = data.split(',')
    name = f"{data[0]} {data[1]} {data[2]}"
    user = await get_user(call.from_user.id)
    lang = user.lang
    text = []
    if lang == 'uz':
        text = 'Manzilni tasdiqlaysizmi?'
    elif lang == 'ru':
        text = 'Вы подтверждаете адрес?'
    elif lang == 'en':
        text = 'Do you confirm the location?'
    await call.message.edit_text(text=location.raw.get('display_name'))
    await state.update_data(latitude=Latitude, longitude=Longitude, name=name,
                            display_name=location.raw.get('display_name'))
    markup = await confirm_address(lang)
    await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup)
    await state.set_state('confirm_address')


@dp.callback_query_handler(text='back_to_address', state="*")
async def CancelSend(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user = await get_user(call.from_user.id)
    lang = user.lang
    text = []
    if lang == 'uz':
        text = ['Yetkazish manzilini jo\'nating']
    elif lang == 'ru':
        text = ['Отправьте адрес доставки']
    elif lang == 'en':
        text = ['Please send your delivery address']
    markup = await location_send(lang)
    await call.message.delete()
    await call.message.answer(_(f"{text[0]} 👇"), reply_markup=markup)
    await state.set_state("get_address")


@dp.callback_query_handler(text='cancel', state="confirm_address")
async def reSendAddress(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user = await get_user(call.from_user.id)
    lang = user.lang
    text = []
    if lang == 'uz':
        text = ['Yetkazish manzilini jo\'nating']
    elif lang == 'ru':
        text = ['Отправьте адрес доставки']
    elif lang == 'en':
        text = ['Please send your delivery address']
    markup = await location_send(lang)
    await call.message.delete()
    await call.message.answer(_(f"{text[0]} 👇"), reply_markup=markup)
    await state.set_state("get_address")


@dp.callback_query_handler(text='confirm', state="confirm_address")
async def address_name_fun(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = await get_user(call.from_user.id)
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    loc_name = data.get('name')
    address = data.get('display_name')
    name = user.name
    cash = await get_cashback(call.from_user.id)
    cash_total = 0
    await add_address(latitude=latitude, longitude=longitude, user_id=call.from_user.id, name=loc_name)
    phone = user.phone
    purchases = await get_purchase(user)
    text = _(
        "<b>Name:</b> {}\n<b>Phone:</b> {}\n<b>Address:</b> {}\n\n").format(
        name, phone, address)
    final_total = 0
    total = 0
    i = 1
    for purchase in purchases:
        category_name = ''
        item_name = ''
        if purchase.product:
            item = purchase.product
            price = purchase.product.price
        else:
            item = purchase.productA
            price = purchase.productA.price
        if user.lang == "ru":
            item_name = item.name_ru
            category_name = item.category_name_ru
        elif user.lang == 'en':
            item_name = item.name
            category_name = item.category_name
        elif user.lang == 'en':
            item_name = item.name_uz
            category_name = item.category_name.uz
        amount = purchase.amount
        total = purchase.total
        text += '<b>{}) {}\n   └{}</b> {} x {} = {} $\n\n'.format(
            i, category_name, item_name, amount, price, total
        )
        i += 1
        final_total += total
    cash_total = final_total - final_total * cash / 100
    text += "Total: " + str(final_total) + " uzs"
    text += f"Cashback = {cash} % " + f" ➡️{cash_total} uzs"
    await state.update_data(text=text, name=name, phone=phone, final_total=final_total, address=address,
                            cash_total=cash_total)
    markup = await confirm_end(lang=await get_lang(call.from_user.id))
    await call.message.edit_text(text=text, reply_markup=markup)
    await state.set_state("confirm_state")


@dp.callback_query_handler(text="confirm_end", state="confirm_state")
async def confirm_end_fun(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    type_pay = data.get('type_pay')
    text = data.get("text")
    name = data.get("name")
    phone = data.get("phone")
    address = data.get("address")
    final_total = data.get("final_total")
    cash_total = data.get("cash_total")
    card_type = data.get('card_type')
    user = await get_user(call.from_user.id)
    purchases = await get_purchase(user)
    purchase_text = ""
    i = 1
    prices = []
    desc = []
    for purchase in purchases:
        if purchase.product:
            item = purchase.product
            price = purchase.product.price
        else:
            item = purchase.productA
            price = purchase.productA.price
        if user.lang == "ru":
            item_name = item.name_ru
            desc = ["Платеж за покупку", "Вы должны оплатить 20% от общей суммы", "Требуемая сумма"]
        elif user.lang == "uz":
            desc = ["Xarid uchun to'lov", "Xo'o'sh", "Kerakli summa"]
            item_name = item.name_uz
        else:
            desc = ["Payment for purchase", "Жами сумманинг 20% ни тўлашингиз керак", "The required amount"]
            item_name = item.name
        amount = purchase.amount
        purchase_text += f'{i}) {item_name} {amount}\n'
        i += 1
    if type_pay == 'offline':
        try:
            order = Order()
            order.user = user
            order.name = name
            order.phone = phone
            order.purchases = purchase_text
            order.address = address
            order.total = cash_total
            order.is_success = False
            order.save()
            await update_purchase(user)
            date_time = await df()
            if final_total >= 200000:
                await add_cash(user_id=call.from_user.id)
            await bot.send_message(chat_id="-1001690881154",
                                   text=f"# {date_time}\n" + _("<b>Order ID: {}\n</b>").format(order.id) + text)
            await call.message.edit_reply_markup()
            await call.answer(_("Your order has been accepted."), show_alert=True)
            await state.finish()
            markup = await categories_keyboard(lang=await get_lang(call.from_user.id))
            await call.message.answer(_("Select one of the categories👇"), reply_markup=markup)
        except Exception as err:
            print(err)
            pass
    else:
        photo = ''
        token = ''
        if card_type == 'click':
            photo = 'https://click.uz/click/images/clickog.png'
            token = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'
        else:
            photo = 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fcdn.paycom.uz%2Fdocumentation_assets' \
                    '%2Fpayme_01.png&imgrefurl=https%3A%2F%2Fbusiness.help.paycom.uz%2Fru%2Fresursy&tbnid' \
                    '=bj2LIcsqagtFPM&vet=12ahUKEwjcuPDJnaL4AhWJuIsKHeH5AN8QMygCegUIARC6AQ..i&docid=4O8uWJGbCn5UUM' \
                    '&w=1080&h=314&q=payme&ved=2ahUKEwjcuPDJnaL4AhWJuIsKHeH5AN8QMygCegUIARC6AQ '
            token = '371317599:TEST:1654841947981'
        prices.append(
            types.LabeledPrice(label=f"{desc[2]}", amount=int(cash_total) * 100))
        await call.message.delete()
        await bot.send_invoice(chat_id=call.from_user.id, title=f'{desc[0]}',
                               description=f' \n{desc[1]}',
                               provider_token=token,
                               currency='UZS',
                               photo_url=photo,
                               photo_height=512,  # !=0/None or picture won't be shown
                               photo_width=512,
                               photo_size=512,
                               prices=prices,
                               start_parameter='hz-wto-tut',
                               payload="Payload"
                               )


@dp.pre_checkout_query_handler(lambda query: True, state='confirm_state')
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentTypes.SUCCESSFUL_PAYMENT, state="confirm_state")
async def got_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    type_pay = data.get('type_pay')
    print("Qaniii")
    text = data.get("text")
    name = data.get("name")
    phone = data.get("phone")
    address = data.get("address")
    print(address)
    final_total = data.get("final_total")
    cash_total = data.get("cash_total")
    card_type = data.get('card_type')
    user = await get_user(message.from_user.id)
    purchases = await get_purchase(user)
    purchase_text = ""
    i = 1
    for purchase in purchases:
        if purchase.product:
            item = purchase.product
            price = purchase.product.price
        else:
            item = purchase.productA
            price = purchase.productA.price
        if user.lang == "ru":
            item_name = item.name_ru
            desc = ["Платеж за покупку", "Вы должны оплатить 20% от общей суммы", "Требуемая сумма"]
        elif user.lang == "uz":
            desc = ["Xarid uchun to'lov", "Xo'o'sh", "Kerakli summa"]
            item_name = item.name_uz
        else:
            desc = ["Payment for purchase", "Жами сумманинг 20% ни тўлашингиз керак", "The required amount"]
            item_name = item.name
        amount = purchase.amount
        purchase_text += f'{i}) {item_name} x {amount}\n'
        i += 1
    try:
        order = Order()
        order.user = user
        order.name = name
        order.phone = phone
        order.purchases = purchase_text
        order.address = address
        order.total = cash_total
        order.is_success = False
        order.save()
        await update_purchase(user)
        date_time = await df()
        if final_total >= 200000:
            await add_cash(user_id=message.from_user.id)
        await bot.send_message(chat_id="-1001690881154",
                               text=f"# {date_time}\n" + _("<b>Order ID: {}\n</b>").format(order.id) + text)
        await message.answer(_("Your order has been accepted."))
        await state.finish()
        markup = await categories_keyboard(lang=await get_lang(message.from_user.id))
        await message.answer(_("Select one of the categories👇"), reply_markup=markup)
    except Exception as err:
        print(err)
        pass


@dp.callback_query_handler(text="cancel_end", state="confirm_state")
async def cancel_end_fun(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(_("Your order was canceled.But not deleted."), show_alert=True)
    await call.message.delete()
    user = await get_user(call.from_user.id)
    purchases = await get_purchase(user)
    category_name = ''
    cash = await get_cashback(call.from_user.id)
    item_name = ''
    total = 0
    final_total = 0
    text = ""
    texts = []
    if purchases:
        await call.answer()
        for purchase in purchases:
            if purchase.product:
                item = purchase.product
                price = purchase.product.price
            else:
                item = purchase.productA
                price = purchase.productA.price
            if user.lang == "ru":
                item_name = item.name_ru
                category_name = item.category_name_ru
                texts = ['В вашей корзине нет товаров 🤷‍♂️']
            elif user.lang == 'en':
                item_name = item.name
                texts = ['You haven\'t products in your cart 🤷‍♂️']
                category_name = item.category_name
            elif user.lang == 'uz':
                texts = ['Savatingizda mahsulot yoʻq 🤷‍♂️']
                item_name = item.name_uz
                category_name = item.category_name_uz
            amount = purchase.amount
            total = purchase.total
            text += f'<b>{category_name}\n   └{item_name}</b> {amount} x {price} = {total} $\n\n'
            final_total += total
        cash_total = final_total - final_total * cash / 100
        markup = await main_cart_button(purchases, lang=await get_lang(user.id))
        text += "Total: " + str(final_total) + " uzs"
        text += f"Cashback = {cash} % " + f" ➡️{cash_total} uzs"
        await call.message.answer(text=text, reply_markup=markup)
    else:
        await call.answer(_(f"{texts[0]}"), show_alert=True)


@dp.callback_query_handler(text="clear_cart")
async def clear_cart_fun(call: types.CallbackQuery):
    user = await get_user(call.from_user.id)
    lang = user.lang
    text = []
    if lang == 'uz':
        text = ['Buyurtmangiz oʻchirildi']
    elif lang == 'ru':
        text = ['Ваш заказ удален']
    elif lang == 'en':
        text = ['Your order deleted']
    purchases = await get_purchase(user)
    for purchase in purchases:
        await delete_purchase(purchase.id)
    await call.answer(_(""), show_alert=True)
    await list_categories(call.message)
