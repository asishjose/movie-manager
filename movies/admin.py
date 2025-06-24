from django.contrib import admin

# Register your models here.
from . models import MovieInfo,Director,CensorInfo,Actor

admin.site.register(MovieInfo)
admin.site.register(Director)
admin.site.register(CensorInfo)
admin.site.register(Actor)