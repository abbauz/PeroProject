from rest_framework import serializers
from .models import Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'name_ru', 'name_uz', 'price', 'description_ru', 'description_en', 'description_uz', 'image']


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'category_name', 'category_name_ru', 'category_name_uz', 'image']

