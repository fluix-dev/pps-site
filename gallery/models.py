import os
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import format_html


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'Category', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    link_override = models.CharField(
        max_length=200, default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['sort_order']

    sort_order = models.PositiveIntegerField(
        default=0, blank=False, null=False)

    @property
    def get_url(self):
        if self.link_override is not None:
            return self.link_override
        if self.category_id is not None:
            return reverse('category', args=(self.category_id,))
        return None

    @property
    def get_url_html(self):
        return format_html("<a href='{url}'>{url}</a>", url=self.get_url)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        'Category', related_name='galleries', on_delete=models.CASCADE)
    gallery_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    thumbnail = models.ImageField(
        upload_to='gallery_thumbnails', blank=True, null=True)
    locked = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
        ordering = ['sort_order']

    sort_order = models.PositiveIntegerField(
        default=0, blank=False, null=False)

    @property
    def image_path(self):
        if self.gallery_id is not None:
            return os.path.join(settings.MEDIA_ROOT, str(self.category.category_id), str(self.gallery_id))
        return None

    def __str__(self):
        return self.name


@receiver(post_save, sender=Gallery)
def create_image_paths(sender, instance, **kwargs):
    thumbnail_path = os.path.join(instance.image_path, 'thumbnails')
    if not os.path.exists(thumbnail_path):
        os.makedirs(thumbnail_path)

    watermark_path = os.path.join(instance.image_path, 'watermarked')
    if not os.path.exists(watermark_path):
        os.makedirs(watermark_path)
