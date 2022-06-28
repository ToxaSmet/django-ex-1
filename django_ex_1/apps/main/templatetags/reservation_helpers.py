from django import template

register = template.Library()


@register.filter
def get_previous_reservation_id(page, index):
    reservations = page.paginator.object_list_with_previous

    # NOTE: when using PreviousObjectPaginator we must increase index,
    # as paginator has one more object in its object_list_with_previous property,
    # in order to match indexes with page objects
    index += 1
    if index >= len(reservations):
        return None

    if index <= 0:
        return None

    previous_reservation = reservations[index - 1]
    if not previous_reservation:
        return None

    reservation = reservations[index]
    if previous_reservation.rental.name == reservation.rental.name:  # so it's same rental
        return previous_reservation.id

    return None
