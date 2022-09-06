from .models import *
import json


def check_user_auth(request):
    # Check if user is logged in
    if request.user.is_authenticated:
        customer = request.user
        return customer
    else:
        return False


def cart_data(request):
    '''Return the cart item count corresponding to current user if they exist otherwise create an empty order'''

    customer = check_user_auth(request)
    if customer is not False:
        print('""""""""""""""""""""""""""""""""""""""""""""""', customer)
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
