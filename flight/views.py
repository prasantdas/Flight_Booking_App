from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as DjangoUser
from .models import Flight, Booking, MyBookings
from django.db.models import Q
from django.contrib.auth import REDIRECT_FIELD_NAME
from .forms import BookingForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
import json
from django.http import HttpResponseForbidden
from django.db import transaction


def home(request):
    return render(request, 'home.html')

def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home')
    return render(request, 'home')

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def userSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('home')

        if not is_valid_email(email):
            messages.error(request, "Invalid email format. Please use a valid email.")
            return redirect('home')

        if DjangoUser.objects.filter(username=username).exists() or DjangoUser.objects.filter(email=email).exists():
            messages.error(request, "Username or email already exists. Please choose a different one.")
            return redirect('home')

        # Create the user
        user = DjangoUser.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')


def flightSearch(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        number = request.POST.get('number', '')
        date = request.POST.get('date', '')
        from_location = request.POST.get('from_location', '')
        to_location = request.POST.get('to_location', '')

        query = Q()
        if from_location and to_location:
            query |= Q(from_location__icontains=from_location, to_location__icontains=to_location)
            flights = Flight.objects.filter(query)
            return render(request, 'flightSearch.html', {'flights': flights})

        if name:
            query |= Q(flight_name__icontains=name)

        if number:
            query |= Q(flight_number__icontains=number)

        if date:
            query |= Q(date__icontains=date)

        flights = Flight.objects.filter(query)

        return render(request, 'flightSearch.html', {'flights': flights})

    return render(request, 'flightSearch.html', {'flights': None})


def myBookings(request):
    if request.user.is_authenticated: 
        mybookings = MyBookings.objects.filter(user=request.user)
        return render(request, 'myBookings.html', {'bookings': mybookings})

def bookTicket(request, flight_number):
    flight = Flight.objects.get(flight_number=flight_number)
    user = request.user

    if flight.seat_count - Booking.objects.filter(flight=flight).count() <= 0:
        return render(request, 'booking.html', {'error': 'No available seats on this flight.'})

    if request.method == 'POST':
        total_passengers = int(request.POST.get('total_passengers', 0))
        passenger_data_json = request.POST.get('passenger_data')

        if total_passengers > 0 and passenger_data_json:
            passenger_data = json.loads(passenger_data_json)

            for data in passenger_data:
                form = BookingForm(data)

                if form.is_valid():
                    first_name = form.cleaned_data.get('passenger_first_name')
                    last_name = form.cleaned_data.get('passenger_last_name')
                    age = form.cleaned_data.get('passenger_age')

                    if first_name and last_name and age:
                        booking = Booking.objects.create(
                            user=user,
                            flight=flight,
                            passenger_first_name=first_name,
                            passenger_last_name=last_name,
                            passenger_age=age
                        )
                        booking.save()
                else:
                    print(form.errors)
                    pass

            return render(request, 'booking.html', {'success': 'Booking successful!'})
        else:
            return render(request, 'booking.html', {'error': 'No passengers added.'})

    return render(request, 'booking.html', {'flight': flight})

def bookForm(request):
    # flight = Flight.objects.get(flight_number=flight_number)
    # flight = request.POST['flight_number']
    # fare= request.POST['fare']
    
    
    
    from_location=request.POST['from_location']
    to_location=request.POST['to_location']
    date=request.POST['date']
    flight_number=request.POST['flight_number']
    fare=request.POST['fare']
    
    data = {
        'flight_number': flight_number,
        'fare': fare,
        'from_location':from_location,
        'to_location':to_location,
        'date':date
    }
    return render(request, 'bookForm.html', {'data': data})
    # return HttpResponse(fare)


def payment(request):
    # return  render(request, 'payment.html')
    # if request.user.is_authenticated:
    #     if request.method=='POST':
    #         count=int(request.POST['total_passengers'])
    #         fare=request.POST['fare']
    #         amount=count*fare
    #         return render(request, 'payment.html', {'totprice': amount})
    #     return  render(request, 'payment.html')
    # return render(request,'home.html')
    if request.user.is_authenticated:
        if request.method == 'POST':
            user=request.user
            from_location=request.POST['from_location']
            to_location=request.POST['to_location']
            date=request.POST['date']
            flight_number=request.POST['flight_number']
            passenger_data = request.POST.getlist('passenger_data')
            # fare=request.POST.get('fare', '')
            fare = request.POST['fare']
            # count = len(passenger_data)
            # amount = count * fare
            # amount = fare
            MyBookings.objects.create(
                user = user,
                flight_number=flight_number,
                from_location=from_location,
                to_location=to_location,
                fare=fare,
                booking_date=date
            )
            # MyBookings.save()
            return render(request, 'payment.html', {'totprice': fare})
        return render(request, 'payment.html')
    return redirect('home')  # Assuming you have a URL named 'home'


def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('adminDashboard')
        else:
            return render(request, 'admin/login.html', {'error': 'Invalid credentials'})

    return render(request, 'admin/login.html')



def adminDashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    return render(request, 'admin/dashboard.html')


def addFlight(request):
    if request.method == 'POST':
        flight_name = request.POST['flight_name']
        flight_number = request.POST['flight_number']

        if Flight.objects.filter(flight_name=flight_name, flight_number=flight_number).exists():
            return render(request, 'admin/addFlight.html', {'error': 'Flight with the same name and number already exists.'})

        date = request.POST['date']
        seat_count = request.POST['seat_count']
        from_location = request.POST['from_location']
        to_location = request.POST['to_location']
        fare = request.POST['fare']

        Flight.objects.create(
            flight_name=flight_name,
            flight_number=flight_number,
            date=date,
            seat_count=seat_count,
            from_location=from_location,
            to_location=to_location,
            fare=fare
        )

        return redirect('adminDashboard')

    return render(request, 'admin/addFlight.html')


def viewBookings(request):
    flights = Flight.objects.all()
    bookings = None

    if request.method == 'POST':
        flight_number = request.POST.get('flight_number', '')
        flight_name = request.POST.get('flight_name', '')
        date = request.POST.get('date', '')

        query = Q()

        if flight_number:
            query |= Q(flight__flight_number__icontains=flight_number)

        if flight_name:
            query |= Q(flight__flight_name__icontains=flight_name)

        if date:
            query |= Q(flight__date__icontains=date)

        bookings = Booking.objects.filter(query)

    return render(request, 'admin/viewBookings.html', {'bookings': bookings, 'flights': flights})

def userLogout(request):
    logout(request)
    return redirect('home')

def adminLogout(request):
    logout(request)
    return redirect('adminLogin')

def flights(request):
    flights = Flight.objects.all()
    return render(request, 'admin/flights.html', {'flights': flights})


def cancelBooking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.user:
        return HttpResponseForbidden("You don't have permission to cancel this booking.")

    with transaction.atomic():
        # Delete the booking
        booking.delete()

    return redirect('myBookings')


def processing(request):
    return render(request,'processing.html')