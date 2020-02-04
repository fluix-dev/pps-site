import os
import logging

from .forms import ContactForm
from .models import Category, ContactMessage, Gallery, Settings

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, reverse, get_list_or_404, get_object_or_404

from PIL import Image

logger = logging.getLogger(__name__)

WORD_BLACKLIST = ['sex', 'porn', 'dating', 'seo']

def get_navbar_context():
    context = {
        'parent_categories': Category.objects.all().filter(parent=None, hidden=False)
    }
    return context

def download_help(request):
    return render(request, 'help.html', get_navbar_context())

def home(request):
    return render(request, 'index.html', get_navbar_context())

def maintenance(request):
    return render(request, 'maintenance.html')

def preorder(request):
    return render(request, 'preorder.html', get_navbar_context())

def individual(request):
    request.session['items'] = [('Individual Image Purchase', 20)]
    request.session['total'] = 20
    return redirect(reverse('checkout'))

def package(request):
    request.session['items'] = [('Image Package Purchase', 100)]
    request.session['total'] = 100
    return redirect(reverse('checkout'))

def checkout(request):
    context = {
        'total': "%01.2f" % (request.session.get('total')),
        'items': request.session.get('items'),
        'key': settings.STRIPE_PUBLISHABLE_KEY
    }
    context.update(get_navbar_context())
    return render(request, 'checkout.html', context)

def charge(request):
    context = {}
    context.update(get_navbar_context())
    return render(request, 'charge.html')

def contact(request):
    context = {
        'form': ContactForm()
    }
    context.update(get_navbar_context())
    return render(request, 'contact.html', context)

def category(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    context = {
        'category': category,
        'galleries': category.galleries.all().filter(hidden=False)
    }
    context.update(get_navbar_context())
    return render(request, 'category.html', context)


def gallery(request, gallery_id):
    gallery = get_object_or_404(Gallery, gallery_id=gallery_id)
    category = gallery.category
    root_url = os.path.join(settings.GALLERY_ROOT, str(
        category.category_id), str(gallery_id))

    # Get list of images
    images = [f for f in os.listdir(root_url) if os.path.isfile(os.path.join(root_url, f))]
    images = [f for f in images if 'jpg' in os.path.splitext(f)[1]]
    images.sort()

    context = {
        'base_url': '/media/' + str(category.category_id) + '/' + str(gallery_id) + '/',
        'images': images,
        'category': category,
        'gallery': gallery
    }
    context.update(get_navbar_context())
    return render(request, 'gallery.html', context)


def videos(request, gallery_id):
    gallery = get_object_or_404(Gallery, gallery_id=gallery_id)
    category = gallery.category
    root_url = os.path.join(settings.GALLERY_ROOT, str(
        category.category_id), str(gallery_id))

    # Get list of images
    videos = [f for f in os.listdir(root_url) if os.path.isfile(os.path.join(root_url, f))]
    videos = [f for f in videos if 'mp4' in os.path.splitext(f)[1]]
    videos.sort()

    context = {
        'base_url': '/media/' + str(category.category_id) + '/' + str(gallery_id) + '/',
        'videos': videos,
        'category': category,
        'gallery': gallery
    }
    context.update(get_navbar_context())
    return render(request, 'videos.html', context)

def contact_post(request):
    if request.method == "POST":
        cf = ContactForm(request.POST)

        # Set default fail message
        message = 'Failed... Try again later.'
        if(cf.is_valid()):
            # Check for blacklisted words
            for word in WORD_BLACKLIST:
                if word in cf.cleaned_data['message']:
                    # Fake sent response
                    return HttpResponse("Sent!")

            # Create actual object
            cm = ContactMessage()
            cm.name = cf.cleaned_data['name']
            cm.email = cf.cleaned_data['email']
            cm.message = cf.cleaned_data['message']
            cm.save()

            # Success Message
            message = "Sent!"

        return HttpResponse(message)
    return Http404()


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
    if (not Gallery.objects.all().get(gallery_id=gallery_id).locked and
            not Settings.objects.all().first().lock_all or
            'mp4' in os.path.splitext(file)[1]):
        image = os.path.join(str(category_id), str(gallery_id), str(file))
    else:
        image = os.path.join(str(category_id), str(
            gallery_id), 'watermarked', str(file))
    return serve_protected(request, image)


# Serve requested file
def serve_protected(request, file):
    # Use XSendFile if it's enabled
    g_settings = Settings.objects.all().first()
    if g_settings.use_x_sendfile:
        response = HttpResponse()
        response['Content-Type'] = ''
        response['X-Accel-Redirect'] = '/protected/' + str(file)
        return response

    # Let Django serve the file itself
    file = os.path.join(settings.MEDIA_ROOT, file)
    try:
        with open(file, "rb") as f:
            return HttpResponse(f.read(), content_type="")
    except IOError:
        # Empty image
        red = Image.new('RGB', (1, 1), (0, 0, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response
