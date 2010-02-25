from djtracker import models 

from django import forms
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify

class IssueForm(forms.ModelForm):
    class Meta:
        model = models.Issue
        exclude = ['slug', 'active']

    name = forms.CharField(max_length=256)
    project = forms.ModelChoiceField(
        queryset=models.Project.objects.all(),
        widget=forms.HiddenInput
    )
    component = forms.ModelChoiceField(
        queryset=models.Component.objects.none(),
        required=False
    )
    version = forms.ModelChoiceField(
        queryset=models.Version.objects.none(),
        required=False
    )
    milestone = forms.ModelChoiceField(
        queryset=models.Milestone.objects.none(),
        required=False
    )
    description = forms.CharField(widget=forms.Textarea)
    created_by = forms.ModelChoiceField(
        queryset = models.UserProfile.objects.all(),
        widget=forms.HiddenInput,
        required=False
    )
    assigned_to = forms.ModelChoiceField(
        queryset = models.UserProfile.objects.all(),
        required=False
    )
    watched_by = forms.ModelMultipleChoiceField(
        queryset=models.UserProfile.objects.all(),
        required=False
    )

    def __init__(self, project_id, can_edit, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        project_instance = models.Project.objects.get(id=project_id)
        if models.Component.objects.filter(project=project_instance).count() > 0:
            self.fields['component'].queryset = \
                models.Component.objects.filter(project=project_instance)
        else:
            del self.fields['component']
        
        if models.Version.objects.filter(project=project_instance).count() > 0:
            self.fields['version'].queryset = \
                models.Version.objects.filter(project=project_instance)
        else:
            del self.fields['version']
        if models.Milestone.objects.filter(project=project_instance).count() > 0:            
            self.fields['milestone'].queryset = \
                models.Milestone.objects.filter(project=project_instance)
        else:
            del self.fields['milestone']
            
        if can_edit is False:
            self.fields['assigned_to'].widget = forms.HiddenInput()
            self.fields['watched_by'].widget = forms.HiddenInput()
    
    def save(self):
        if self.instance:
            try:
                issue = models.Issue.objects.get(id=self.instance.id)
            except:
                issue = models.Issue()
        else:
            issue = models.Issue()
        data = self.cleaned_data
        issue.name = data['name']
        issue.project = data['project']
        if 'component' in data:
            issue.component = data['component']
        if 'version' in data:
            issue.version = data['version']
        if 'milestone' in data:            
            issue.milestone = data['milestone']
        issue.status = data['status']
        issue.priority = data['priority']
        issue.issue_type = data['issue_type']
        issue.description = data['description']
        issue.created_by = data['created_by']
        issue.assigned_to = data['assigned_to']
        issue.active = True
        issue.save()
        return issue
    

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = models.FileUpload

    issue = forms.ModelChoiceField(
        queryset=models.Issue.objects.all(),
        widget=forms.HiddenInput
    )
