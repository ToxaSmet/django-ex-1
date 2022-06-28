from django import template

register = template.Library()


@register.filter
def get_previous_reservation_id(reservations, index):
    if index >= len(reservations):
        return None

    if index <= 0:
        return None

    previous_reservation = reservations[index - 1]
    reservation = reservations[index]
    if previous_reservation.rental.name == reservation.rental.name:  # so it's same rental
        return previous_reservation.id

    return None
