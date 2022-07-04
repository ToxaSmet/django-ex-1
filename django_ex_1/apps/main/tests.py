import math
import random

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from django_ex_1.apps.main.models import Rental, Reservation
from django_ex_1.apps.main.views import IndexView
from django_ex_1.utils import generate_random_string


class IndexTest(TestCase):
    rentals_to_create_count = 10

    def create_random_data(self):
        """
        NOTE: not best approach to randomize initial data - better to pre-create fixtures
        """

        now = timezone.now()

        for i in range(self.rentals_to_create_count):
            Rental.objects.create(name=generate_random_string())

        for rental in Rental.objects.all():
            for i in range(random.randint(1, 5)):
                checkin = timezone.make_aware(
                    timezone.datetime(year=now.year, month=now.month, day=random.randint(1, 15))
                )
                checkout = timezone.make_aware(
                    timezone.datetime(year=now.year, month=now.month, day=random.randint(15, 28))
                )
                Reservation.objects.create(
                    rental=rental,
                    checkin_at=checkin,
                    checkout_at=checkout,
                )

    def setUp(self):
        self.create_random_data()
        return super().setUp()

    def test_access(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_data_exists(self):
        response = self.client.get(reverse('index'))
        reservations = response.context['reservations_page']
        self.assertGreater(len(reservations), 0)

    def _test_reservation_previous_id(self, page=None):
        data = None
        if page:
            data = {'page': page}

        response = self.client.get(reverse('index'), data=data)
        reservations = response.context['reservations_page']
        for reservation in reservations:

            previous_reservation = Reservation.objects.filter(
                rental_id=reservation.rental_id,
                checkin_at__lte=reservation.checkin_at
            ).exclude(id=reservation.id).order_by('-checkin_at', '-id').only('id').first()

            if previous_reservation:
                self.assertEqual(previous_reservation.id, reservation.previous_id)
                self.assertGreaterEqual(reservation.checkin_at, previous_reservation.checkin_at)
            else:
                self.assertIsNone(reservation.previous_id)

    def test_reservation_previous_id(self):
        self._test_reservation_previous_id()

    def test_reservation_previous_id_on_pages(self):
        c = Reservation.objects.count()
        per_page = IndexView.per_page
        pages = math.ceil(c / per_page)
        for p in range(pages):
            self._test_reservation_previous_id(p)

