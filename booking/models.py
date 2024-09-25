from django.db import models

from properties.models import Property


class Calendar(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
#     opened_dates = models.ArrayField()
#     locked_dates = models.ArrayField()


class Appointment(models.Model):
    pass


class Booking(models.Model):
    pass
