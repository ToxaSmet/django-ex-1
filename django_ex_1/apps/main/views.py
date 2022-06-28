from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from django_ex_1.apps.main.models import Reservation


class IndexView(View):
    template_name = 'index.html'
    per_page = 10

    def get(self, request, *args, **kwargs):
        reservations = Reservation.objects.select_related('rental').order_by('rental__name', 'checkin_at')

        # paginator = Paginator(reservations, per_page=self.per_page)
        # page = paginator.get_page(request.GET.get('page'))

        context = {
            # 'reservations_page': page,
            'reservations_page': reservations,
        }
        return render(request, self.template_name, context)
