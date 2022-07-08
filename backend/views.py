from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework import viewsets


class ProductView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


