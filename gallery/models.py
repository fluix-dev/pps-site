import os
import random
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import format_html


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, help_text='Model creation time.')
    updated_at = models.DateTimeField(
        auto_now=True, help_text='Last update time.')

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100, help_text='Name of the category.')
    parent = models.ForeignKey(
        'Category', related_name='children', on_delete=models.CASCADE, blank=True,
        null=True, help_text='A parent category seen as the dropdown link on navbar.')
    category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    link_override = models.CharField(
        max_length=200, default=None, blank=True, null=True,
        help_text='A link which overrieds the category url in the navbar.')
    banner = models.CharField(max_length=1000, default=None, blank=True, null=True,
                              help_text="A banner shown on the Category's page.")
    hidden = models.BooleanField(default=False,
                                 help_text='Whether the category should be hidden from the navbar.')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Menus'
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
        return format_html("<a href='{url}'>View Site</a>", url=self.get_url)

    @property
    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        admin_url = reverse('admin:%s_%s_change' % info, args=(self.pk,))
        return format_html("<a href='{url}'>View Admin</a>", url=admin_url)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        'Category', related_name='galleries', on_delete=models.CASCADE,
        help_text='Category in which the gallery resides.')
    gallery_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    thumbnail = models.ImageField(
        upload_to='gallery_thumbnails', blank=True, null=True,
        help_text='The thumbnail of the gallery which may be left blank.')
    random_thumbnail = models.BooleanField(default=True,
                                           help_text="Whether a random thumbnail should be picked if the thumbnail isn't set.")
    locked = models.BooleanField(default=True,
                                 help_text='Whether the images within the gallery can be downloaded or are free from watermark.')
    hidden = models.BooleanField(default=False,
                                 help_text='Whether the gallery should be hidden from the category view.')

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
        ordering = ['sort_order']

    sort_order = models.PositiveIntegerField(
        default=0, blank=False, null=False)

    @property
    def image_path(self):
        if self.gallery_id is not None:
            return os.path.join(settings.GALLERY_ROOT, str(self.category.category_id), str(self.gallery_id))
        return None

    @property
    def get_admin_url(self):
        info = (self.category._meta.app_label, self.category._meta.model_name)
        admin_url = reverse('admin:%s_%s_change' % info, args=(self.category.pk,))
        return format_html("<a href='{url}'>{name}</a>", url=admin_url, name=self.category.name)

    @property
    def get_thumbnail_url(self):
        if self.thumbnail:
            # Specified thumbnail
            return reverse('serve_thumbnail', args=[os.path.basename(self.thumbnail.name)])
        else:
            # Random thumbnail
            if self.random_thumbnail:
                # Get list of all thumbnail
                root_url = os.path.join(settings.GALLERY_ROOT, str(
                    self.category.category_id), str(self.gallery_id))
                thumbnail_url = os.path.join(root_url, 'thumbnails')
                thumbnails = [f for f in os.listdir(
                    thumbnail_url) if os.path.isfile(os.path.join(thumbnail_url, f))]

                # Choose random thumbnail
                if (len(thumbnails) != 0):
                    return reverse('serve_gallery_thumbnail',
                                   args=[self.category.category_id, self.gallery_id, random.choice(thumbnails)])

        # Fallback to blank thumbnail
        return settings.STATIC_URL + '/img/blank.png'

    def __str__(self):
        return self.name


class ContactMessage(TimeStampMixin):
    name = models.CharField(
        max_length=100, editable=False, help_text="User's name.")
    email = models.EmailField(editable=False, help_text="User's email.")
    message = models.TextField(
        max_length=2047, editable=False, help_text="User's message.")

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.name

class Settings(models.Model):
    lock_all = models.BooleanField(default=False, help_text='Lock all galleries.')
    use_x_sendfile = models.BooleanField(default=True, help_text="Whether to send files using Nginx's XSendFile Header or not.")

    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'

    def save(self, *args, **kwargs):
        if not self.pk and Settings.objects.exists():
            raise ValidationError('There is can be only one Settings instance.')
        return super(Settings, self).save(*args, **kwargs)

    def __str__(self):
        return 'Global Settings'

@receiver(post_save, sender=Gallery)
def create_image_paths(sender, instance, **kwargs):
    thumbnail_path = os.path.join(instance.image_path, 'thumbnails')
    if not os.path.exists(thumbnail_path):
        os.makedirs(thumbnail_path)

    watermark_path = os.path.join(instance.image_path, 'watermarked')
    if not os.path.exists(watermark_path):
        os.makedirs(watermark_path)
