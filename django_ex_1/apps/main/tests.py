import random

from django.template.defaultfilters import striptags
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from django_ex_1.apps.main.models import Rental, Reservation
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

    def parse_html_to_reservations(self, html_content):
        html_content = html_content.replace('\\n', '').replace('\'', '')
        table_body = html_content.split('<tbody>')[1]
        reservations = table_body.split('<tr>')[1:]
        res = []
        for reservation in reservations:
            rows = reservation.split('<td>')[1:]
            res.append({
                'rental_name': striptags(rows[0]).strip(),
                'id': striptags(rows[1]).strip(),
                'checkin': striptags(rows[2]).strip(),
                'checkout': striptags(rows[3]).strip(),
                'previous_id': striptags(rows[4]).strip(),
            })
        return res

    def setUp(self):
        self.create_random_data()
        return super().setUp()

    def test_access(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_data_exists(self):
        response = self.client.get(reverse('index'))
        reservations = response.context['reservations_page']
        self.assertEqual(len(reservations), Reservation.objects.count())

    def test_reservation_previous_id(self):
        response = self.client.get(reverse('index'))
        reservations = self.parse_html_to_reservations(str(response.content))
        previous_reservation = reservations[0]
        for reservation in reservations[1:]:
            if previous_reservation['rental_name'] == reservation['rental_name']:
                self.assertEqual(previous_reservation['id'], reservation['previous_id'])

                previous_checkin = timezone.datetime.strptime(previous_reservation['checkin'], '%Y-%m-%d')
                checkin = timezone.datetime.strptime(reservation['checkin'], '%Y-%m-%d')
                self.assertGreaterEqual(checkin, previous_checkin)
            else:
                self.assertEqual('-', reservation['previous_id'])

            previous_reservation = reservation

