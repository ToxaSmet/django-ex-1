from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from django_ex_1.apps.main.models import Reservation


class PreviousObjectPaginator(Paginator):
    """
    Returns objects like origin Paginator,
    but saves one more previous object in object_list_with_previous
    for further previous_id search
    """

    object_list_with_previous = []

    def page(self, number):
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count

        if bottom == 0:
            self.object_list_with_previous = [None, *self.object_list[bottom:top]]
        else:
            self.object_list_with_previous = self.object_list[bottom-1:top]
        return self._get_page(self.object_list_with_previous[1:], number, self)


class IndexView(View):
    template_name = 'index.html'
    per_page = 10

    def get(self, request, *args, **kwargs):
        reservations = Reservation.objects.select_related('rental').order_by('rental__name', 'checkin_at')

        paginator = PreviousObjectPaginator(reservations, per_page=self.per_page)
        page = paginator.get_page(request.GET.get('page'))

        context = {
            'reservations_page': page,
        }
        return render(request, self.template_name, context)
