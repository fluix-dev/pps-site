import math
import os

from .models import Category, ContactMessage, Gallery, Settings

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html

from PIL import Image
from threading import Thread


class CategoryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Category
    fields = ('name', 'link_override', 'get_url_html',
              'get_admin_url', 'hidden')
    readonly_fields = ('get_url_html', 'get_admin_url')
    extra = 0


class GalleryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Gallery
    fields = ('name', 'thumbnail', 'random_thumbnail',
              'image_path', 'locked', 'hidden')
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


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    # Displayed in list view
    list_display = ('name', 'get_admin_url', 'locked', 'hidden', 'account_actions')
    readonly_fields = ('account_actions',)
    search_fields = ['name']
    ordering = ('category__name','name')

    def account_actions(self, obj):
        # TODO: Render action buttons
        return format_html(
            '<a class="button" href="{}">Generate Thumbnails</a>&nbsp;'
            '<a class="button" href="{}">Generate Watermarks</a>&nbsp;'
            '<a class="button" href="{}">Generate Zip</a>',
            reverse('admin:generate_thumbnails', args=[obj.pk]),
            reverse('admin:generate_watermarks', args=[obj.pk]),
            reverse('admin:generate_zip', args=[obj.pk]),
        )
    account_actions.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        admin_urls = [
            path('generate_thumbnails/<uuid:gallery_id>',
                 self.generate_thumbnails, name='generate_thumbnails'),
            path('generate_watermarks/<uuid:gallery_id>',
                 self.generate_watermarks, name='generate_watermarks'),
            path('generate_zip/<uuid:gallery_id>',
                 self.generate_zip, name='generate_zip'),
        ]
        return admin_urls + urls

    def generate_thumbnails(self, request, gallery_id):
        if not request.user.is_authenticated:
            raise Http404

        gallery = get_object_or_404(Gallery, gallery_id=gallery_id)
        root_url = os.path.join(settings.GALLERY_ROOT, str(
            gallery.category.category_id), str(gallery_id))
        thumbnail_url = os.path.join(root_url, 'thumbnails')

        # Get list of images
        images = [f for f in os.listdir(root_url) if os.path.isfile(os.path.join(root_url, f))]
        images = [f for f in images if 'jpg' in os.path.splitext(f)[1]]
        images.sort()

        # Generate thumbnails
        thread = Thread(target=self.create_thumbnails, args=(
            images, root_url, thumbnail_url))
        thread.start()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def generate_watermarks(self, request, gallery_id):
        if not request.user.is_authenticated:
            raise Http404

        gallery = get_object_or_404(Gallery, gallery_id=gallery_id)
        root_url = os.path.join(settings.GALLERY_ROOT, str(
            gallery.category.category_id), str(gallery_id))
        watermark_url = os.path.join(root_url, 'watermarked')

        # Get list of images
        images = [f for f in os.listdir(root_url) if os.path.isfile(os.path.join(root_url, f))]
        images = [f for f in images if 'jpg' in os.path.splitext(f)[1]]
        images.sort()

        # Generate watermakred images
        thread = Thread(target=self.create_watermarks, args=(
            images, root_url, watermark_url))
        thread.start()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def generate_zip(self, request, gallery_id):
        if not request.user.is_authenticated:
            raise Http404
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Create thumbnails
    def create_thumbnails(self, images, root_url, thumbnail_url):
        maxsize = (256, 256)
        for infile in images:
            outfile = os.path.join(thumbnail_url, infile)
            im = Image.open(os.path.join(root_url, infile))
            im.thumbnail(maxsize, Image.ANTIALIAS)
            im.save(outfile, "JPEG")

    # Create watermarks
    def create_watermarks(self, images, root_url, watermark_url):
        for infile in images:
            outfile = os.path.join(watermark_url, infile)

            # Open images
            im = Image.open(os.path.join(root_url, infile))
            watermark = Image.open(os.path.join(
                settings.STATIC_ROOT, 'img', 'watermark.png'))

            # Calculate dimensions
            maxwidth, maxheight = im.size
            width, height = watermark.size
            ratio = min(maxwidth / width, maxheight / height)
            watermark = watermark.resize(
                (math.floor(width * ratio), math.floor(height * ratio)))
            width, height = watermark.size
            watermark_pos = (math.floor(maxwidth / 2 - width / 2),
                             math.floor(maxheight / 2 - height / 2))

            # Create final image
            transparent = Image.new('RGBA', im.size, (0, 0, 0, 0))
            transparent.paste(im, (0, 0))
            transparent.paste(watermark, watermark_pos, mask=watermark)
            transparent.convert('RGB').save(outfile, "JPEG")


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Global Settings', {
            'fields': ('lock_all', 'use_x_sendfile')
        }),
    )


admin.site.site_header = 'Prime Pix Studio Administration'
