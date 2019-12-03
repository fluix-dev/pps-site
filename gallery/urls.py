from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('c/<uuid:category_id>', views.category, name='category'),
    path('g/<uuid:gallery_id>', views.gallery, name='gallery'),
    path('media/<uuid:category_id>/<uuid:gallery_id>/<file>', views.serve_protected, name='serve_protected'),
    path('media/<uuid:category_id>/<uuid:gallery_id>/thumbnails/<file>', views.serve_protected, name='serve_protected')
]
