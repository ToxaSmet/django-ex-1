from django import template

register = template.Library()


@register.filter
def get_previous_reservation_id(reservations, index):
    if index >= len(reservations):
        return None

    if index > 0:
        return reservations[index - 1].id
    return None


@register.filter
def to_list(a):
    return list(a)
