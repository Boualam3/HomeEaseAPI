from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	# add required
	email=models.EmailField(unique=True)

class Member(models.Model):
    class Role(models.TextChoices):
        HOST = 'HOST', 'Host'
        GUEST = 'GUEST', 'Guest'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)

    def __str__(self):
        return f"{self.role}: {self.user.username}"

class Address(models.Model):
    street = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    zip = models.DecimalField(decimal_places=0, max_digits=6)
    customer = models.OneToOneField(
        Member, on_delete=models.CASCADE, primary_key=True)