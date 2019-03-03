from django.contrib import admin

# Register your models here.
import .models.MediaAlert

@admin.register(MediaAlert)
class MediaAmin(admin.ModelAdmin):
    pass