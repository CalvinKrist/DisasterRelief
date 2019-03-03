from django.contrib import admin

# Register your models here.
from . models import MediaAlert

@admin.register(MediaAlert)
class MediaAmin(admin.ModelAdmin):
    pass