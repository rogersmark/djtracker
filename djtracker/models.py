from django.db import models
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse

class UserProfile(models.Model):
    """
    Extension of User to allow for more detailed information about a
    user
    """
    instant_messanger = models.CharField(max_length=256,
        blank=True,
        null=True
    )
    user = models.OneToOneField(User, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ("project_user", (), {'username': self.user.username})

class Project(models.Model):
    """
    Projects are the central location of where everything comes together. An
    issue is attached to a project, which has components, and so on and so
    forth. Consider it a grouping mechanism for all the moving parts.
    """
    ## Project descriptions
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    git_repo_path = models.CharField(max_length=1024,
        blank=True,
        null=True
    )
    git_repo_commit = models.TextField(max_length=512,
        blank=True,
        null=True
    )
    svn_repo_url = models.CharField(max_length=1024,
        blank=True,
        null=True
    )
    svn_repo_commit = models.TextField(max_length=512,
        blank=True,
        null=True
    )
    svn_repo_username = models.CharField(max_length=256,
        blank=True,
        null=True
    )
    svn_repo_password = models.TextField(max_length=256,
        blank=True,
        null=True
    )

    ## Project level permissions
    allow_anon_viewing = models.BooleanField(default=False)
    allow_anon_editing = models.BooleanField(default=False)
    allow_anon_comment = models.BooleanField(default=False)

    allow_authed_viewing = models.BooleanField(default=False)
    allow_authed_editing = models.BooleanField(default=False)
    allow_authed_comment = models.BooleanField(default=False)

    groups_can_view = models.ManyToManyField(Group,
        blank=True,
        null=True,
        related_name='view_group_set'
    )
    groups_can_edit = models.ManyToManyField(Group,
        blank=True,
        null=True,
        related_name='edit_group_set'
    )
    groups_can_comment = models.ManyToManyField(Group,
        blank=True,
        null=True,
        related_name='comment_group_set'
    )

    users_can_view = models.ManyToManyField(User,
        blank=True,
        null=True,
        related_name='view_user_set'
    )
    users_can_edit = models.ManyToManyField(User,
        blank=True,
        null=True,
        related_name='edit_user_set'
    )
    users_can_comment = models.ManyToManyField(User,
        blank=True,
        null=True,
        related_name='comment_user_set'
    )

    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_index", (), {'project_slug': self.slug})

class Milestone(models.Model):
    """
    Goal to be reached
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    project = models.ForeignKey(Project)
    description = models.TextField(blank=True, null=True)
    goal_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_milestone", (), {'project_slug': self.project.slug,
            'modi_slug': self.slug})

class Component(models.Model):
    """
    Components are items that are part of a project. For instance I have a
    project called Cars. We then have tires that are part of cars
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    project = models.ForeignKey(Project)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_component", (), {'project_slug': self.project.slug, 
            'modi_slug': self.slug})

class Version(models.Model):
    """
    This will be FKed to projects. This will allow creation of issues
    that point at specific versions
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    project = models.ForeignKey(Project)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_version", (), {'project_slug': self.project.slug,
            'modi_slug': self.slug})

class Status(models.Model):
    """
    Status dictate what status an issue is in, such as open, closed, etc
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

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
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

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
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

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
    name = models.CharField(max_length=256)
    project = models.ForeignKey(Project)
    component = models.ForeignKey(Component,
        blank=True,
        null=True
    )
    version = models.ForeignKey(Version,
        blank=True,
        null=True
    )
    milestone = models.ForeignKey(Milestone,
        blank=True,
        null=True
    )
    status = models.ForeignKey(Status)
    priority = models.ForeignKey(Priority)
    issue_type = models.ForeignKey(IssueType)
    description = models.TextField()
    created_by = models.ForeignKey(UserProfile,
        blank=True,
        null=True,
        related_name="issue_creator"
    )
    assigned_to = models.ForeignKey(UserProfile,
        blank=True,
        null=True
    )
    watched_by = models.ManyToManyField(UserProfile,
        blank=True,
        null=True,
        related_name="watched_set"
    )
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_issue", (), {'project_slug': self.project.slug,
            'issue_id': self.id})

class FileUpload(models.Model):
    """
    File uploads will be FKed to specific issues. This will allow for 
    multiple files to be uploaded to a particular issue.
    """
    name = models.CharField(max_length=256)
    file = models.FileField(upload_to='attachments')
    issue = models.ForeignKey(Issue)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
            return ("project_issue_file", (), {'project_slug': self.issue.project.slug,
                                               'file_id': self.id})

class IssueFilter(models.Model):
    """
    This allows users to save their favorite view filters
    """
    project = models.ForeignKey(Project)
    user = models.ForeignKey(UserProfile,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=256)
    component = models.CharField(max_length=256,
        blank=True,
        null=True
    )
    version = models.CharField(max_length=256,
        blank=True,
        null=True
    )
    milestone = models.CharField(max_length=256,
        blank=True,
        null=True
    )
    status = models.CharField(max_length=256,
        blank=True,
        null=True
    )
    type = models.CharField(max_length=256,
        blank=True,
        null=True
    )
    priority = models.CharField(max_length=256,
        blank=True,
        null=True
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
