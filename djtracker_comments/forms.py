from djtracker.models import Status

from django import forms
from django.contrib.comments.forms import CommentForm
from djtracker_comments.models import CommentWithIssueStatus

class CommentWithIssueStatusForm(CommentForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False
    )
    
    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return CommentWithIssueStatus

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(CommentWithIssueStatusForm, self).get_comment_create_data()
        data['status'] = self.cleaned_data['status']
        return data
        