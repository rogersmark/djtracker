import datetime

from django.db import models
from django.contrib.comments.models import Comment

from djtracker.models import Status, Issue
from djtracker.signals import issue_commented
from djtracker.middleware import get_current_request

class CommentWithIssueStatus(Comment):
    """
    The object here is to add a status field for issues that are being
    commented on.
    """
    status = models.ForeignKey(Status)
    old_status = models.ForeignKey(Status, blank=True, null=True, related_name='oldstatus_set')
    
    def save(self):
        issue = Issue.objects.get(id=self.object_pk)
        status_change = None
        if self.status_id:
            status = Status.objects.get(id=self.status_id)
            if issue.status != status:
                status_change = (issue.status, status)                
                self.old_status = issue.status
                issue.status = status                
        else:
            self.status = issue.status
        
        issue.modified_date = datetime.datetime.now()
        issue.save(suppress_signal=True)
        
        super(CommentWithIssueStatus, self).save()
        
        issue_commented.send(sender=self.__class__, 
                             comment=self, 
                             issue=issue, 
                             status_change=status_change, 
                             request=get_current_request(True))