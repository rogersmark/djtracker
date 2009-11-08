from django.db import models
from django.contrib.auth.models import User, Group

from djtracker import choices

class UserProfile(models.Model):
    """
    Extension of User to allow for more detailed information about a
    user
    """
    instant_messanger = models.CharField(max_length=256)
    user = models.ForeignKey(User, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_Date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ("project_user", (), {'user': self.username})

class Category(models.Model):
    """
    Projects will be able to be assigned to different categories. For 
    instance you may have some HR projects in here, as well as dev
    projects
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_Date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_categories", (), {'category_slug': self.slug})

    class Meta:
        verbose_name_plural = "Categories"

class Project(models.Model):
    """
    Projects are the central location of where everything comes together. An
    issue is attached to a project, which has components, and so on and so
    forth. Consider it a grouping mechanism for all the moving parts.
    """
    ## Project descriptions
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category)
    description = models.TextField(blank=True, null=True)

    ## Project level permissions
    allow_anon_viewing = models.BooleanField(default=False)
    allow_anon_editing = models.BooleanField(default=False)
    allow_anon_comment = models.BooleanField(default=False)

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
    modified_Date = models.DateTimeField(auto_now=True)

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
    modified_Date = models.DateTimeField(auto_now=True)

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
    modified_Date = models.DateTimeField(auto_now=True)

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
    modified_Date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_version", (), {'project_slug': self.project.slug,
            'modi_slug': self.slug})

class Issue(models.Model):
    """
    This will be the root problem that is created. It will have a version,
    component, and so on.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
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
    status = models.CharField(max_length=128,
        choices=choices.STATUS_OPTIONS
    )
    priority = models.CharField(max_length=128,
        choices=choices.PRIORITIES
    )
    issue_type = models.CharField(max_length=128,
        choices=choices.BUG_TYPES
    )
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
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_Date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_issue", (), {'project_slug': self.project.slug,
            'issue_slug': self.slug})

class FileUpload(models.Model):
    """
    File uploads will be FKed to specific issues. This will allow for 
    multiple files to be uploaded to a particular issue.
    """
    name = models.CharField(max_length=256)
    file = models.FileField(upload_to='attachments')
    issue = models.ForeignKey(Issue)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_Date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("project_file", (), {'file': self.file})

