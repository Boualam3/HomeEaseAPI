from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Member


# here we wanna tell django execute function when user is save

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_member_for_new_user(sender, **kwargs):
    if kwargs['created']:
        Member.objects.create(user=kwargs['instance'])


"""
#! This code above  is not called directly we need to override function (ready) in apps model apps.py
then  we import  `core.signals` , it will be called 
"""
