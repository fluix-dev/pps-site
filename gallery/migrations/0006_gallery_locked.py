# Generated by Django 2.2.5 on 2019-12-03 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_gallery_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='locked',
            field=models.BooleanField(default=True),
        ),
    ]