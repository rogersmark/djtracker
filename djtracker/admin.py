from django.contrib import admin
from djtracker import models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'active',)
    list_filter = ('active',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'active')
        }),
    )

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'active',)
    list_filter = ('active',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Project Information', {
            'fields': ('name', 'slug', 'category',
                'description', 'active')
        }),
    )

class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'goal_date',)
    list_filter = ('active', 'project',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Milestone Infromation', {
            'fields': ('name', 'slug', 'project',
                'description', 'goal_date',
                'active')
        }),
    )

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'project',)
    list_filter = ('active', 'project',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Component Information', {
            'fields': ('name', 'slug', 'project',
                'active')
        }),
    )

class VersionAdmin(admin.ModelAdmin):
    list_display = ('name', 'project',)
    list_filter = ('active', 'project',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Version Information', {
            'fields': ('name', 'slug', 'project',
                'active')
        }),
    )

class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'component',
        'version', 'milestone', 'status', 
        'priority',)
    list_filter = ('active', 'project', 'component',
        'version', 'milestone', 'status',
        'priority',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'slug', 'active')
        }),
        ('Issue Information', {
            'fields': ('project', ('component', 'version'),
                ('milestone', 'status'),
                ('priority', 'issue_type'),
                'description')
        }),
    )

class FileUploadAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Milestone, MilestoneAdmin)
admin.site.register(models.Component, ComponentAdmin)
admin.site.register(models.Version, VersionAdmin)
admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.FileUpload, FileUploadAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
