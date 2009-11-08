from django.conf.urls.defaults import patterns

urlpatterns = patterns('djtracker.views',
    (r'^$', 'index', None, 'index'),
    (r'project/(?P<project_slug>\w+)/$', 'project_index', None, 'project_index'),
    (r'project/(?P<project_slug>\w+)/submit_issue/$', 'submit_issue', None, 
        'project_submit_issue'),
    (r'project/(?P<project_slug>\w+)/(?P<issue_slug>\w+)/$', 'view_issue', None,
        'project_issue'),
    (r'project/(?P<project_slug>\w+)/(?P<issue_slug>\w+)/modify_issue/$', 
        'modify_issue', None, 'project_modify_issue'),
    (r'project/(?P<project_slug>\w+)/(?P<issue_slug>\w+)/file_upload/$', 'issue_attach',
        None, 'project_file_upload'),
    (r'profile/(?P<username>\w+)/$', 'view_profile', None, 'project_user'),
)
