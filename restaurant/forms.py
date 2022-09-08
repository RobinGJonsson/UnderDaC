from .models import Contact, Booking, Customer
from django import forms


class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ('subject', 'message',)


class BookingForm(forms.ModelForm):
    
    class Meta:
        model = Booking
        fields = ('restaurant', 'guest_count', 'date', 'time',)


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('firstName', 'lastName', 'phone', 'address')

