from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

from core.constants import LANGUAGES, Role


class User(AbstractUser):
    # add required
    email = models.EmailField(unique=True)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.GUEST)
    languages = ArrayField(
        models.CharField(
            max_length=10, choices=LANGUAGES.choices
        ),
        default=LANGUAGES.default_language
        # size=5,
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=225, blank=True, null=True)
    city = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return f"{self.role}: {self.user.username}"


# class Payment(models.Model):
#     card_id = models.CharField(max_length=225)
#     card_placeholder = models.CharField(max_length=225)
#     card_cvv = models.DecimalField(decimal_places=0, max_digits=6)
#     card_expired_date = models.DateField()
#     profile = models.OneToOneField(
#         Profile, on_delete=models.CASCADE, primary_key=True
#     )
