from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('booking/', views.booking, name='booking'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('process_order/', views.process_order, name='process_order'),
]

