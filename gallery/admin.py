from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from .models import *

import uuid

class CategoryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Category
    fields = ('name','link_override','get_url_html')
    readonly_fields = ('get_url_html',)
    extra = 0


class GalleryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Gallery
    fields = ('name','thumbnail','image_path')
    readonly_fields = ('image_path',)
    extra = 0

@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)

        #Show only root directorie
        uuid_string = str(request).split("/")[4]
        if (uuid_string == "'>" and not request.GET.get('all') == 'true'):
            return qs.filter(parent=None)

        #Show all
        return qs

    list_display = ('name','parent')
    fields = (('name','parent'),'link_override','get_url_html')
    readonly_fields = ('get_url_html',)

    inlines = [
        CategoryInline,
        GalleryInline
    ]
