from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('table_booking/', views.table_booking, name='table_booking'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('process_order/', views.process_order, name='process_order'),
    path('update_booking/<str:pk>/', views.update_booking, name='update_booking'),
    path('delete_booking/<str:pk>/', views.delete_booking, name='delete_booking'),
    path('profile/', views.profile, name='profile'),
    path('restaurant_booking/<str:name>/', views.restaurant_booking, name='restaurant_booking'),

]

