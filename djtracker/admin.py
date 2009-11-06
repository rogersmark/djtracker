from django.contrib import admin
from djtracker import models

class (admin.ModelAdmin):
    pass

class (admin.ModelAdmin):
    pass

class (admin.ModelAdmin):
    pass

class (admin.ModelAdmin):
    pass

class (admin.ModelAdmin):
    pass

class (admin.ModelAdmin):
    pass

class (admin.ModelAdmin):
    pass

class (admin.ModelAdmin):
    pass

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Milestone, MilestoneAdmin)
admin.site.register(models.Component, ComponentAdmin)
admin.site.register(models.Version, VersionAdmin)
admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.FileUpload, FileUploadAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
