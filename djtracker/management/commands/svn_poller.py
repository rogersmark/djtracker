import pysvn
import re

from djtracker import models

from django.core.management.base import NoArgsCommand
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.conf import settings

class Command(NoArgsCommand):
    help = "Polls SVN repo assigned to a project"

    def start_parser(self):
        self.content_type = ContentType.objects.get(model='issue')
        projects = models.Project.objects.all()
        for x in projects:
            if x.svn_repo_url:
                self.parse_repo(x)

    def parse_repo(self, project):
        starting_commit = project.svn_repo_commit
        client = pysvn.Client()
        client.set_interactive(False)
        client.set_default_username(project.svn_repo_username)
        client.set_default_password(project.svn_repo_password)
        commits = client.log(project.svn_repo_url,
           revision_start=pysvn.Revision(pysvn.opt_revision_kind.number, int(starting_commit)),
           revision_end=pysvn.Revision(pysvn.opt_revision_kind.head))

        match_string = re.compile('Fixes #[\d]+')
        issue_matches = []
        for x in commits:
            for message in match_string.findall(x.data['message']):
                issue_matches.append(x)

        number_string = re.compile('\d+')
        closed_status = models.Status.objects.get(slug="closed")
        for x in issue_matches:
            for y in number_string.findall(x.data['message']):
                try:
                    issue = models.Issue.objects.get(id=y)
                    if issue.status is closed_status:
                        continue
                except ObjectDoesNotExist:
                    continue

                issue.status=closed_status
                issue.save()
                comment = Comment()
                comment.user_name = "vcs_bot"
                comment.user_email = "vcs_bot@test.com"
                comment.content_type = self.content_type
                comment.object_pk = issue.id
                comment.comment = x.data['message']
                comment.site = Site.objects.get(id=settings.SITE_ID)
                comment.save()
                project.git_repo_commit = x.data['revision'].number
                project.save()

    def handle_noargs(self, **options):
        self.start_parser()


