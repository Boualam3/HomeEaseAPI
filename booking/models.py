from django.db import models
from django.utils import timezone

from core.models import Profile
from properties.models import Property

# Create your models here.
class Booking(models.Model):        
    STATUS_CHOICES = (
        ('Pending', 'pending'),
        ('Canceled', 'canceled'),
        ('Reserved', 'reserved'),
    )
     
    checkin =  models.DateField(timezone.now)
    checkout = models.DateField(timezone.now)
    number_guests = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='Pending')
    property = models.ForeignKey(Property, on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)


class Order(models.Model):
    total_amount = models.DecimalField(max_digits=35, decimal_places=2)
    vat = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2)
    fees = models.DecimalField(max_digits=12, decimal_places=2)
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT)

   
