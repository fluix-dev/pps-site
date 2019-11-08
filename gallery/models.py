import uuid

from django.db import models
from django.urls import reverse
from django.utils.html import format_html

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('Category', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link_override = models.CharField(max_length=200, default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['sort_order']

    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False)

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
