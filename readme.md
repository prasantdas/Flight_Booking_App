```markdown
# Flight Booking App

Flight Booking App is a web application that allows users to search for flights, book tickets, and view their previous bookings. It also provides an admin dashboard to manage flights and view booking details.

## Features

### User

1. **Login/Signup:**
   - Users can create an account or log in to an existing account.

2. **Search Flights:**
   - Search for flights based on flight name, number, and date.
   - Logging in is not required for searching.

3. **Book Flight:**
   - Users can book flights for up to 5 passengers at a time.
   - Booking requires user login.

4. **View Previous Bookings:**
   - Users can view details of their previous bookings.

### Admin

1. **Login:**
   - Admins can log in to access the admin panel.

2. **Dashboard:**
   - Admins have access to a dashboard with an overview of the system.

3. **Add Flights:**
   - Admins can add new flights to the system.

4. **View Bookings:**
   - Admins can view booking details based on flight name, number, and date.

## Getting Started

### Prerequisites

- Python (version 3.6 or higher)
- Django
- Git

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/flight-booking-app.git
cd flight-booking-app
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Create a superuser (admin) account:

```bash
python manage.py createsuperuser
```

5. Start the development server:

```bash
python manage.py runserver
```

Visit [Flight Booking App](https://flightbooking-l2rc.onrender.com/) to access the website.

### Admin Credentials

- **Username:** admin
- **Password:** admin123

Visit [Flight Booking App Admin](https://flightbooking-l2rc.onrender.com/myadmin/login) to access the admin pannel.

