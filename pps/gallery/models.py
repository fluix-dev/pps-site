from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('Category', related_name='children', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
