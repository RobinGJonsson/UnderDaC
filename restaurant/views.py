import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .utils import cart_data, check_user_auth, navbar, booking_validation
from .forms import BookingForm, ContactForm, SignupForm
from .models import Restaurant, Order, OrderItem, MenuItem, DeliveryInfo, Booking, Customer
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout


def home(request):
    restaurants = Restaurant.objects.all()

    context = navbar(request)
    print(context['cart_count'])
    context['restaurants'] = restaurants
    return render(request, 'home.html', context)


# Sends menu items and categories to the menu page
def menu(request):
    context = navbar(request)

    categories = ['Menu', 'Vegan Menu', 'Kids Menu']
    menu_items = MenuItem.objects.all()

    context.update({'menu_items': menu_items,
                    'categories': categories})

    if request.method == 'POST':
        messages.add_message(request, messages.INFO,
                             'Item Added To Your Order')
        return redirect('/menu/')

    return render(request, 'menu.html', context)


def contact(request):
    context = navbar(request)

    if request.user.is_authenticated:
        form = ContactForm(initial={'email': request.user.email})
    else:
        form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.customer = request.user
            contact.save()
            messages.add_message(request, messages.INFO,
                                 '''Your Message Has Been Sent, We Will Get
                                 Back To You Shortly''')
            return redirect('/home/')

    context['form'] = form
    return render(request, 'contact.html', context)


def checkout(request):
    context = navbar(request)
    cart_info = cart_data(request)
    customer = request.user

    restaurants = Restaurant.objects.all()
    items = cart_info['items']
    order = cart_info['order']

    if request.method == 'POST':
        order = Order.objects.get(customer=customer, complete=False)
        delivery_info = DeliveryInfo.objects.create(customer=customer,
                                                    order=order,
                                                    address=request.address,
                                                    city=request.city)

        delivery_info.save()

    context.update({'items': items,
                    'order': order,
                    'restaurants': restaurants})

    return render(request, 'checkout.html', context)


def cart(request):
    context = navbar(request)
    cart_info = cart_data(request)

    items = cart_info['items'].order_by('id')
    order = cart_info['order']

    context.update({'items': items,
                    'order': order})

    return render(request, 'cart.html', context)


def process_order(request):
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
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
                first_name=data['userFormData']['fname'],
                last_name=data['userFormData']['lname'],
                address=data['deliveryFormData']['address'],
                city=data['deliveryFormData']['city']
            ).save()

        print('Order Completed')

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
            new_booking = booking_validation(form, customer, restaurant)
            if new_booking == 'No Tables':
                messages.add_message(request, messages.WARNING,
                                     '''Unfortunatly There Are No 
                                     Tables Available at Your Chosen Time''')
                return redirect(f'/restaurant_booking/{name}/')
            if new_booking == 'Too Close':
                messages.add_message(request, messages.WARNING,
                                     '''The Time of Your Booking is 
                                     Too Close to Another Booking You 
                                     Have. Bookings Must Be at 
                                     Least 3 Hours Apart''')
                return redirect(f'/restaurant_booking/{name}/')

            if customer:
                new_booking.customer = customer
            new_booking.restaurant = restaurant
            new_booking.save()

            # Send email confirmation
            send_mail(
                f'{new_booking.restaurant} Booking Confirmation',
                f'''Hello {new_booking.first_name} your booking to 
                {new_booking.restaurant} has been made for {new_booking.date}
                 at {new_booking.time}''',
                'robin__94@hotmail.se',
                [str(new_booking.email)],
                fail_silently=False,
            )
            messages.add_message(request, messages.INFO,
                                 '''The Booking Confirmation Has
                                  Been Sent to Your Email''')
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
    print(data)
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
    elif action == 'deleteAll':
        order_item.quantity = 0
        
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse('Item was updated', safe=False)


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
    customer = check_user_auth(request)
    booking = Booking.objects.get(id=pk)
    form = BookingForm(instance=booking)
    restaurant = booking.restaurant
    context = navbar(request, name=restaurant.name)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            new_booking = booking_validation(form, customer, restaurant)
            if not new_booking:
                messages.add_message(request, messages.WARNING,
                                     '''The Time of Your Booking is Too Close 
                                     to Another Booking You Have. Bookings Must
                                      Be at Least 3 Hours Apart''')
                return redirect(f'/restaurant_booking/{restaurant.name}/')
            new_booking.save()
            messages.add_message(request, messages.INFO,
                                 'Your Booking Has Been Updated')
            return redirect(f'/restaurant_booking/{restaurant.name}/')

    context.update({'form': form,
                    'restaurant': restaurant,
                    'update': True})
    return render(request, 'restaurant_booking.html', context)


def delete_booking(request, pk, name=None):
    booking = Booking.objects.get(id=pk)
    booking.delete()

    messages.add_message(request, messages.INFO,
                         'Your Booking Has Been Deleted')

    if name == 'None':
        return redirect('/my_bookings/')
    else:
        return redirect(f'/restaurant_booking/{name}/')


def delete_account(request):
    user = request.user
    logout(request)
    user.delete()

    messages.add_message(request, messages.INFO,
                         'Your Account Has Been Deleted')

    return redirect('/')
