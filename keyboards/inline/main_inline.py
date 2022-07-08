from loader import _
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.database import get_links

plus_minus_data = CallbackData("PS", "key", "purchase_id")


async def menu_button(lang):
    text = []
    if lang == 'en':
        text = ['Products', 'About us', 'Settings', 'Cart', 'Cashbacks', 'Our social pages', 'Suggestions and opinions',
                'Order history', 'Promotions']
    if lang == 'uz':
        text = ['Maxsulotlar', 'Biz xaqimizda', 'Sozlamalar', 'Savat', 'Keshbeklar', 'Ijtimoi sahifalarimiz',
                'Takliflar va fikrlar', 'Buyurtmalar tarixi', 'Aktsiyalar']
    if lang == 'ru':
        text = ['Продукты', 'О нас', 'Настройки', 'Корзина', 'Кешбеки', 'Наши страницы в социальных сетях',
                'Предложения и отзывы', 'История заказов', 'Акции']
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_(f"🛍 {text[0]}", locale=lang), callback_data="order_menu"),
            ],
            [
                InlineKeyboardButton(text=_(f"📑 {text[1]}", locale=lang), callback_data="about_us"),
            ],
            [
                InlineKeyboardButton(text=_(f"⚙️ {text[2]}", locale=lang), callback_data="settings")
            ],
            [
                InlineKeyboardButton(text=_(f"🧾️ {text[7]}", locale=lang), callback_data="history")
            ],
            [
                InlineKeyboardButton(text=_(f"🛒 {text[3]}", locale=lang), callback_data="cart")
            ],
            [
                InlineKeyboardButton(text=_(f"💰 {text[4]}", locale=lang), callback_data="cashback")
            ],
            [
                InlineKeyboardButton(text=_(f"🌐 {text[5]}", locale=lang), callback_data="messenger")
            ],
            [
                InlineKeyboardButton(text=_(f"🗒 {text[6]}", locale=lang), callback_data="offer_feedback")
            ],
            [
                InlineKeyboardButton(text=_(f"🅰️ {text[8]}💯", locale=lang), callback_data="aksiya")
            ]

        ]
    )
    return markup


async def languages_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="🇺🇿uz", callback_data="lang_uz"),
                InlineKeyboardButton(text="🇷🇺ru", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇺🇸en", callback_data="lang_en"),
            ],
        ]
    )
    return markup


async def contact_btn(lang):
    text = ''
    if lang == 'uz':
        text = '🔙 Orqaga'
    elif lang == 'en':
        text = '🔙 Back'
    elif lang == 'ru':
        text = '🔙 Назад'

    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text=f"{text}")
    keyboard.add(button_phone)

    return keyboard


async def main_cart_button(purchases, lang):
    markup = InlineKeyboardMarkup(row_width=3)
    for purchase in purchases:
        if purchase.product:
            item = purchase.product
        else:
            item = purchase.productA
        markup.insert(
            InlineKeyboardButton(text=f"➖", callback_data=plus_minus_data.new(key="minus", purchase_id=purchase.id)))
        if lang == "ru":
            markup.insert(InlineKeyboardButton(text=f"{item.name_ru}", callback_data="no_call"))
        if lang == "en":
            markup.insert(InlineKeyboardButton(text=f"{item.name}", callback_data="no_call"))
        if lang == "uz":
            markup.insert(InlineKeyboardButton(text=f"{item.name_uz}", callback_data="no_call"))
        markup.insert(
            InlineKeyboardButton(text=f"➕", callback_data=plus_minus_data.new(key="plus", purchase_id=purchase.id)))
    texts = []
    if lang == 'en':
        texts = ['🗑 Clear cart', '🧾 Confirm order', 'Order again']
    elif lang == 'ru':
        texts = ['🗑 Очистить', '🧾 Confirm order', 'Order again']
    markup.row(
        InlineKeyboardButton(text=_("🗑 Clear cart", locale=lang), callback_data="clear_cart"),
        InlineKeyboardButton(text=_("🧾 Confirm order", locale=lang), callback_data="confirm")
    )
    markup.row(InlineKeyboardButton(text=_("♻️ ", locale=lang), callback_data="back_to_menu_page"))
    return markup


async def confirm_end(lang):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("❌ Cancel", locale=lang), callback_data="cancel_end"),
                InlineKeyboardButton(text=_("✅ Confirm", locale=lang), callback_data="confirm_end"),
            ],
            [
                InlineKeyboardButton(text=_("◀️ Back"), callback_data="back_main"),
            ]

        ]
    )
    return markup


async def back_to_home(lang):
    text = ''
    if lang == 'uz':
        text = 'Orqaga'
    elif lang == 'en':
        text = 'Back'
    elif lang == 'ru':
        text = 'Назад'

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_(f"◀️ {text}", locale=lang), callback_data="back_home"),
            ]

        ]
    )
    return markup


async def cashback_keyboard(lang):
    text = []
    if lang == 'uz':
        text = ['Xaridni boshlash', 'Orqaga']
    elif lang == 'en':
        text = ['Start shopping', 'Back']
    elif lang == 'ru':
        text = ['Начать покупки', 'Назад']

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_(f"🛒 {text[0]}", locale=lang), callback_data="order_menu"),
            ],
            [
                InlineKeyboardButton(text=_(f"◀️ {text[1]}", locale=lang), callback_data="back_home"),
            ]

        ]
    )
    return markup


async def about_us_btn(lang):
    text = []
    if lang == 'uz':
        text = ['Tadbirlardan foto', 'Voqealardan video', 'Orqaga']
    elif lang == 'en':
        text = ['Photo from events', 'Video from events', 'Back']
    elif lang == 'ru':
        text = ['Фото с мероприятий', 'Видео с мероприятий',  'Назад']
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            # [
            #     InlineKeyboardButton(text=_("📷 Photo from events", locale=lang), callback_data="meeting_photos"),
            # ],
            # [
            #     InlineKeyboardButton(text=_("🎥 Video from events", locale=lang), callback_data="meeting_videos"),
            # ],
            [
                InlineKeyboardButton(text=_(f"◀️ {text[2]}", locale=lang), callback_data="back_home"),
            ]

        ]
    )
    return markup


pagination_call = CallbackData("paginator", "key", "page")
show_item = CallbackData("show_item", "item_id")


async def get_page_keyboard(max_pages: int, key, lang, page: int = 1):
    previous_page = page - 1
    previous_page_text = "⬅️"

    next_page = page + 1
    next_page_text = "➡️"

    markup = InlineKeyboardMarkup(row_width=2)
    if previous_page > 0:
        markup.insert(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(key=key, page=previous_page)
            )
        )

    if next_page <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(key=key, page=next_page)
            )
        )

    markup.row(
        InlineKeyboardButton(text=_("◀️ Back", locale=lang), callback_data="back_about_us"),
    )
    return markup


back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("◀️ Back"), callback_data="back_main"),
        ]
    ]
)


async def messenger_keyboards(lang):
    locs = await get_links()
    text = ''
    if lang == 'uz':
        text = 'Orqaga'
    elif lang == 'en':
        text = 'Back'
    elif lang == 'ru':
        text = 'Назад'

    markup = InlineKeyboardMarkup()
    if locs:
        for i in locs:
            markup.row(InlineKeyboardButton(text=f"{i.name}", url=f'{i.url}'))
        markup.row(InlineKeyboardButton(text=f"◀️{text}", callback_data='back_home'))
        return markup
    else:
        return None
