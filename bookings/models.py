import uuid

from django.db   import models

from core.models import TimeStampModel

class Booking(TimeStampModel):
    booking_code  = models.UUIDField(default=uuid.uuid4, editable=False)
    checkin_date  = models.DateField()
    checkout_date = models.DateField()
    user          = models.ForeignKey('users.User', on_delete=models.CASCADE)
    petsitter     = models.ForeignKey('petsitters.Petsitter', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bookings'


