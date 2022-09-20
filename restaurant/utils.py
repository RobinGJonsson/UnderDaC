from .models import Order, Booking, MenuItem, Restaurant
import json


def check_user_auth(request):
    # Check if user is logged in
    if request.user.is_authenticated:
        customer = request.user
        return customer
    else:
        return False


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


def booking_validation(form, customer, restaurant):
    new_booking = form.save(commit=False)
    booking_date = new_booking.date
    booking_time = new_booking.time

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

    # Don't allow bookings 3 hours before or after an existing booking
    # belonging to the current customer
    for booking in customer_bookings:
        if booking.date == booking_date:
            booking.time.hour*60 + booking.time.minute
            booking_time.hour*60 + booking_time.minute
            hour_time_dif = abs((
                booking.time.hour*60 + booking.time.minute
            ) - (booking_time.hour*60 + booking_time.minute)) / 60
            if hour_time_dif <= 3 and (new_booking.id != booking.id):
                return False

    return new_booking
