from django.db import models
from django.db.models.signals import pre_save


class User(models.Model):
    USER_TYPE_CHOICES = (
        ("user", "USER"),
        ("admin", "ADMIN"),
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "1.Users"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(verbose_name="ID", unique=True, default=1)
    lang = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=300, verbose_name="Name")
    phone = models.CharField(max_length=300, verbose_name="Phone", blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.CharField(verbose_name="User Type", max_length=300,
                                choices=USER_TYPE_CHOICES, default="user", blank=True, null=True)

    def __str__(self):
        return f"{self.user_id}"


class ProductCategory(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "2.Categories"

    id = models.AutoField(primary_key=True)
    category_name = models.CharField(verbose_name="Category name En", max_length=300)
    category_name_ru = models.CharField(verbose_name="Category name Ru", max_length=300, blank=True, null=True)
    category_name_uz = models.CharField(verbose_name="Category name Uz", max_length=300, blank=True, null=True)
    category_photo = models.CharField(max_length=1000, verbose_name="Category photo", blank=True, null=True)
    image = models.ImageField(null=True, verbose_name="Category Image")

    def __str__(self):
        return self.category_name


class Product(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "3.Products"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Product name En", max_length=200)
    name_ru = models.CharField(verbose_name="Product name Ru", max_length=200, default="S")
    name_uz = models.CharField(verbose_name="Product name Uz", max_length=200, default="S")
    price = models.DecimalField(verbose_name="Price", decimal_places=2, max_digits=20)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    description_ru = models.TextField(verbose_name="Description Ru", blank=True, null=True)
    description_en = models.TextField(verbose_name="Description En", blank=True, null=True)
    description_uz = models.TextField(verbose_name="Description Uz", blank=True, null=True)
    photo = models.CharField(max_length=1000, verbose_name="Photo", null=True, blank=True)
    image = models.ImageField(null=True, verbose_name="Image")

    category_name = models.ForeignKey(ProductCategory, verbose_name="Category En", on_delete=models.CASCADE)
    category_name_ru = models.CharField(max_length=300, verbose_name="Category Ru", blank=True, null=True)
    category_name_uz = models.CharField(max_length=300, verbose_name="Category Ru", blank=True, null=True)
    category_code = models.CharField(verbose_name="Unnecassary category-code", max_length=300, blank=True)

    def __str__(self):
        return f"{self.name}"


class ProductAksiya(models.Model):
    class Meta:
        verbose_name = "Product Aktsiya"
        verbose_name_plural = "4.Products Aktsiya"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Product name En", max_length=200)
    name_ru = models.CharField(verbose_name="Product name Ru", max_length=200, default="S")
    name_uz = models.CharField(verbose_name="Product name Uz", max_length=200, default="S")
    price = models.DecimalField(verbose_name="Price", decimal_places=2, max_digits=20)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    description_ru = models.TextField(verbose_name="Description Ru", blank=True, null=True)
    description_en = models.TextField(verbose_name="Description En", blank=True, null=True)
    description_uz = models.TextField(verbose_name="Description Uz", blank=True, null=True)
    photo = models.CharField(max_length=1000, verbose_name="Photo")
    image = models.ImageField(null=True, verbose_name="Image")
    begin_aksiya = models.IntegerField(default=0, verbose_name="Begin akysiya")
    count_a = models.IntegerField(default=0, verbose_name="Count akysiya")

    category_name = models.ForeignKey(ProductCategory, verbose_name="Category En", on_delete=models.CASCADE)
    category_name_ru = models.CharField(max_length=300, verbose_name="Category Ru", blank=True, null=True)
    category_name_uz = models.CharField(max_length=300, verbose_name="Category Ru", blank=True, null=True)
    category_code = models.CharField(verbose_name="Unnecassary category-code", max_length=300, blank=True)

    def __str__(self):
        return f"{self.name}"


class CartModel(models.Model):
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "5.Carts"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    amount = models.BigIntegerField(verbose_name="Amount")
    total = models.BigIntegerField(verbose_name="Total")
    is_success = models.BooleanField(verbose_name="Purchased ?", blank=True, null=True)

    def __str__(self):
        return str(self.product)


class Order(models.Model):
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "6.Orders"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    name = models.CharField(max_length=400, verbose_name="Name")
    phone = models.CharField(max_length=400, verbose_name="Phone", blank=True, null=True)
    address = models.CharField(max_length=400, verbose_name="Address company")
    purchases = models.TextField(verbose_name="Purchases")
    total = models.BigIntegerField(verbose_name="Total")
    is_success = models.BooleanField(verbose_name="Delivered ?", blank=True, null=True, default=False)
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.total)


class Location(models.Model):
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "7.Locations"

    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=400, verbose_name="User id", null=True)
    name = models.CharField(max_length=400, verbose_name="Name")
    longitude = models.CharField(max_length=400, verbose_name="Longitude")
    latitude = models.CharField(max_length=400, verbose_name="Latitude")


class Cashback(models.Model):
    class Meta:
        verbose_name = "Cashback"
        verbose_name_plural = "8.Cashbacks"

    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=400, verbose_name="User id", null=True)
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=False)
    count = models.IntegerField(default=1)


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.category_code:
        instance.category_code = instance.category_name.category_name
    if instance.category_code != instance.category_name.category_name:
        instance.category_code = instance.category_name.category_name
    if instance.category_name_ru is None or instance.category_name_ru != instance.category_name.category_name_ru:
        instance.category_name_ru = instance.category_name.category_name_ru
    if instance.category_name_uz is None or instance.category_name_uz != instance.category_name.category_name_uz:
        instance.category_name_uz = instance.category_name.category_name_uz


pre_save.connect(category_pre_save_receiver, sender=Product)
pre_save.connect(category_pre_save_receiver, sender=ProductAksiya)
