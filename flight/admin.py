from django.contrib import admin
from .models import  Flight, Booking, MyBookings
# Register your models here.
admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(MyBookings)
