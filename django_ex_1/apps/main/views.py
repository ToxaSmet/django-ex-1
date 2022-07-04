from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef
from django.shortcuts import render
from django.views import View

from django_ex_1.apps.main.models import Reservation


class IndexView(View):
    template_name = 'index.html'
    per_page = 10

    def get(self, request, *args, **kwargs):
        previous_ids_query = Reservation.objects.filter(
            rental_id=OuterRef('rental_id'),
            checkin_at__lte=OuterRef('checkin_at')
        ).exclude(id=OuterRef('id')).order_by('-checkin_at', '-id').values('id')

        reservations = Reservation.objects.select_related('rental').order_by('rental__name', 'checkin_at') \
            .annotate(previous_id=Subquery(previous_ids_query[:1]))

        paginator = Paginator(reservations, per_page=self.per_page)
        page = paginator.get_page(request.GET.get('page'))

        context = {
            'reservations_page': page,
        }
        return render(request, self.template_name, context)
