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
    context = {
        'parent_categories': Category.objects.filter(parent=None),
        'latest': Category.objects.all().exclude(parent=None)[0]
    }
    return render(request, 'index.html', context)
