import imaplib
import re
import StringIO
import rfc822

from djtracker import models, utils

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class Command(NoArgsCommand):
    help = "Polls your IMAP account for new issue emails"

    def init_imap_client(self):
        if settings.ISSUE_PARSE_EMAIL is False:
            return

        if settings.ISSUE_MAIL_SSL:
            self.handler = imaplib.IMAP4_SSL(settings.ISSUE_MAIL_HOST)
            self.handler.login(
                settings.ISSUE_MAIL_USER,
                settings.ISSUE_MAIL_PASSWORD
            )
        else:
            self.handler = imaplib.IMAP4(settings.ISSUE_MAIL_HOST)
            self.handler.authenticate(
                settings.ISSUE_MAIL_USER,
                settings.ISSUE_MAIL_PASSWORD
            )
        self.handler.select("INBOX")
        self.search_emails()

    def search_emails(self):
        typ, msgnums = self.handler.search(None, '(UNSEEN SUBJECT "DjTracker")')
        for num in msgnums[0].split():
            typ, data = self.handler.fetch(num, '(RFC822)')
            match = re.search("\[[\w-]+\]", data[0][1])

            if match:
                file = StringIO.StringIO(data[0][1])
                message = rfc822.Message(file)
                self.parse_message(message, data[0][1])

    def parse_message(self, message, raw_data):
        ## Get project slug
        match = re.search("\[[\w-]+\]", message['subject'])
        project_slug = match.group().lstrip('[').rstrip(']')

        ## Get email address
        match = re.search('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+',
                               message['from'])
        email_addy = match.group()
        ## Get Issue Number (if exists)
        match = re.search("Issue #[\d]+", message['subject'])
        if match:
            issue_string = match.group()
            issue_num = issue_string.lstrip("Issue #")
            issue_title = subject[match.end():].lstrip(" - ")
        else:
            issue_num = None
            match = re.search("\[[\w-]+\]", message['subject'])
            issue_title = message['subject'][match.end():]

        ## Get our django objects
        try:
            project = models.Project.objects.get(slug=project_slug)
        except ObjectDoesNotExist:
            return

        try:
            user = User.objects.get(email=email_addy)
        except ObjectDoesNotExist:
            user = None

        try:
            issue = models.Issue.objects.get(id=issue_num)
        except ObjectDoesNotExist:
            issue = None

        can_view, can_edit, can_comment = utils.check_perms(
            None, project, user)

        body = raw_data[message.startofbody:]
        content_type = ContentType.objects.get(model='issue')

        if can_comment:
            if issue is not None:
                comment = Comment()
                if user is not None:
                    comment.user_name = user.username
                    comment.user_email = user.email
                else:
                    comment.user_name = email_addy
                    comment.user_email = email_addy

                comment.content_type = content_type
                comment.object_pk = issue.id
                comment.comment = body
                comment.site = Site.objects.get(id=settings.SITE_ID)
                comment.save()
            else:
                issue = models.Issue()
                issue.name = issue_title
                issue.project = project
                issue.description = body
                status = models.Status.objects.get(id=1)
                priority = models.Priority.objects.get(id=1)
                issue_type = models.IssueType.objects.get(id=1)
                issue.status = status
                issue.priority = priority
                issue.issue_type = issue_type
                issue.save()

    def handle_noargs(self, **options):
        self.init_imap_client()
