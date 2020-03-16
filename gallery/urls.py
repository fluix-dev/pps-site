from . import views

from django.urls import path

urlpatterns = [
    # Static pages
    path('', views.home, name='index'),
    path('help/', views.download_help, name='help'),
    path('maintenance/', views.maintenance, name='maintenance'),

    # Pre-ordering
    path('preorder/', views.preorder, name='preorder'),
    path('preorder/package', views.package, name='package'),
    path('preorder/individual', views.individual, name='individual'),
    path('preorder/checkout', views.checkout, name='checkout'),
    path('preorder/charge', views.charge, name='charge'),

    # Contact
    path('contact/', views.contact, name='contact'),
    path('contact_post/', views.contact_post, name='contact_post'),
    
    # Dynamic pages
    path('c/<uuid:category_id>', views.category, name='category'),
    path('g/<uuid:gallery_id>', views.gallery, name='gallery'),
    path('v/<uuid:gallery_id>', views.videos, name='videos'),

    # Media files
    path('media/<uuid:category_id>/<uuid:gallery_id>/<file>',
        views.serve_gallery_image, name='serve_gallery_image'),
    path('media/<uuid:category_id>/<uuid:gallery_id>/thumbnails/<file>',
        views.serve_gallery_thumbnail, name='serve_gallery_thumbnail'),
    path('media/gallery_thumbnails/<file>',
        views.serve_thumbnail, name='serve_thumbnail')
]