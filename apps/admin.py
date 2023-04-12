from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import regionType

# Register your models here.

@admin.register(regionType)
class regionTypeAdmin(admin.ModelAdmin):
    pass
