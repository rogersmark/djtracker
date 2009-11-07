from djtracker import models, choices

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
    if project.allow_anon_viewing is False and request.user.is_authenticated is False:
        return HttpResponseNotFound()
    elif request.user.is_authenticated():
        can_view = False
        user = request.user
        groups = user.groups.all()
        if user not in project.users_can_view.all() and \
            groups not in project.groups_can_view.all() and \
            project.allow_anon_viewing is False:
            return HttpResponseNotFound()
        else:
            return list_detail.object_detail(request,
                queryset=models.Project.objects.all(),
                slug=project_slug,
                template_name="djtracker/project_index.html",
                template_object_name="project"
            )
