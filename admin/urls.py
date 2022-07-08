from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .api import router
from .settings import STATIC_URL, STATIC_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]


urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
