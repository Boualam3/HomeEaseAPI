from django.db import models
from core.models import Profile
from properties.models import Property


class Calendar(models.Model):
    property = models.OneToOneField(
        Property, related_name="calendar", on_delete=models.CASCADE
    )
    from_date = models.DateField(auto_now_add=True)
    to_date = models.DateField(auto_now_add=True)
    locked_dates = models.JSONField(default=dict)


class Appointment(models.Model):
    class Status(models.TextChoices):
        Pending = "PENDING", "Pending"
        Confirmed = "Confirmed", "Confirmed"
        Canceled = "Canceled", "Canceled"
    user = models.ForeignKey(
        Profile, related_name="appointments", on_delete=models.PROTECT)
    
    #TODO Maybe we could make Only properties associated with Appointment.Status Canceled can be deleted otherwise it protected
    property = models.ForeignKey(
        Property, related_name="appointments", on_delete=models.PROTECT)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.Pending)


class Booking(models.Model):
    appointment = models.ForeignKey(
        Appointment, on_delete=models.SET_NULL, null=True)


"""
              property
                 |
              available            
               /y      \n
create Appointment     Send email notification when become available
        |status=P
update payment data in profile
        |
request stripe api for payment
      /             \        
success            failure         
"""
