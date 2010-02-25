'''
alternative views for the new, report-based dashboard and project view

@author: chris vigelius <chris.vigelius@gmx.net>
'''

import os
import mimetypes

from djtracker import models, utils, forms
from djtracker_comments.models import CommentWithIssueStatus

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User, Group
from django.contrib.comments.models import Comment
from django.core.urlresolvers import reverse
from django.views.generic import list_detail
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings


def dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound()
    user = request.user
    profile = user.userprofile
    rss_feed = "personal/1/%s" % profile.uuid
#    assigned_issues = models.Issue.objects.filter(assigned_to=profile)
#    created_issues = models.Issue.objects.filter(created_by=profile)
#    watched_issues = models.Issue.objects.filter(watched_by=profile)
#    comments = []
#    for x in Comment.objects.all():
#        if x.content_type.name == "issue":
#            if x.user == user:
#                comments.append(x.content_object.id)
#
#    commented_issues = models.Issue.objects.filter(id__in=comments)
#    all_relevant_issues = []
#    for x in assigned_issues:
#        if x not in all_relevant_issues:
#            all_relevant_issues.append(x.id)
#    for x in created_issues:
#        if x not in all_relevant_issues:
#            all_relevant_issues.append(x.id)
#    for x in watched_issues:
#        if x not in all_relevant_issues:
#            all_relevant_issues.append(x.id)
#    for x in commented_issues:
#        if x not in all_relevant_issues:
#            all_relevant_issues.append(x.id)
#
#    recently_updated = models.Issue.objects.filter(
#        id__in=all_relevant_issues).order_by(
#        '-modified_date')
    return render_to_response(
        "djtracker_reporting/user_dashboard.html", locals(),
        context_instance=RequestContext(request))

def project_index(request, project_slug):
    project = get_object_or_404(models.Project, slug=project_slug)
    #open_issues = project.issue_set.filter(status__slug="open")
    priorities = models.Priority.objects.all()
    statuses = models.Status.objects.all()
    types = models.IssueType.objects.all()
    can_view, can_edit, can_comment = utils.check_perms(request, project)
    
    ## Check if we're watching this project
    is_watching = False
    if request.user.is_authenticated():
        try:
            profile = models.UserProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            is_watching = False
            profile = None
        if profile in project.watched_by.all():
            is_watching = True
    
    if "watch" in request.GET and can_view:
        if request.GET['watch'] == "yes":
            try:
                profile = models.UserProfile.objects.get(user=request.user)
            except ObjectDoesNotExist:
                profile = models.UserProfile.create(user=request.user)
                profile.save()
            project.watched_by.add(profile)
            return HttpResponseRedirect(project.get_absolute_url())
        elif request.GET['watch'] == "no":
            profile = models.UserProfile.objects.get(user=request.user)
            project.watched_by.remove(profile)
            return HttpResponseRedirect(project.get_absolute_url())
        
    if can_view is False:
        return HttpResponseNotFound()
    else:
        return list_detail.object_detail(request,
            queryset=models.Project.objects.all(),
            extra_context={'can_comment': can_comment,
                'statuses': statuses,
                'priorities': priorities,
                'request': request,
                'types': types,
                'is_watching': is_watching
            },
            slug=project_slug,
            template_name="djtracker_reporting/project_index.html",
            template_object_name="project"
        )
