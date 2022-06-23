from django.contrib import admin

from django_ex_1.apps.main.models import Rental, Reservation


class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'rental_id', 'checkin_at', 'checkout_at')
    raw_id_fields = ('rental',)


admin.site.register(Rental, RentalAdmin)
admin.site.register(Reservation, ReservationAdmin)
