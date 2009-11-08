from django.conf.urls.defaults import patterns

urlpatterns = patterns('djtracker.views',
    ## Project views
    (r'^$', 'index', None, 'index'),
    (r'project/(?P<project_slug>\w+)/$', 'project_index', None, 'project_index'),

    ## Issue forms and views
    (r'project/(?P<project_slug>\w+)/submit_issue/$', 'submit_issue', None, 
        'project_submit_issue'),
    (r'project/(?P<project_slug>\w+)/(?P<issue_slug>\w+)/$', 'view_issue', None,
        'project_issue'),
    (r'project/(?P<project_slug>\w+)/(?P<issue_slug>\w+)/modify_issue/$', 
        'modify_issue', None, 'project_modify_issue'),
    (r'project/(?P<project_slug>\w+)/(?P<issue_slug>\w+)/file_upload/$', 'issue_attach',
        None, 'project_file_upload'),

    ## View 'modifiers' (list issues by component, milestone, version
    (r'project/(?P<project_slug>\w+)/component/(?P<modi_slug>\w+)/$', 'project_component',
        None, 'project_component'),
    (r'project/(?P<project_slug>\w+)/milestone/(?P<modi_slug>\w+)/$', 'project_milestone',
        None, 'project_milestone'),
    (r'project/(?P<project_slug>\w+)/version/(?P<modi_slug>\w+)/$', 'project_version',
        None, 'project_version'),

    ## Profile views
    (r'profile/(?P<username>\w+)/$', 'view_profile', None, 'project_user'),
)
