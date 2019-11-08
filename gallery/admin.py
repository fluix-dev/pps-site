from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from .models import *

class CategoryInLine(SortableInlineAdminMixin, admin.TabularInline):
    list_display = ('name', 'parent')
    model = Category
    extra = 0

@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        return qs.filter(parent=None)

    list_display = ('name', 'parent')
    inlines = [
        CategoryInLine,
    ]
