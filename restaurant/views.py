from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import BookingForm, ContactForm
from .models import Restaurant
from . import utils


from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

from .models import *
from .forms import *
from .utils import *


def home(request):
    restaurants = Restaurant.objects.all()
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']

    context = {'restaurants': restaurants,
               'cart_count': cart_count}

    return render(request, 'home.html', context)


# Sends menu items and categories to the menu page
def menu(request):
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']
    categories = ['Menu', 'Vegan Menu', 'Kids Menu']
    menu_items = MenuItem.objects.all()

    context = {'menu_items': menu_items,
               'categories': categories,
               'cart_count': cart_count}

    return render(request, 'menu.html', context)


def booking(request):
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']
    customer = check_user_auth(request)
    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = customer
            form.save()
            return redirect('/')

    context = {'form': form,
               'cart_count': cart_count}

    return render(request, 'booking.html', context)


def contact(request):
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']
    form = ContactForm

    context = {'cart_count': cart_count,
               'form': form}

    return render(request, 'contact.html', context)


def checkout(request):
    restaurants = Restaurant.objects.all()
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']
    items = cart_info['items']
    order = cart_info['order']

    context = {'items': items,
               'order': order,
               'cart_count': cart_count,
               'restaurants': restaurants}

    return render(request, 'checkout.html', context)


def cart(request):
    print(request.COOKIES)
    cart_info = cart_data(request)

    cart_count = cart_info['cart_count']
    items = cart_info['items']
    order = cart_info['order']

    context = {'items': items,
               'order': order,
               'cart_count': cart_count}
    return render(request, 'cart.html', context)


def update_cart(request):
    # Unpack json data from collected from add to cart buttons
    data = json.loads(request.body)
    itemID = data['itemID']
    action = data['action']

    print('Action: ', action)
    print('ItemID: ', itemID)

    # Asign a customer
    customer = request.user.customer
    # Get the specific menu item that was clicked
    item = MenuItem.objects.get(id=itemID)
    # Get or create an order and asign it to the current customer already has an order
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    # Get or create an order item and asign it to the current order
    order_item, created = OrderItem.objects.get_or_create(
        order=order, item=item)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'subtract':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

        order.delivery = data['deliveryFormData']['delivery']
        order.delivery_time = data['deliveryFormData']['delivery_time']
        order.restaurant = Restaurant.objects.get(
            name=data['deliveryFormData']['restaurant'])

        order.complete = True
        order.save()

        if order.delivery == True:
            DeliveryInfo.objects.create(
                customer=customer,
                order=order,
                firstName=data['userFormData']['fname'],
                lastName=data['userFormData']['lname'],
                address=data['deliveryFormData']['address'],
                city=data['deliveryFormData']['city']
            ).save()

    else:
        print('User is not logged in')
    return JsonResponse('Payment Complete', safe=False)
