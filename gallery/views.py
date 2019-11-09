import os
from os.path import isfile, join

from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    context = {
        'parent_categories': Category.objects.filter(parent=None),
        'latest': Category.objects.all().exclude(parent=None)[0]
    }
    return render(request, 'index.html', context)

def category(request, category_id):
    category = Category.objects.get(category_id=category_id)
    context = {
        'parent_categories': Category.objects.filter(parent=None),
        'latest': Category.objects.all().exclude(parent=None)[0],
        'category': category,
        'galleries': category.galleries.all()
    }
    return render(request, 'category.html', context)

def gallery(request, gallery_id):
    gallery = Gallery.objects.get(gallery_id=gallery_id)
    root_url = os.path.join(settings.MEDIA_ROOT, str(gallery.category.category_id), str(gallery_id))
    images = [f for f in os.listdir(root_url) if isfile(join(root_url, f))]

    context = {
        'parent_categories': Category.objects.filter(parent=None),
        'latest': Category.objects.all().exclude(parent=None)[0],
        'base_url': settings.MEDIA_URL + str(gallery.category.category_id) + '/' + str(gallery_id) + '/',
        'images': images
    }
    return render(request, 'gallery.html', context)
