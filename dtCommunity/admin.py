from django.contrib import admin

from dtCommunity.models import projectPost

# Register your models here.

@admin.register(projectPost)
class projectPostAdmin(admin.ModelAdmin):
    pass