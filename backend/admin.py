from django.contrib import admin
from .models import User, Product, CartModel, Order, ProductCategory, Location, Cashback, ProductAksiya
from django.contrib.auth.models import Group

admin.site.unregister(Group)


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Product",
         {'fields': ["name_uz", "name", "name_ru", "price", "description_uz", "description_ru", "description_en",
                     "photo", 'image']}),
        ("Category/SubCategory", {"fields": ["category_name"]}),
    ]
    list_display = ("name_uz", "price")
    list_display_links = ("name_uz", "price")


admin.site.register(Product, ProductAdmin)


class AktsiyaAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Product",
         {'fields': ["name_uz", "name", "name_ru", "price", "description_uz", "description_ru", "description_en",
                     "photo", 'begin_aksiya', 'count_a', 'image']}),
        ("Category/SubCategory", {"fields": ["category_name"]}),
    ]
    list_display = ("name_uz", "price")
    list_display_links = ("name_uz", "price")


admin.site.register(ProductAksiya, AktsiyaAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "name", "phone", "is_admin", "is_active")
    list_display_links = ("user_id", "name")


admin.site.register(User, UserAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name_uz", "category_name_ru")
    list_display_links = ("category_name_uz", "category_name_ru")


admin.site.register(ProductCategory, ProductCategoryAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "amount", "total", "is_success")
    list_display_links = ("product", "user")


admin.site.register(CartModel, CartAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "phone", "total", "is_success")
    list_display_links = ("user", "name")


admin.site.register(Order, OrderAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "user_id")
    list_display_links = ("name", "user_id")


admin.site.register(Location, LocationAdmin)


class CashbackAdmin(admin.ModelAdmin):
    list_display = ("user_id", "begin_date", 'end_date')
    list_display_links = ("end_date", "begin_date", "user_id")


admin.site.register(Cashback, CashbackAdmin)
