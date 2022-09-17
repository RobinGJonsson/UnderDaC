import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .utils import cart_data, check_user_auth, navbar
from .forms import BookingForm, ContactForm, SignupForm
from .models import Restaurant, Order, OrderItem, MenuItem, DeliveryInfo, Booking, Customer
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout


def home(request):
    restaurants = Restaurant.objects.all()

    context = navbar(request)
    context['restaurants'] = restaurants
    return render(request, 'home.html', context)


# Sends menu items and categories to the menu page
def menu(request):
    context = navbar(request)

    categories = ['Menu', 'Vegan Menu', 'Kids Menu']
    menu_items = MenuItem.objects.all()

    context.update({'menu_items': menu_items,
                    'categories': categories})

    return render(request, 'menu.html', context)


def contact(request):
    context = navbar(request)

    form = ContactForm

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.customer = request.user
            contact.save()
            messages.add_message(request, messages.INFO,
                                 'Your Message Has Been Sent, We Will Get Back To You Shortly')
            return redirect('/')

    context['form'] = form
    return render(request, 'contact.html', context)


def checkout(request):
    context = navbar(request)
    cart_info = cart_data(request)

    restaurants = Restaurant.objects.all()
    items = cart_info['items']
    order = cart_info['order']

    context.update({'items': items,
                    'order': order,
                    'restaurants': restaurants})

    return render(request, 'checkout.html', context)


def cart(request):
    context = navbar(request)
    cart_info = cart_data(request)

    items = cart_info['items']
    order = cart_info['order']

    context.update({'items': items,
                    'order': order})

    return render(request, 'cart.html', context)


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
    context = navbar(request, name=name)
    customer = check_user_auth(request)
    restaurant = Restaurant.objects.get(name=name)

    if customer:
        data = {'first_name': customer.customer.first_name,
                'last_name': customer.customer.last_name,
                'phone': customer.customer.phone,
                'email': customer.customer.email}
        form = BookingForm(initial=data)
    else:
        form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            new_booking = form.save(commit=False)
            booking_date = new_booking.date
            booking_time = new_booking.time

            if customer:
                customer_bookings = Booking.objects.filter(
                    customer=customer)
            else:
                customer_bookings = Booking.objects.filter(
                    first_name=new_booking.first_name,
                    last_name=new_booking.last_name,
                    phone=new_booking.phone,
                    email=new_booking.email)

            # Don't allow bookings 3 hours before or after an existing booking 
            # belonging to the current customer
            for booking in customer_bookings:
                if booking.date == booking_date:
                    booking.time.hour*60 + booking.time.minute
                    booking_time.hour*60 + booking_time.minute
                    hour_time_dif = abs((
                        booking.time.hour*60 + booking.time.minute
                    ) - (booking_time.hour*60 + booking_time.minute)) / 60
                    if hour_time_dif <= 3:
                        messages.add_message(request, messages.INFO,
                                             'The Time of Your Booking is Too Close to Another Booking You Have.. Bookings Must Be at Least 3 Hours Apart')
                        return (redirect(f'/restaurant_booking/{name}'))

            if customer:
                new_booking.customer = customer
            new_booking.restaurant = restaurant
            new_booking.save()

            # Send email confirmation
            send_mail(
                f'{new_booking.restaurant} Booking Confirmation',
                f'Hello {new_booking.first_name} your booking to {new_booking.restaurant} has been made for {new_booking.date} at {new_booking.time}',
                'c.robin.g.j@gmail.com',
                [str(new_booking.email)],
                fail_silently=False,
            )
            messages.add_message(request, messages.INFO,
                                 'The Booking Confirmation Has Been Sent to Your Email')
            return (redirect(f'/restaurant_booking/{name}'))

    context.update({'restaurant': restaurant,
                    'form': form})
    return render(request, 'restaurant_booking.html', context)


def my_bookings(request):
    context = navbar(request)
    return render(request, 'my_bookings.html', context)


def my_details(request):
    context = navbar(request)
    customer_details = Customer.objects.get(customer=request.user)

    context['customer_details'] = customer_details
    return render(request, 'my_details.html', context)


def update_cart(request):
    # Unpack json data collected from add to cart buttons
    data = json.loads(request.body)
    itemID = data['itemID']
    action = data['action']

    print('Action: ', action)
    print('ItemID: ', itemID)

    # Asign a customer
    customer = request.user
    # Get the specific menu item that was clicked
    item = MenuItem.objects.get(id=itemID)
    # Get or create an order and asign it to the current customer
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


def update_details(request):
    context = navbar(request)
    customer_details = Customer.objects.get(customer=request.user)

    form = SignupForm(instance=customer_details)

    if request.method == 'POST':
        form = SignupForm(request.POST, instance=customer_details)
        if form.is_valid:
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Your Details Have Been Updated')
            return redirect('/my_details/')

    context.update({'form': form,
                    'customer_details': customer_details})
    return render(request, 'update_details.html', context)


def update_booking(request, pk):
    context = navbar(request)

    booking = Booking.objects.get(id=pk)
    form = BookingForm(instance=booking)
    restaurant = booking.restaurant

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Your Booking Has Been Updated')

    context.update({'form': form,
                    'restaurant': restaurant,
                    'update': True})
    return render(request, 'restaurant_booking.html', context)


def delete_booking(request, pk, name):
    booking = Booking.objects.get(id=pk)
    booking.delete()

    messages.add_message(request, messages.INFO,
                         'Your Booking Has Been Deleted')

    return redirect('/my_bookings/')


def delete_account(request, pk):
    customer = Customer.objects.get(id=pk)
    logout(request)
    customer.customer.delete()

    messages.add_message(request, messages.INFO,
                         'Your Account Has Been Deleted')

    return redirect('/')
