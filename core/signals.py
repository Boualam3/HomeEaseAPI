"""
JUST FOR RESOURCE PURPOSE 
I WAS USE THAT TO CREATE PROFILE OBJECT  WHENEVER USER REGISTERED `POST SAVE` BUT ITS NOT BETTER APPROACH 

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


# when user is created ,so profile object will created

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender,  instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



#! This code above  is not called directly we need to override function (ready) in apps class (apps.py)
then  we import  `core.signals` , it will be called 
"""
