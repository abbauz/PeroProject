from datetime import datetime, timedelta
from typing import List, Any
from asgiref.sync import sync_to_async
from backend.models import User, Product, ProductCategory, CartModel, Location, Cashback, Order, ProductAksiya
from about_us.models import VideoModel, PhotoModel, About, Messenger


@sync_to_async
def add_user(user_id, name, phone, lang):
    try:
        user, created = User.objects.get_or_create(user_id=int(user_id), name=name, phone=phone, lang=lang)
        user.save()
        print(user)
        return User
    except Exception as err:
        print(err)


@sync_to_async
def get_user(user_id: int):
    try:
        user = User.objects.filter(user_id=user_id).first()
        return user
    except:
        return None


@sync_to_async
def get_users() -> List[User]:
    try:
        users = User.objects.filter(is_admin="user").all()
        return users
    except Exception as err:
        print("ERROR ->>>>", err)
        return None


@sync_to_async
def get_admins():
    try:
        admins = User.objects.filter(is_admin="admin")
        return admins
    except:
        return None


@sync_to_async
def set_lang(lang, user_id):
    user = User.objects.filter(user_id=user_id).first()
    user.lang = lang
    user.save()


@sync_to_async
def get_lang(user_id):
    try:
        user = User.objects.filter(user_id=user_id).first()
        if user.lang:
            return user.lang
        else:
            return "uz"
    except:
        "uz"


@sync_to_async
def get_categories() -> List[Product]:
    items = Product.objects.all().distinct("category_name")
    return items


@sync_to_async
def get_aksiya_categories() -> List[ProductAksiya]:
    items = ProductAksiya.objects.all().distinct("category_name")
    return items


@sync_to_async
def get_category_by_name(category_name) -> List[ProductCategory]:
    category = ProductCategory.objects.get(category_name=category_name)
    return category


@sync_to_async
def get_category_by_id(category_name) -> List[ProductCategory]:
    category = ProductCategory.objects.get(id=category_name)
    return category


@sync_to_async
def get_items(category) -> List[Product]:
    return Product.objects.all().filter(category_code=category).all()


@sync_to_async
def get_aksiya_items(category) -> List[ProductAksiya]:
    return ProductAksiya.objects.all().filter(category_name__id=category).all()


@sync_to_async
def get_item(item_id) -> Product:
    item = Product.objects.filter(id=int(item_id)).first()
    return item


@sync_to_async
def get_aksiya_item(item_id) -> ProductAksiya:
    item = ProductAksiya.objects.filter(id=int(item_id)).first()
    return item


@sync_to_async
def get_purchase(user) -> List[CartModel]:
    try:
        purchase = CartModel.objects.filter(user=user, is_success=False).order_by("-id")
        return purchase
    except:
        pass


@sync_to_async
def get_purchase_by_id(purchase_id):
    try:
        purchase = CartModel.objects.get(id=purchase_id)
        return purchase
    except:
        pass


@sync_to_async
def delete_purchase(purchase_id):
    purchase = CartModel.objects.get(id=purchase_id)
    purchase.delete()


@sync_to_async
def update_purchase(buyer):
    purchase = False
    purchases = CartModel.objects.filter(user=buyer).all()
    for purchase in purchases:
        purchase.is_success = True
        purchase.save()

    return purchase


@sync_to_async
def get_about_us():
    try:
        about_us = About.objects.all().order_by("-id")[0]
        return about_us
    except Exception as err:
        print(err)
        return None
        pass


#
#
# @sync_to_async
# def get_faq():
#     try:
#         faq = FaqModel.objects.all().order_by("-id")[0]
#         return faq
#     except Exception as err:
#         print(err)
#         return None
#         pass

#
# @sync_to_async
# def get_price_list():
#     try:
#         price_list = PriceListModel.objects.all().order_by("-id")[0]
#         return price_list
#     except Exception as err:
#         print(err)
#         return None
#         pass
#

@sync_to_async
def get_videos():
    try:
        videos = VideoModel.objects.all().order_by("-id")
        return videos
    except:
        return None


@sync_to_async
def get_photos():
    try:
        photos = PhotoModel.objects.all().order_by("-id")
        return photos
    except:
        return None


#
# @sync_to_async
# def get_certificate():
#     try:
#         certificates = SerificateModel.objects.all().order_by("-id")
#         return certificates
#     except:
#         return None


@sync_to_async
def get_address(user_id):
    try:
        locs = Location.objects.filter(user_id=user_id).all()
        return locs
    except:
        return None


@sync_to_async
def get_address_by_id(id):
    try:
        locs = Location.objects.filter(id=id).first()
        return locs
    except:
        return None


@sync_to_async
def add_address(longitude, latitude, name, user_id):
    try:
        long, created = Location.objects.get_or_create(longitude=longitude, latitude=latitude,
                                                       user_id=user_id, name=name)
        long.save()
        return long
    except:
        return None


@sync_to_async
def add_cash(user_id):
    try:
        end_date = datetime.now() + timedelta(days=30)
        cash = Cashback(user_id=user_id, end_date=end_date, count=1).save()
        return cash
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_cash(user_id):
    try:
        cashback = []
        cash = Cashback.objects.filter(user_id=user_id).all()
        now = datetime.today().date()
        for i in cash:
            if i.begin_date <= now <= i.end_date:
                cashback.append(i)
            else:
                i.delete()
        return cashback
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_cashback(user_id):
    try:
        cashback = []
        cash = Cashback.objects.filter(user_id=user_id).all()
        now = datetime.today().date()
        for i in cash:
            if i.begin_date <= now <= i.end_date:
                cashback.append(i)
            else:
                i.delete()
        return int(len(cashback))
    except Exception as exx:
        print(exx)
        return 0


@sync_to_async
def get_links() -> List[Messenger]:
    try:
        return Messenger.objects.all()
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_user_orders(user_id):
    try:
        user = User.objects.filter(user_id=user_id).first()
        orders = Order.objects.filter(user=user).all()
        return orders
    except Exception as ex:
        print(ex)
        return None
