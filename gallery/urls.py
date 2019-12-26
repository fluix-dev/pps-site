from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='index'),
    path('preorder/', views.preorder, name='preorder'),
    path('contact/', views.contact, name='contact'),
    path('contact_post/', views.contact_post, name='contact_post'),
    path('help/', views.download_help, name='help'),
    path('c/<uuid:category_id>', views.category, name='category'),
    path('g/<uuid:gallery_id>', views.gallery, name='gallery'),
    path('v/<uuid:gallery_id>', views.videos, name='videos'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('media/<uuid:category_id>/<uuid:gallery_id>/<file>',
         views.serve_gallery_image, name='serve_gallery_image'),
    path('media/<uuid:category_id>/<uuid:gallery_id>/thumbnails/<file>',
         views.serve_gallery_thumbnail, name='serve_gallery_thumbnail'),
    path('media/gallery_thumbnails/<file>',
         views.serve_thumbnail, name='serve_thumbnail')
]
