from django.contrib import admin

from .models import SRreview, CeiTreeList, Group, Type, ProcessGuideList, Type1, Type2, Type3


# Register your models here.

@admin.register(SRreview)
class SRreviewAdmin(admin.ModelAdmin):
    pass



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    pass
@admin.register(CeiTreeList)
class CeiTreeListAdmin(admin.ModelAdmin):
    pass



@admin.register(ProcessGuideList)
class ProcessGuideListAdmin(admin.ModelAdmin):
    pass
@admin.register(Type1)
class Type1Admin(admin.ModelAdmin):
    pass
@admin.register(Type2)
class Type2Admin(admin.ModelAdmin):
    pass
@admin.register(Type3)
class Type3Admin(admin.ModelAdmin):
    pass