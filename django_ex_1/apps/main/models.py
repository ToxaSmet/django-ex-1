from django.db import models


class Rental(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'rentals'


class Reservation(models.Model):
    rental = models.ForeignKey(Rental, related_name='reservations', on_delete=models.SET_NULL, null=True)
    checkin_at = models.DateTimeField()
    checkout_at = models.DateTimeField()

    class Meta:
        db_table = 'reservations'
