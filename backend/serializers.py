from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'name_ru', 'name_uz', 'price', 'description_ru', 'description_en', 'description_uz', 'photo']
