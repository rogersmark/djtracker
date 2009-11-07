from djtracker import models, choices, utils, forms

from django.http import HttpResponseNotFound
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.views.generic import list_detail
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    projects = models.Project.objects.all()
    if request.user.is_authenticated():
        user = request.user
        groups = user.groups.all()
        viewable_projects = []
        for x in projects.filter(allow_anon_viewing=False):
            if user in x.users_can_view.all():
                viewable_projects.append(x.id)
            for y in groups:
                if y in x.groups_can_view.all():
                    if x.id not in viewable_projects:
                        viewable_projects.append(x.id)

        for x in projects.filter(allow_anon_viewing=True):
            if x.id not in viewable_projects:
                viewable_projects.append(x.id)

        display_projects = models.Project.objects.filter(
            id__in=viewable_projects)
    else:
        display_projects = projects.filter(allow_anon_viewing=True)

    return list_detail.object_list(request,
        queryset=display_projects,
        paginate_by=10,
        allow_empty=True,
        template_name="djtracker/index.html",
        template_object_name="project"
    )

def project_index(request, project_slug):
    project = get_object_or_404(models.Project, slug=project_slug)
    can_comment = False
    if project.allow_anon_comment is True or \
        utils.check_permissions("", request.user, project) is True:
        can_comment = True
    if project.allow_anon_viewing is False and request.user.is_authenticated() is False:
        return HttpResponseNotFound()
    elif request.user.is_authenticated():
        user = request.user
        groups = user.groups.all()
        if utils.check_permissions("view", request.user, project) is False:
            return HttpResponseNotFound()
        else:
            return list_detail.object_detail(request,
                queryset=models.Project.objects.all(),
                extra_context={'can_comment': can_comment},
                slug=project_slug,
                template_name="djtracker/project_index.html",
                template_object_name="project"
            )

def submit_issue(request, project_slug):
    project = get_object_or_404(models.Project, slug=project_slug)
    can_edit = False
    if project.allow_anon_editing is False and \
        utils.check_permissions("", request.user, project) is False:
        can_edit = False
    else:
        can_edit = True
    if project.allow_anon_comment is False and request.user.is_authenticated() is False:
        return HttpResponseNotFound()
    elif utils.check_permissions("comment", request.user, project) is False: 
        return HttpResponseNotFound()
    else:
        if request.method == "POST":
            form = forms.IssueForm(project.id, can_edit, request.POST)
            if form.is_valid():
                issue = form.save()
                return HttpResponseRedirect(issue.get_absolute_url())
        else:
            if request.user:
                form = forms.IssueForm(project.id, can_edit, 
                    initial={ 'project': project.id, 'created_by': request.user.id})
            else:
                form = forms.IssueForm(project.id, can_edit,
                    initial={ 'project': project.id })
        return render_to_response(
            "djtracker/submit_issue.html", locals(),
            context_instance=RequestContext(request))

def modify_issue(request, project_slug, issue_slug):
    project = get_object_or_404(models.Project, slug=project_slug)
    issue = get_object_or_404(models.Issue, slug=issue_slug)
    if project.allow_anon_editing is False:
        return HttpResponseNotFound()
    elif utils.check_permissions("", request.user, project) is False and \
        project.allow_anon_editing is False:
        return HttpResponseNotFound()
    else:
        can_edit = True
        if request.method == "POST":
            form = forms.IssueForm(project.id, can_edit, request.POST, instance=issue)
            if form.is_valid():
                issue=form.save()
                return HttpResponseRedirect(issue.get_absolute_url())
        else:
            form = forms.IssueForm(project.id, can_edit, instance=issue)
        
        return render_to_response(
            "djtracker/modify_issue.html", locals(),
            context_instance=RequestContext(request))

def view_issue(request, project_slug, issue_slug):
    project = get_object_or_404(models.Project, slug=project_slug)
    issue = get_object_or_404(models.Issue, slug=issue_slug)
    ## Check if we can comment
    can_comment = False
    if project.allow_anon_comment is True:
        can_comment = True
    if utils.check_permissions("comment", request.user, project):
        can_comment = True

    can_modify = False
    if project.allow_anon_editing is True:
        can_modify = True
    if utils.check_permissions("", request.user, project):
        can_modify = True
    
    ## Check if we can view
    if project.allow_anon_viewing is False and request.user.is_authenticated() is False:
        return HttpResponseNotFound()
    elif utils.check_permissions("view", request.user, project) is False:
        return HttpResponseNotFound()
    else:
        return render_to_response(
            "djtracker/issue_detail.html", locals(),
            context_instance=RequestContext(request))
