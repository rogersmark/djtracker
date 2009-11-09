from djtracker import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = models.UserProfile()
        profile.user = instance
        profile.save()

post_save.connect(create_profile, sender=User)

