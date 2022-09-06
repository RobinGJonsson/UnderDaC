from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Will complement the default user information upon signup
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user.get_full_name()


class Restaurant(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    image = CloudinaryField('image', default='placeholder')
    map = models.IntegerField(null=True)
    open_times = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    categories = (
        ('Kids Menu', 'Kids Menu'),
        ('Menu', 'Menu'),
        ('Vegan Menu', 'Vegan Menu')
    )
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    image = CloudinaryField('image', default='placeholder')
    category = models.CharField(max_length=200, choices=categories, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def half_price(self):
        return self.price / 2

    # Catch error of no image in menu item, which otherwise would crash the page
    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''

        return url

    def __str__(self):
        return self.name


class Booking(models.Model):
    customer = models.ForeignKey(Customer, null=True,
                                 on_delete=models.SET_NULL)
    restaurant = models.ForeignKey(
        Restaurant, default=None, null=True, on_delete=models.SET_NULL)
    guest_count = models.IntegerField(default=2, null=True)
    datetime = models.DateTimeField(null=True)
    # date = models.DateField()
    # time = models.TimeField(max_length=200, null=True)

    def __str__(self):
        return self.customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, null=True, on_delete=models.SET_NULL)
    delivery_time = models.TimeField(null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)

    @property
    def get_cart_total_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])

        return total

    @property
    def get_cart_item_count(self):
        orderitems = self.orderitem_set.all()
        quantity = sum([item.quantity for item in orderitems])

        return quantity

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True)

    @property
    def get_total(self):
        return self.item.price * self.quantity

    def __str__(self):
        return self.item.name


class DeliveryInfo(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    firstName = models.CharField(max_length=200, null=True)
    lastName = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Contact(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, null=True)
    message = models.TextField(null=True)

    def __str__(self):
        return self.subject
