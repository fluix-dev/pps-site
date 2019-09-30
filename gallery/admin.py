from django.contrib import admin
from adminsortable.admin import SortableStackedInline, NonSortableParentAdmin
from .models import *

class CategoryInLine(SortableStackedInline):
    model = Category
    extra = 0

class CategoryAdmin(NonSortableParentAdmin):
    inlines = [
        CategoryInLine,
    ]

# Register your models here.
admin.site.register(Category, CategoryAdmin)
