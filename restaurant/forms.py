from .models import Contact, Booking
from django import forms


class ContactForm(form.ModelForm):
    
    class Meta:
        model = Contact
        fields = ('subject', 'message',)

class BookingForm(form.ModelForm):
    
    class Meta:
        model = Booking
        fields = ('restaurant', 'guest_count', 'datetime',)

