from rest_framework import routers
from backend.views import *

router = routers.DefaultRouter()

router.register(r'products', ProductView, basename='products')
router.register(r'categories', ProductCategoryView, basename='categories')
