import git
import re

from djtracker import models

from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.conf import settings

class Command(NoArgsCommand):
    """
    This argument parses the repos assigned to the various projects that can 
    be stored in djtracker. It currently doesn't take any arguments either.
    A few notes in regards to this though:

        1. gitpython is in an Alpha state
        2. This makes some assumptions, such as you want to parse all commits
        since your last one
        3. That you want to close the issue by saying "Fixes #issue_number"

    Essentially what this does is takes the commit hash the user initialized
    the project with, and finds it in the list of commits. Then we find its
    index in the list, and slice the index down. We parse everything since the
    last commit for the "Fixes #ISSUE_NUMBER" string. If found, we add a 
    comment to the issue, and close the issue out.
    """
    help = "Polls Git repos assigned to projects"

    def start_parser(self):
        self.content_type = ContentType.objects.get(model='issue')
        projects = models.Project.objects.all()
        for x in projects:
            if x.git_repo_path:
                self.parse_repo(x)

    def parse_repo(self, project):
        repo = git.Repo(project.git_repo_path)
        starting_commit = project.git_repo_commit
        commits = repo.commits()
        for x in commits:
            if starting_commit == x.id:
                starting_commit = x
        index = commits.index(starting_commit)
        commits = commits[:index]
        match_string = re.compile('Fixes #[\d]+')
        issue_matches = []
        for x in commits:
            for message in match_string.findall(x.message):
                issue_matches.append(x)

        number_string = re.compile('\d+')
        closed_status = models.Status.objects.get(slug="closed")
        for x in issue_matches:
            for y in number_string.findall(x.message):
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
                comment.comment = x.message
                comment.site = Site.objects.get(id=settings.SITE_ID)
                comment.save()
                project.git_repo_commit = x.id
                project.save()

    def handle_noargs(self, **options):
        self.start_parser()
        

