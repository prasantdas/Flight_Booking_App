from django.db import models

class Flight(models.Model):
    flight_name = models.CharField(max_length=100)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    seat_count = models.IntegerField(default=60)
    flight_number = models.IntegerField(unique=True, primary_key=True)

class Booking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    passenger_first_name = models.CharField(max_length=100)
    passenger_last_name = models.CharField(max_length=100)
    passenger_age = models.IntegerField()
    
class MyBookings(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    # fare = models.DecimalField(max_digits=10, decimal_places=2)
    fare = models.CharField(max_length=20)
    # booking_date = models.DateTimeField(auto_now_add=True)
    booking_date = models.CharField(max_length=20)