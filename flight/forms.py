from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['passenger_first_name', 'passenger_last_name', 'passenger_age']
    