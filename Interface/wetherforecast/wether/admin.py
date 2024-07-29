# admin.py
from django.contrib import admin
from .models import Data, CropType


class admin_view(admin.ModelAdmin):
    list_display = ['locations', 'done']
    list_editable = ['done']


# Register the Data model with the custom admin class
admin.site.register(Data, admin_view)
admin.site.register(CropType)
