import datetime

from djtracker import models

from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.conf import settings
from django.template.loader import get_template
from django.template import Context

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = models.UserProfile()
        profile.user = instance
        profile.save()

def update_watchers(sender, instance, created, **kwargs):
    comment = instance
    site = Site.objects.get(id=settings.SITE_ID)
    if comment.content_type.name == "issue":
        issue = comment.content_object
        # we send email to: all watchers, the creator and the current processor...
        email_addresses = list(issue.watched_by.all().values_list('user__email', flat=True))
        if issue.created_by:
            email_addresses.append(issue.created_by.user.email)
        if issue.assigned_to: 
            email_addresses.append(issue.assigned_to.user.email)
        # make list unique
        email_addresses = {}.fromkeys(email_addresses).keys()
        email_title = "DjTracker: [%s]: Issue #%s has been updated by %s" % (comment.content_object.project.slug, 
            comment.content_object.id, comment.user_name)
        t = get_template('djtracker/mail/issue_updated.txt')
        email_body = t.render(Context({'comment': comment, 'site': site}))
        # send mails seperately to protect privacy
        for recipient in email_addresses:
            send_mail(email_title, email_body, settings.ISSUE_ADDRESS, [recipient], fail_silently=False)

def update_modified_time(sender, instance, created, **kwargs):
    comment = instance
    if comment.content_type.name == "issue":
        issue = comment.content_object
        issue.modified_date = datetime.datetime.now()
        issue.save()

post_save.connect(create_profile, sender=User)
post_save.connect(update_watchers, sender=Comment)
post_save.connect(update_modified_time, sender=Comment)

if not hasattr(settings, "WEB_SERVER"):
    settings.WEB_SERVER = 'apache'
