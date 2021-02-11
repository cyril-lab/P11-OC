from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('search/', views.search, name='search'),
    path('product/<int:pk>/', views.product, name='product'),
    path('favorite/', views.favorite, name='favorite'),
    path('save-favorite/<int:pk_prod>/', views.save_favorite,
         name='save_favorite'),
    path('favorite-detail/<int:pk>/', views.favorite_detail,
         name='favorite-detail'),
    path('contact/', views.contact, name='contact'),
    path('legal/', views.legal, name='legal'),
]
