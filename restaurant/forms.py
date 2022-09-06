from .models import Contact, Booking
from django import forms


class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ('subject', 'message',)


class BookingForm(forms.ModelForm):
    
    class Meta:
        model = Booking
        fields = ('restaurant', 'guest_count', 'datetime',)

