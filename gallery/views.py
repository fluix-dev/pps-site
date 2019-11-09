import os
import sys
import PIL

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
    category = gallery.category
    root_url = os.path.join(settings.MEDIA_ROOT, str(gallery.category.category_id), str(gallery_id))
    thumbnail_url = os.path.join(root_url, 'thumbnails')
    images = [f for f in os.listdir(root_url) if isfile(join(root_url, f))]
    thumbnails = [f for f in os.listdir(thumbnail_url) if isfile(join(thumbnail_url, f))]

    # Generate thumbnails
    if (len(images) != len(thumbnails)):
        maxsize = (256, 256)
        for infile in images:
            outfile = os.path.join(thumbnail_url, infile)
            try:
                im = PIL.Image.open(os.path.join(root_url, infile))
                im.thumbnail(maxsize, PIL.Image.ANTIALIAS)
                im.save(outfile, "JPEG")
            except IOError:
                print('Failed creating a thumbnail.')

    context = {
        'parent_categories': Category.objects.filter(parent=None),
        'latest': Category.objects.all().exclude(parent=None)[0],
        'base_url': settings.MEDIA_URL + str(gallery.category.category_id) + '/' + str(gallery_id) + '/',
        'images': images,
        'category': category,
        'gallery': gallery
    }
    return render(request, 'gallery.html', context)
