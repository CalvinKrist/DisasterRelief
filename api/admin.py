from django.contrib import admin

# Register your models here.
import api.models.MediaAlert as MediaAlert

@admin.register(MediaAlert)
class MediaAmin(admin.ModelAdmin):
    pass