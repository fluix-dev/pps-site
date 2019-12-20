import uuid

from .models import *
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin


class CategoryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Category
    fields = ('name', 'link_override', 'get_url_html', 'get_admin_url', 'hidden')
    readonly_fields = ('get_url_html', 'get_admin_url')
    extra = 0


class GalleryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Gallery
    fields = ('name', 'thumbnail', 'random_thumbnail', 'image_path', 'locked', 'hidden')
    readonly_fields = ('image_path',)
    extra = 0


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)

        # Show only root directorie
        uuid_string = str(request).split("/")[4]
        if (uuid_string == "'>" and not request.GET.get('all') == 'true'):
            return qs.filter(parent=None)

        # Show all
        return qs

    list_display = ('name', 'parent')
    fieldsets = (
        ('Visibility', {
            'fields': (('name', 'parent'), 'banner', 'hidden')
        }),
        ('Linking', {
            'fields': ('link_override', 'get_url_html'),
        }),
    )
    readonly_fields = ('get_url_html',)

    inlines = [
        CategoryInline,
        GalleryInline
    ]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Displayed in list view
    date_hierarchy = 'updated_at'
    list_display = ('name', 'email', 'message_truncate', 'created_at')

    def message_truncate(self, obj):
        return obj.message[:80]

    # Displayed in model editing
    readonly_fields = ('name', 'email', 'message', 'created_at', 'updated_at')
    fieldsets = (
        ('Message', {
            'fields': ('name', 'email', 'message')
        }),
        ('Dates and Times', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Global Settings', {
            'fields': ('lock_all', 'disable_creation')
        }),
    )

admin.site.site_header = 'Prime Pix Studio Administration'
