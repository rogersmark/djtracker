import datetime

from djtracker import models, utils
from djtracker.signals import issue_created, issue_updated, issue_commented
from djtracker_comments.models import CommentWithIssueStatus

from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.conf import settings
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

def create_profile(sender, instance, created, **kwargs):    
    if created:
        profile = models.UserProfile()
        profile.user = instance
        profile.save()

def _get_notification_context(issue, request):
    site = Site.objects.get_current()
    user = request.user.get_full_name() if request and request.user else _('anonymous user')
    return Context({'issue': issue, 'project': issue.project, 'site': site, 'request' : request, 'user': user })

def _get_notification_recipients(issue, request):
    # all watchers of this issue
    email_addresses = list(issue.watched_by.all().values_list('user__email', flat=True))
    # all watchers of the project
    [email_addresses.append(mail) for mail in issue.project.watched_by.all().values_list('user__email', flat=True)]
    # creator
    if issue.created_by:
        email_addresses.append(issue.created_by.user.email)    
    # current assignee
    if issue.assigned_to:
        email_addresses.append(issue.assigned_to.user.email)
    # make list unique
    email_addresses = {}.fromkeys(email_addresses).keys()    
    # remove current user from the list of recipients
    # (you don't need an email telling you what you did just minutes before)
    if request and request.user:
        try:
            email_addresses.remove(request.user.email)
        except ValueError:
            pass
    return email_addresses

def _send_notifications(template, context):
    for recipient in _get_notification_recipients(context['issue'], context['request']):        
        msg = template.render_to_mail(context)
        msg.from_address = settings.ISSUE_ADDRESS    
        msg.to = [recipient,]
        msg.send(fail_silently=True)

def notify_issue_created(sender, issue, request, **kwargs):
    context = _get_notification_context(issue, request)
    template = utils.MailTemplate('djtracker/mail/issue_created.mail')
    _send_notifications(template, context)    

def notify_issue_updated(sender, issue, updated_fields, request, **kwargs):
    context = _get_notification_context(issue, request)
    context['updated_fields'] = updated_fields        
    template = utils.MailTemplate('djtracker/mail/issue_updated.mail')
    _send_notifications(template, context)
    
def notify_issue_commented(sender, comment, issue, status_change, request, **kwargs):
    context = _get_notification_context(issue, request)
    context['comment'] = comment
    context['comment_user_name'] = comment.user_name
    context['status_change'] = status_change
    template = utils.MailTemplate('djtracker/mail/issue_commented.mail')
    _send_notifications(template, context)
    
post_save.connect(create_profile, sender=User)

issue_created.connect(notify_issue_created, dispatch_uid='djtracker.notify_issue_created')
issue_updated.connect(notify_issue_updated, dispatch_uid='djtracker.notify_issue_updated')
issue_commented.connect(notify_issue_commented, dispatch_uid='djtracker.notify_issue_commented')

if not hasattr(settings, "WEB_SERVER"):
    settings.WEB_SERVER = 'apache'
