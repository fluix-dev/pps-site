from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from .models import *

class CategoryInLine(SortableInlineAdminMixin, admin.TabularInline):
    list_display = ('sort_order', 'name', 'parent')
    model = Category
    extra = 0

@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    #def get_model_perms(self, request): return {}

    list_display = ('name', 'parent')
    inlines = [
        CategoryInLine,
    ]
