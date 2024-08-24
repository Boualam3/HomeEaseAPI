from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	# add required
	email=models.EmailField(unique=True)

# Create your models here.
