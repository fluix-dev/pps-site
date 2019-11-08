from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('Category', related_name='children', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['sort_order']

    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name
