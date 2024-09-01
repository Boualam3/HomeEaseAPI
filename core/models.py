from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # add required
    email = models.EmailField(unique=True)


class Profile(models.Model):
    class Role(models.TextChoices):
        HOST = 'HOST', 'Host'
        GUEST = 'GUEST', 'Guest'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.GUEST)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=225, blank=True, null=True)
    city = models.CharField(max_length=225, blank=True, null=True)
    zip = models.DecimalField(
        decimal_places=0, max_digits=6, blank=True, null=True)

    def __str__(self):
        return f"{self.role}: {self.user.username}"

# I don't think user will need many addresses to link with their profile , if so uncomment this model
# class Address(models.Model):
#     street = models.CharField(max_length=225)
#     city = models.CharField(max_length=225)
#     zip = models.DecimalField(decimal_places=0, max_digits=6)
#     profile = models.OneToOneField(
#         Profile, on_delete=models.CASCADE, primary_key=True
#     )
