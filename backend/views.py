from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCategoryView(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


