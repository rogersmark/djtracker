from django.conf.urls.defaults import patterns

urlpatterns = patterns('djtracker.views',
    ## Project views
    (r'^$', 'index', None, 'index'),
    (r'project/(?P<project_slug>\w+)/$', 'project_index', None, 'project_index'),
    (r'category/(?P<cat_slug>\w+)/$', 'view_category', None, 'project_category'),

    ## View 'modifiers' (list issues by component, milestone, version
    (r'project/(?P<project_slug>\w+)/component/(?P<modi_slug>\w+)/$', 
        'project_component',
        None, 'project_component'),
    (r'project/(?P<project_slug>\w+)/milestone/(?P<modi_slug>[a-z0-9-]+)/$', 
        'project_milestone',
        None, 'project_milestone'),
    (r'project/(?P<project_slug>\w+)/version/(?P<modi_slug>[a-z0-9-]+)/$', 
        'project_version',
        None, 'project_version'),

    ## Issue forms and views
    (r'project/(?P<project_slug>\w+)/submit_issue/$', 'submit_issue', None, 
        'project_submit_issue'),
    (r'project/(?P<project_slug>\w+)/(?P<issue_slug>\w+)/$', 'view_issue', None,
        'project_issue'),
    (r'project/(?P<project_slug>\w+)/(?P<issue_slug>\w+)/modify_issue/$', 
        'modify_issue', None, 'project_modify_issue'),
    (r'project/(?P<project_slug>\w+)/(?P<issue_slug>\w+)/file_upload/$', 
        'issue_attach',
        None, 'project_file_upload'),

    ## Profile views
    (r'profile/detail/(?P<username>\w+)/$', 'view_profile', None, 'project_user'),
    (r'profile/list/$', 'view_users', None, 'project_user_list'),
)
