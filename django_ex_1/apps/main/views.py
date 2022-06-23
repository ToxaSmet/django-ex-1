from django.db.models import Prefetch
from django.shortcuts import render
from django.views import View

from django_ex_1.apps.main.models import Rental, Reservation


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        prefetch = Prefetch('reservations', queryset=Reservation.objects.order_by('checkin_at'))
        rentals = Rental.objects.prefetch_related(prefetch).all()

        context = {
            'rentals': rentals,
        }
        return render(request, self.template_name, context)
