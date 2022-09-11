import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .utils import cart_data, check_user_auth
from .forms import BookingForm, ContactForm, SignupForm
from .models import Restaurant, Order, OrderItem, MenuItem, DeliveryInfo, Booking, Customer
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout


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


def contact(request):
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']
    customer = check_user_auth(request)
    form = ContactForm

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.customer = customer
            contact.save()
            messages.add_message(request, messages.INFO,
                                 'Your Message Has Been Sent')
            return redirect('/')

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


def update_booking(request, pk):
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']
    booking = Booking.objects.get(id=pk)
    form = BookingForm(instance=booking)
    restaurant = booking.restaurant

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Your Booking Has Been Updated')

    context = {'form': form,
               'restaurant': restaurant,
               'update': True,
               'cart_count': cart_count}

    return render(request, 'restaurant_booking.html', context)


def delete_booking(request, pk, name):
    booking = Booking.objects.get(id=pk)
    booking.delete()

    messages.add_message(request, messages.INFO,
                         'Your Booking Has Been Deleted')

    return redirect(f'/restaurant_booking/{name}')


def update_cart(request):
    # Unpack json data from collected from add to cart buttons
    data = json.loads(request.body)
    itemID = data['itemID']
    action = data['action']

    print('Action: ', action)
    print('ItemID: ', itemID)

    # Asign a customer
    customer = request.user
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

        if order.delivery:
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


def restaurant_booking(request, name):
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']
    customer = check_user_auth(request)

    restaurant = Restaurant.objects.get(name=name)
    customer_bookings = Booking.objects.filter(
        customer=customer, restaurant=restaurant).order_by('date')

    # claculate number of hours open in restaurant
    # Add number of tables to restaurant
    # Add open and close times to restaurant
    # add one button for each half hour

    # Iterate through each hour
    # Add two buttons for each hour; whole and half hour
    #

    # for i in range()

    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if customer:
                booking.customer = customer
            booking.restaurant = restaurant
            booking.save()

            # Send email confirmation
            send_mail(
                f'{booking.restaurant} Booking Confirmation',
                f'Hello {booking.first_name} your booking to {booking.restaurant} has been made for {booking.date} at {booking.time}',
                'c.robin.g.j@gmail.com',
                [str(booking.email)],
                fail_silently=False,
            )
            messages.add_message(request, messages.INFO,
                                 'The Booking Confirmation Has Been Sent to Your Email')

    context = {'restaurant': restaurant,
               'form': form,
               'cart_count': cart_count,
               'customer_bookings': customer_bookings}
    if customer_bookings:
        context['customer_bookings'] = customer_bookings
    return render(request, 'restaurant_booking.html', context)


def my_bookings(request):
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']
    customer = check_user_auth(request)

    customer_bookings = Booking.objects.filter(customer=customer)

    context = {'cart_count': cart_count,
               'cart_count': cart_count}

    customer_bookings = Booking.objects.filter(
        customer=customer).order_by('date')
    if customer_bookings:
        context['customer_bookings'] = customer_bookings

    return render(request, 'my_bookings.html', context)


def my_details(request):
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']
    customer = check_user_auth(request)

    customer_details = Customer.objects.get(customer=customer)
    context = {'customer_details': customer_details,
               'cart_count': cart_count}

    print(customer_details.id)
    return render(request, 'my_details.html', context)


def update_details(request, pk):
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']

    customer_details = Customer.objects.get(id=pk)
    form = SignupForm(instance=customer_details)

    if request.method == 'POST':
        form = SignupForm(request.POST, instance=customer_details)
        if form.is_valid:
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Your Details Have Been Updated')
            return redirect('/my_details/')

    context = {'form': form,
               'customer_details': customer_details,
               'cart_count': cart_count}
    return render(request, 'update_details.html', context)


def delete_account(request, pk):
    customer = Customer.objects.get(id=pk)
    logout(request)
    customer.customer.delete()

    messages.add_message(request, messages.INFO,
                         'Your Account Has Been Deleted')

    return redirect('/')
