from djtracker import models

from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.conf import settings

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = models.UserProfile()
        profile.user = instance
        profile.save()

def update_watchers(sender, instance, created, **kwargs):
    comment = instance
    site = Site.objects.get(id=settings.SITE_ID)
    if comment.content_type.name == "issue":
        users = comment.content_object.watched_by.all()
        email_addresses = []
        for x in users:
            email_addresses.append(x.user.email)
        email_title = "%s has been updated by %s" % (comment.content_object.name, 
            comment.name)
        email_message = """
            Hello,
            This message is to inform you that the issue you are watching has 
            been updated. The update is as follows:

            -------------------------------
            %s
            -------------------------------

            You can view this issue as http://%s%s

            Thanks,
            DjTracker Administration
            """ % (comment.comment, site, 
                comment.content_object.get_absolute_url())
        send_mail(email_title, email_message, settings.ISSUE_ADDRESS,
            email_addresses, fail_silently=False)

post_save.connect(create_profile, sender=User)
post_save.connect(update_watchers, sender=Comment)
