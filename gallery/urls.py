from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('c/<uuid:category_id>', views.category, name='category'),
    path('g/<uuid:gallery_id>', views.gallery, name='gallery')
]
