from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Will complement the default user information upon signup
class Customer(models.Model):
    customer = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, unique=True)

    def __str__(self):
        return str(self.first_name)


class Restaurant(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    image = CloudinaryField('image', default='placeholder')
    map_num = models.IntegerField(null=True)
    open_times_weekdays = models.CharField(max_length=200, null=True)
    open_times_weekends = models.CharField(max_length=200, null=True)

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

    def __str__(self):
        return self.name


class Booking(models.Model):
    customer = models.ForeignKey(User, null=True,
                                 on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    restaurant = models.ForeignKey(
        Restaurant, default=None, null=True, on_delete=models.SET_NULL)
    guest_count = models.IntegerField(default=2, null=True)
    date = models.DateField(default=None)
    time = models.TimeField(max_length=200, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Order(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, null=True, on_delete=models.SET_NULL)
    delivery_time = models.TimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
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
        User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Contact(models.Model):
    customer = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    subject = models.CharField(max_length=200, null=True)
    message = models.TextField(null=True)

    def __str__(self):
        return self.subject
