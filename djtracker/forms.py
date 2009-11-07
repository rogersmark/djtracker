from djtracker import models, choices

from django import forms
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify

class IssueForm(forms.Form):
    def __init__(self, project_id, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.project = models.Project.objects.get(id=project_id)

    name = forms.CharField(max_length=256)
    component = forms.ModelChoiceField(
        queryset=models.Component.objects.filter(project=self.project),
        required=False
    )
    version = forms.ModelChoiceField(
        queryset=models.Version.objects.filter(project=self.project),
        required=False
    )
    milestone = forms.ModelChoiceField(
        queryset=models.Milestone.objects.filter(project=self.project),
        required=False
    )
    status = forms.CharField(max_length=128,
        choices=choices.STATUS_OPTIONS
    )
    priority = forms.CharField(max_length=128,
        choices=choices.PRIORITIES
    )
    issue_type = forms.CharField(max_length=128,
        choices=choices.BUG_TYPES
    )
    description = forms.TextField()

    def save(self):
        data = self.cleaned_data
        issue = models.Issue()
        issue.name = data['name']
        issue.slug = slugify(data['name'])
        issue.project = self.project
        issue.component = data['component']
        issue.version = data['version']
        issue.milestone = data['milestone']
        issue.status = data['status']
        issue.priority = data['priority']
        issue.issue_type = data['issue_type']
        issue.description = data['description']
        issue.active = True
        issue.save()

class FileUploadForm(forms.Form):
    def __init__(self, issue_id, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.issue = models.Issue.objects.get(id=issue_id)

    name = forms.CharField(max_length=256)
    file = forms.FileField(upload_to='attachments')
    
    def save()
        data = self.cleaned_data
        file_upload = models.FileUpload()
        file_upload.name = data['name']
        file_upload.file = data['file']
        file_upload.issue = self.issue
        file_upload.save()

