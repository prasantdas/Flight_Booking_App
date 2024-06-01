from django import template

register = template.Library()

@register.filter(name='remaining_seats')
def remaining_seats(flight):
    return flight.seat_count - flight.booking_set.count()
