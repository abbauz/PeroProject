from django.contrib import admin
from .models import PhotoModel, VideoModel, About, Messenger

admin.site.register(About)
admin.site.register(Messenger)
# admin.site.register(PhotoModel)
# admin.site.register(VideoModel)

