import os
import sys
import PIL

from PIL import Image
from os.path import isfile, join
from django.shortcuts import render
from .models import *
from django.http import HttpResponse, Http404

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

    # Get list of images and thumbnails
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

def serve_protected(request, category_id, gallery_id, file):
    # Determine path to requested file
    if 'thumbnail' in str(request):
        valid_image = os.path.join(settings.MEDIA_ROOT, str(category_id), str(gallery_id), 'thumbnails', str(file))
    else:
        valid_image = os.path.join(settings.MEDIA_ROOT, str(category_id), str(gallery_id), str(file))

    # Return the image
    try:
        if ('0010LS' in str(request)):
            raise Http404()
        with open(valid_image, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        # Empty image
        red = Image.new('RGB', (1, 1), (0,0,0,0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response
