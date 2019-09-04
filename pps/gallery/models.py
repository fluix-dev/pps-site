from django.db import models
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

# Create your models here.
class Category(SortableMixin):
    name = models.CharField(max_length=100)
    #parent = models.ForeignKey('Category', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    parent = SortableForeignKey('Category', related_name='children', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order']

    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.name
