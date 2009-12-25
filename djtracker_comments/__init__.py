from djtracker_comments.models import CommentWithIssueStatus
from djtracker_comments.forms import CommentWithIssueStatusForm

def get_model():
    return CommentWithIssueStatus

def get_form():
    return CommentWithIssueStatusForm