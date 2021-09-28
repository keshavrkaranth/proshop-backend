from django.db.models.signals import  pre_save
from django.dispatch import receiver
from . import models


@receiver(pre_save, sender=models.User)
def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email !="":
        user.username = user.email
