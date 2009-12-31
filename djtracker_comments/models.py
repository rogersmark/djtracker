from djtracker.models import Status, Issue

from django.db import models
from django.contrib.comments.models import Comment

class CommentWithIssueStatus(Comment):
    """
    The object here is to add a status field for issues that are being
    commented on.
    """
    status = models.ForeignKey(Status)
    
    def save(self):
        issue = Issue.objects.get(id=self.object_pk)
        if self.status_id:
            status = Status.objects.get(id=self.status_id)
            if issue.status is not status:
                issue.status = status
                issue.save()
        else:
            self.status = issue.status
        super(CommentWithIssueStatus, self).save()