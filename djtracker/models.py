import uuid

from django.db import models
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from djtracker.utils import check_perms

class UserProfile(models.Model):
    """
    Extension of User to allow for more detailed information about a
    user
    """
    instant_messanger = models.CharField(
        _("instant messanger"), 
        max_length=256,
        blank=True,
        null=True
    )
    user = models.OneToOneField(User, unique=True, verbose_name=_("user"))
    uuid = models.CharField(max_length=36)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified date"), auto_now=True)

    def __unicode__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ("project_user", (), {'username': self.user.username})
        
    def save(self):
        if not self.uuid:
            temp_uuid = str(uuid.uuid1())
            temp_uuid = temp_uuid.replace('-', '')
            self.uuid = temp_uuid
            super(UserProfile, self).save()

def get_allowed_project_ids(request, user=None, permission='view'):
    """
    returns a list of project ids which request.user is allowed to see 
    """    
    project_ids = []
    perm_index = ['view', 'edit', 'comment'].index(permission)    
    # need to reference Project indirectly to avoid circular import reference
    for project in models.get_model('djtracker','project').objects.all():
        perms = check_perms(request, project, user)
        if perms[perm_index]:
            project_ids.append(project.id)
    return project_ids

class PermissionFilterManager(models.Manager):
    """
    a manager which adds a special permission filter. usage:
    
    in queries, replace
        model_class.objects.all()
    with
        model_class.objects.filter_allowed(request)
    """
    def __init__(self, by='project__id__in', *args, **kwargs):
        """
        ``by`` determines on which attribute to filter (default: project)  
        """
        self._by = by
        super(PermissionFilterManager, self).__init__(*args, **kwargs)
        
    def filter_allowed(self, request, permission='view'):
        project_ids = get_allowed_project_ids(request, permission)
        if self._by:
            return self.filter(**{self._by: project_ids})

class Project(models.Model):
    """
    Projects are the central location of where everything comes together. An
    issue is attached to a project, which has components, and so on and so
    forth. Consider it a grouping mechanism for all the moving parts.
    """
    ## Project descriptions
    name = models.CharField(_("name"), max_length=256)
    slug = models.SlugField(_("slug"), unique=True)
    description = models.TextField(_("description"), blank=True, null=True)
    git_repo_path = models.CharField(
        _("git repo path"),
        max_length=1024,
        blank=True,
        null=True
    )
    git_repo_commit = models.TextField(
        _("git repo commit"),
        max_length=512,
        blank=True,
        null=True
    )
    svn_repo_url = models.CharField(
        _("svn repo url"),
        max_length=1024,
        blank=True,
        null=True
    )
    svn_repo_commit = models.TextField(
        _("svn repo commit"),
        max_length=512,
        blank=True,
        null=True
    )
    svn_repo_username = models.CharField(
        _("svn repo username"),
        max_length=256,
        blank=True,
        null=True
    )
    svn_repo_password = models.TextField(
        _("svn repo password"),
        max_length=256,
        blank=True,
        null=True
    )

    ## Project level permissions
    allow_anon_viewing = models.BooleanField(_("allow anon viewing"), default=False)
    allow_anon_editing = models.BooleanField(_("allow anon editing"), default=False)
    allow_anon_comment = models.BooleanField(_("allow anon comment"), default=False)

    allow_authed_viewing = models.BooleanField(_("allow authed viewing"), default=False)
    allow_authed_editing = models.BooleanField(_("allow authed editing"), default=False)
    allow_authed_comment = models.BooleanField(_("allow authed comment"), default=False)

    groups_can_view = models.ManyToManyField(Group,
        blank=True,
        null=True,
        related_name='view_group_set',
        verbose_name=_("groups can view")
    )
    groups_can_edit = models.ManyToManyField(Group,
        blank=True,
        null=True,
        related_name='edit_group_set',
        verbose_name=_("groups can edit")
    )
    groups_can_comment = models.ManyToManyField(Group,
        blank=True,
        null=True,
        related_name='comment_group_set',
        verbose_name=_("groups can comment")
    )

    users_can_view = models.ManyToManyField(User,
        blank=True,
        null=True,
        related_name='view_user_set',
        verbose_name=_("users can view")
    )
    users_can_edit = models.ManyToManyField(User,
        blank=True,
        null=True,
        related_name='edit_user_set',
        verbose_name=_("users can edit")
    )
    users_can_comment = models.ManyToManyField(User,
        blank=True,
        null=True,
        related_name='comment_user_set',
        verbose_name=_("users can comment")
    )
    watched_by = models.ManyToManyField(UserProfile,
        blank=True,
        null=True,
        verbose_name=_("watched by")
        
    )

    active = models.BooleanField(_("active"), default=True)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified date"), auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_index", (), {'project_slug': self.slug})

    objects = PermissionFilterManager(by='id__in')

class Milestone(models.Model):
    """
    Goal to be reached
    """
    name = models.CharField(_("name"), max_length=256)
    slug = models.SlugField(_("slug"), unique=True)
    project = models.ForeignKey(Project, verbose_name=_("project"))
    description = models.TextField(_("description"), blank=True, null=True)
    goal_date = models.DateTimeField(_("goal date"), blank=True, null=True)
    active = models.BooleanField(_("active"), default=True)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified date"), auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_milestone", (), {'project_slug': self.project.slug,
            'modi_slug': self.slug})

    objects = PermissionFilterManager()

class Component(models.Model):
    """
    Components are items that are part of a project. For instance I have a
    project called Cars. We then have tires that are part of cars
    """
    name = models.CharField(_("name"), max_length=256)
    slug = models.SlugField(_("slug"), unique=True)
    project = models.ForeignKey(Project, verbose_name=_("project"))
    active = models.BooleanField(_("active"), default=True)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified date"), auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_component", (), {'project_slug': self.project.slug, 
            'modi_slug': self.slug})

    objects = PermissionFilterManager()

class Version(models.Model):
    """
    This will be FKed to projects. This will allow creation of issues
    that point at specific versions
    """
    name = models.CharField(_("name"), max_length=256)
    slug = models.SlugField(_("slug"), unique=True)
    project = models.ForeignKey(Project, verbose_name=_("project"))
    active = models.BooleanField(_("active"), default=True)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified_date"), auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_version", (), {'project_slug': self.project.slug,
            'modi_slug': self.slug})

    objects = PermissionFilterManager()

class Status(models.Model):
    """
    Status dictate what status an issue is in, such as open, closed, etc
    """
    name = models.CharField(_("name"), max_length=256)
    slug = models.SlugField(_("slug"), unique=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_status", (), {'project_slug': self.project.slug,
            'status_slug': self.slug})

class Priority(models.Model):
    """
    Priority dictates the emphasis an issue carries. Urgent, critical, etc
    """
    name = models.CharField(_("name"), max_length=256)
    slug = models.SlugField(_("slug"), unique=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_priority", (), {'project_slug': self.project.slug,
            'priority_slug': self.slug})

    class Meta:
        verbose_name_plural = "Priorities"

class IssueType(models.Model):
    """
    Bug, defect, feature request, etc
    """
    name = models.CharField(_("name"), max_length=256)
    slug = models.SlugField(_("slug"), unique=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_issue_type", (), {'project_slug': self.project.slug,
            'type_slug': self.slug})

class Issue(models.Model):
    """
    This will be the root problem that is created. It will have a version,
    component, and so on.
    """
    name = models.CharField(_("name"), max_length=256)
    project = models.ForeignKey(Project, verbose_name=_("project"))
    component = models.ForeignKey(Component,
        blank=True,
        null=True,
        verbose_name=_("component")
    )
    version = models.ForeignKey(Version,
        blank=True,
        null=True,
        verbose_name=_("version")
    )
    milestone = models.ForeignKey(Milestone,
        blank=True,
        null=True,
        verbose_name=_("milestone")
    )
    status = models.ForeignKey(Status, 
        verbose_name=_("status")
    )
    priority = models.ForeignKey(Priority,
        verbose_name=_("priority")
    )
    issue_type = models.ForeignKey(IssueType,
        blank=True,
        null=True,
        verbose_name=_("issue type")
    )
    description = models.TextField(_("description"))
    created_by = models.ForeignKey(UserProfile,
        blank=True,
        null=True,
        related_name="issue_creator",
        verbose_name=_("created by"),
    )
    assigned_to = models.ForeignKey(UserProfile,
        blank=True,
        null=True,
        verbose_name=_("assigned to")
    )
    watched_by = models.ManyToManyField(UserProfile,
        blank=True,
        null=True,
        related_name="watched_set",
        verbose_name=_("watched by"),
    )
    active = models.BooleanField(_("active"), default=True)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified date"), auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_issue", (), {'project_slug': self.project.slug,
            'issue_id': self.id})

    objects = PermissionFilterManager()

class FileUpload(models.Model):
    """
    File uploads will be FKed to specific issues. This will allow for 
    multiple files to be uploaded to a particular issue.
    """
    name = models.CharField(_("name"), max_length=256)
    file = models.FileField(_("file"), upload_to='attachments')
    issue = models.ForeignKey(Issue, verbose_name=_("issue"))
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified date"), auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
            return ("project_issue_file", (), {'project_slug': self.issue.project.slug,
                                               'file_id': self.id})

    objects = PermissionFilterManager(by='issue__project__id__in')

class IssueFilter(models.Model):
    """
    This allows users to save their favorite view filters
    """
    project = models.ForeignKey(Project, verbose_name=_("project"))
    user = models.ForeignKey(UserProfile,
        blank=True,
        null=True,
        verbose_name=_("user")
    )
    name = models.CharField(_("name"), max_length=256)
    component = models.CharField(max_length=256,
        blank=True,
        null=True,
        verbose_name=_("component"),
    )
    version = models.CharField(max_length=256,
        blank=True,
        null=True,
        verbose_name=_("version")
    )
    milestone = models.CharField(max_length=256,
        blank=True,
        null=True,
        verbose_name=_("milestone")
    )
    status = models.CharField(max_length=256,
        blank=True,
        null=True,
        verbose_name=_("status")
    )
    type = models.CharField(max_length=256,
        blank=True,
        null=True,
        verbose_name=_("type")
    )
    priority = models.CharField(max_length=256,
        blank=True,
        null=True,
        verbose_name=_("priority")
    )

    def __unicode__(self):
        return "Filter for %s: %s" % (self.user, self.name)

    def get_filtered_url(self):
        base_url = reverse("project_all_issues", kwargs={'project_slug': self.project.slug})
        get_vars = "?component=%s&version=%s&milestone=%s&status=%s&type=%s&priority=%s" % (
            self.component, self.version, self.milestone, self.status, self.type,
            self.priority)
        final_url = base_url + get_vars
        return final_url
