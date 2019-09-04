from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    context = {
        'parent_categories': Category.objects.filter(parent=None)
    }
    return render(request, 'index.html', context)
