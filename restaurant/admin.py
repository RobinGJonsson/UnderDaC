from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *



class Filter(admin.ModelAdmin):
    list_filter = ('date',)

admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(Booking, Filter)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryInfo)

