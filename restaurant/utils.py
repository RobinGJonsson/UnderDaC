from .models import Order, Booking, MenuItem, Restaurant
import json
import datetime
from django.contrib import messages


def check_user_auth(request):
    ''' Returns the user if  the user is authenticated
    otherwise it returns False '''
    # Check if user is logged in
    if request.user.is_authenticated:
        customer = request.user
        return customer
    else:
        return False


def hour_dif(time1, time2):
    '''Returns the hour difference between 2 time objects'''

    time1_minutes = time1.hour*60 + time1.minute
    time2_minutes = time2.hour*60 + time2.minute

    hour_dif = abs(time1_minutes - time2_minutes) / 60
    return hour_dif


def cart_data(request):
    '''Return the cart item count corresponding to
    current user if they exist otherwise create an empty order'''

    customer = check_user_auth(request)
    if customer is not False:
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_count = order.get_cart_item_count
    else:
        # If cart is not in cookies catch the exception and set it to {}
        try:
            print('cookie:', request.COOKIES)
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}

        order = {'get_cart_total_price': 0,
                 'get_cart_item_count': 0}
        items = []
        cart_count = order['get_cart_item_count']

        for cart_item in cart:
            print(cart[cart_item]['quantity'])
            cart_count += cart[cart_item]['quantity']
            menu_item = MenuItem.objects.get(id=cart_item)
            total = (menu_item.price * cart[cart_item]['quantity'])

            order['get_cart_item_count'] += cart[cart_item]['quantity']
            order['get_cart_total_price'] += total

            item = {
                'menu_item': {'item_id': menu_item.id,
                              'name': menu_item.name,
                              'price': menu_item.price,
                              'imageURL': menu_item.imageURL
                              },
                'quantity': cart[cart_item]['quantity'],
                'total': total
            }

            items.append(item)

    # print(cart)

    return {'order': order, 'items': items, 'cart_count': cart_count}


def navbar(request, name=None):
    '''Returns the context necessary to populate the 
    navbar with dynamic information'''

    customer = check_user_auth(request)
    cart_info = cart_data(request)
    cart_count = cart_info['cart_count']

    if name is not None:
        restaurant = Restaurant.objects.get(name=name)
        customer_bookings = Booking.objects.filter(
            customer=customer, restaurant=restaurant).order_by('date')
    else:
        customer_bookings = Booking.objects.filter(
            customer=customer).order_by('date')

    context = {'cart_count': cart_count}
    if customer_bookings:
        context['customer_bookings'] = customer_bookings
    return context


def tables_available(new_booking, restaurant):
    ''' Returns True if there are tables available and False if there aren't'''

    restaurant_guests_already_booked = 0

    for booking in Booking.objects.filter(date=new_booking.date):
        hour_difference = hour_dif(booking.time, new_booking.time)

        # If the hour difference is less than three hours we assume the table is free
        if hour_difference <= 3:
            restaurant_guests_already_booked += booking.guest_count

    # Catch exception if there are no guests already booked
    try:
        tables_available = (
            (restaurant.tables * 2) - restaurant_guests_already_booked) / 2
    except ZeroDivisionError:
        tables_available = restaurant.tables

    if tables_available / (new_booking.guest_count / 2) < 1:
        return False
    else:
        return True


def booking_validation(form, customer, restaurant):
    '''Returns the booking if there are tables available and the 
    customer doesn't have an active booking within 3 hours of the 
    new booking, otherwise it will return a string describing why not.
    '''
    new_booking = form.save(commit=False)
    now = datetime.datetime.now()

    # Get if the correct open times of the day
    open_times = restaurant.open_times_weekdays if now.weekday(
    ) < 5 else restaurant.open_times_weekends
    open_times = open_times.split(' - ')

    # Convert the opening hours to open and closing times
    open_hour = datetime.datetime.strptime(open_times[0], '%H').time()
    closing_hour = datetime.datetime.strptime(open_times[1], '%H').time()

    if customer:
        customer_bookings = Booking.objects.filter(
            customer=customer, restaurant=restaurant)
    else:
        customer_bookings = Booking.objects.filter(
            first_name=new_booking.first_name,
            last_name=new_booking.last_name,
            phone=new_booking.phone,
            email=new_booking.email,
            restaurant=restaurant)

    # Check that booking time is not passed and that it is not outside of open times
    if new_booking.date == now.date():
        if new_booking.time < now.time():
            return {'message': 'Invalid Time',
                    'current_time': now.time().strftime('%H:%M')}

    # Don't allow bookings 3 hours before or after an existing booking
    # belonging to the current customer
    for booking in customer_bookings:
        if booking.date == new_booking.date:
            hour_difference = hour_dif(booking.time, new_booking.time)

            if hour_difference <= 3 and (new_booking.id != booking.id):
                return {'message': 'Too Close'}

    if new_booking.time < open_hour or new_booking.time > closing_hour:
        return {'message': 'Not Open'}

    if tables_available(new_booking, restaurant):
        return new_booking
    else:
        return {'message': 'No Tables'}


def displpay_msg(request, msg_key, current_time=None,
                 level=messages.WARNING):
    msg_dict = {
        'No Tables': '''Unfortunatly There Are No 
                        Tables Available at Your Chosen Time''',
        'Too Close': '''The Time of Your Booking is 
                        Too Close to Another Booking You 
                        Have. Bookings Must Be at 
                        Least 3 Hours Apart''',
        'Invalid Time': f'''Please Pick a Time after 
                            {current_time}''',
        'Not Open': '''We Are Unfortunatly Not Open at 
                       Your Chosen Time, Please Chose a 
                       Different Time''',
        'Booking Success': '''The Booking Confirmation Has
                            Been Sent to Your Email''',
        'Booking Update': '''Your Booking Has Been Updated''',
        'Add Item': 'Item Added To Your Order',
        'Contact': '''Your Message Has Been Sent, We Will Get
                      Back To You Shortly''',
        'Update Details': 'Your Details Have Been Updated',
        'Delete Booking': 'Your Booking Has Been Deleted',
        'Delete Account': 'Your Account Has Been Deleted'
    }

    messages.add_message(request, level, msg_dict[msg_key])
