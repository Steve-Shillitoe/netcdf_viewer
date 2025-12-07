from django.contrib import admin
from .models import NetCDFFile

@admin.register(NetCDFFile)
class NetCDFFileAdmin(admin.ModelAdmin):
    list_display = ("file", "uploaded_at")
    ordering = ("-uploaded_at",)
