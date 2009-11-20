import git
import re

from djtracker import models

from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment

class Command(NoArgsCommand):
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
        commits = repo.commits_since(starting_commit)
        print commits
        match_string = re.compile('Fixes #[\d]+')
        issue_matches = []
        for x in commits:
            for message in match_string.findall(x.message):
                print message
                issue_matches.append(x.message)

        number_string = re.compile('\d+')
        closed_status = models.Status.objects.get(slug="closed")
        for x in issue_matches:
            for y in number_string.findall(x):
                try:
                    print y
                    issue = models.Issue.objects.get(id=y)
                    if issue.status is closed_status:
                        continue
                except ObjectDoesNotExist:
                    continue

                issue.status=closed_status
                issue.save()
                comment = Comment()
                comment.content_type = self.content_type
                comment.object_pk = issue.id
                comment.comment = x.message
                comment.save()
                project.git_repo_commit = x
                project.save()

    def handle_noargs(self, **options):
        self.start_parser()
        

