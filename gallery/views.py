import math
import os
import sys

from .models import *
from django.http import HttpResponse, Http404
from django.shortcuts import render
from os.path import isfile, join
from PIL import Image, ImageDraw, ImageFont
from threading import Thread


def get_navbar_context():
    context = {
        'parent_categories': Category.objects.filter(parent=None),
    }
    return context


def home(request):
    return render(request, 'index.html', get_navbar_context())


def contact(request):
    return render(request, 'contact.html', get_navbar_context())


def category(request, category_id):
    category = Category.objects.get(category_id=category_id)
    context = {
        'category': category,
        'galleries': category.galleries.all()
    }
    context.update(get_navbar_context())
    return render(request, 'category.html', context)


def gallery(request, gallery_id):
    gallery = Gallery.objects.get(gallery_id=gallery_id)
    category = gallery.category
    root_url = os.path.join(settings.MEDIA_ROOT, str(
        gallery.category.category_id), str(gallery_id))
    thumbnail_url = os.path.join(root_url, 'thumbnails')
    watermark_url = os.path.join(root_url, 'watermarked')

    # Get list of images and thumbnails
    images = [f for f in os.listdir(root_url) if isfile(join(root_url, f))]
    thumbnails = [f for f in os.listdir(
        thumbnail_url) if isfile(join(thumbnail_url, f))]
    watermarked = [f for f in os.listdir(
        watermark_url) if isfile(join(watermark_url, f))]

    # Generate thumbnails
    if (len(images) != len(thumbnails)):
        maxsize = (256, 256)
        for infile in images:
            outfile = os.path.join(thumbnail_url, infile)
            try:
                im = Image.open(os.path.join(root_url, infile))
                im.thumbnail(maxsize, Image.ANTIALIAS)
                im.save(outfile, "JPEG")
            except IOError:
                print('Failed creating a thumbnail.')

    # Generate watermakred images
    if (len(images) != len(watermarked)):
        thread = Thread(target=create_watermarks, args=(
            images, root_url, watermark_url))
        thread.start()

    context = {
        'base_url': settings.MEDIA_URL + str(gallery.category.category_id) + '/' + str(gallery_id) + '/',
        'images': images,
        'category': category,
        'gallery': gallery
    }
    context.update(get_navbar_context())
    return render(request, 'gallery.html', context)


# Create watermarks
def create_watermarks(images, root_url, watermark_url):
    for infile in images:
        outfile = os.path.join(watermark_url, infile)
        try:
            # Open images
            im = Image.open(os.path.join(root_url, infile))
            watermark = Image.open(os.path.join(
                settings.STATIC_ROOT, 'img', 'watermark.png'))

            # Calculate dimensions
            maxwidth, maxheight = im.size
            width, height = watermark.size
            ratio = min(maxwidth / width, maxheight / height)
            watermark = watermark.resize(
                (math.floor(width * ratio), math.floor(height * ratio)))
            width, height = watermark.size
            watermark_pos = (math.floor(maxwidth / 2 - width / 2),
                             math.floor(maxheight / 2 - height / 2))

            # Create final image
            transparent = Image.new('RGBA', im.size, (0, 0, 0, 0))
            transparent.paste(im, (0, 0))
            transparent.paste(watermark, watermark_pos, mask=watermark)
            transparent.convert('RGB').save(outfile, "JPEG")
        except IOError:
            print('Failed creating a watermark.')


# Serve full gallery thumbnail
def serve_thumbnail(request, file):
    thumbnail = os.path.join(
        'gallery_thumbnails', str(file))
    return serve_protected(request, thumbnail)


# Serve full gallery image thumbnails
def serve_gallery_thumbnail(request, category_id, gallery_id, file):
    thumbnail = os.path.join(str(
        category_id), str(gallery_id), 'thumbnails', str(file))
    return serve_protected(request, thumbnail)


# Serve full gallery images
def serve_gallery_image(request, category_id, gallery_id, file):
    if not Gallery.objects.all().get(gallery_id=gallery_id).locked:
        image = os.path.join(str(
            category_id), str(gallery_id), str(file))
    else:
        image = os.path.join(str(
            category_id), str(gallery_id), 'watermarked', str(file))
    return serve_protected(request, image)


# Serve requested file
def serve_protected(request, file):
    print("Getting file: " + str(file))
    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename={0}".format(
            os.path.basename(file))
    response['X-Accel-Redirect'] = "/media/{0}".format(str(file))
    return response
