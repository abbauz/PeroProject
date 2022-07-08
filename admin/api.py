from rest_framework import routers
from backend.views import ProductView

router = routers.DefaultRouter()

router.register(r'products', ProductView, basename='products')
