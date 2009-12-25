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
        status = Status.objects.get(id=self.status_id)
        issue.status = status
        issue.save()
        super(CommentWithIssueStatus, self).save()