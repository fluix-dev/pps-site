from django.contrib import admin
from .models import *

class CategoryInLine(admin.TabularInline):
    model = Category
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        CategoryInLine,
    ]

# Register your models here.
admin.site.register(Category, CategoryAdmin)
