from .models import Contact, Booking, Customer
import datetime
from django import forms
from django.core.validators import MinValueValidator


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('email', 'subject', 'message',)


class BookingForm(forms.ModelForm):
    # Only allow to pick dates from today and forward
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),
                           validators=[MinValueValidator(datetime.date.today)])
    time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    class Meta:
        model = Booking
        fields = ('first_name', 'last_name', 'phone',
                  'email', 'guest_count', 'date', 'time',)


class SignupForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone', 'address')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        customer, created = Customer.objects.get_or_create(customer=user)

        customer.customer = user
        customer.first_name = self.cleaned_data['first_name']
        customer.last_name = self.cleaned_data['last_name']
        customer.email = self.cleaned_data['email']
        customer.phone = self.cleaned_data['phone']
        customer.address = self.cleaned_data['address']
        customer.save()
