from django.conf.urls.defaults import patterns
from djtracker.feeds import PersonalFeed, ProjectIssue

feeds = {
    'project': ProjectIssue,
    'personal': PersonalFeed,
}

urlpatterns = patterns('djtracker.views',
    ## Project views
    (r'^$', 'index', None, 'index'),
    (r'^project/search/$', 'project_search', None, 'project_search'),
    (r'^project/(?P<project_slug>[a-z0-9-]+)/$', 'project_index', None, 'project_index'),
    (r'^project/(?P<project_slug>[a-z0-9-]+)/status/(?P<status_slug>[a-z0-9-]+)/$',
        'project_status_issues', None, 'project_status'),
    (r'^project/(?P<project_slug>[a-z0-9-]+)/priority/(?P<priority_slug>[a-z0-9-]+)/$',
        'project_priority_issues', None, 'project_priority'),
    (r'^project/(?P<project_slug>[a-z0-9-]+)/type/(?P<type_slug>[a-z0-9-]+)/$',
        'project_type_issues', None, 'project_issue_type'),
    (r'^project/(?P<project_slug>[a-z0-9-]+)/view_all/$', 'project_all_issues', 
        None, 'project_all_issues'),
    (r'^project/(?P<project_slug>[a-z0-9-]+)/file/(?P<file_id>[-\d]+)/$',
        'project_issue_file', None, 'project_issue_file'),

    ## View 'modifiers' (list issues by component, milestone, version
    (r'^project/(?P<project_slug>[a-z0-9-]+)/component/(?P<modi_slug>[a-z0-9-]+)/$', 
        'project_component',
        None, 'project_component'),
    (r'^project/(?P<project_slug>[a-z0-9-]+)/milestone/(?P<modi_slug>[a-z0-9-]+)/$', 
        'project_milestone',
        None, 'project_milestone'),
    (r'^project/(?P<project_slug>[a-z0-9-]+)/version/(?P<modi_slug>[a-z0-9-]+)/$', 
        'project_version',
        None, 'project_version'),

    ## Issue forms and views
    (r'^project/(?P<project_slug>[a-z0-9-]+)/submit_issue/$', 'submit_issue', None, 
        'project_submit_issue'),
    (r'^project/(?P<project_slug>[a-z0-9-]+)/(?P<issue_id>[0-9-]+)/$', 'view_issue', None,
        'project_issue'),
    (r'^project/(?P<project_slug>[a-z0-9-]+)/(?P<issue_id>[0-9-]+)/modify_issue/$', 
        'modify_issue', None, 'project_modify_issue'),
    (r'^project/(?P<project_slug>[a-z0-9-]+)/(?P<issue_id>[0-9-]+)/file_upload/$', 
        'issue_attach',
        None, 'project_file_upload'),

    ## Profile views
    (r'^profile/dashboard/$', 'dashboard', None, 'project_user_dashboard'),
    (r'^profile/detail/(?P<username>\w+)/$', 'view_profile', None, 'project_user'),
    (r'^profile/list/$', 'view_users', None, 'project_user_list'),
    (r'^profile/filter/delete/(?P<filter_id>[\d]+)/$', 'filter_delete', None,
        'project_filter_delete'),
)

urlpatterns += patterns('',
    (r'^profile/login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'djtracker/profile/login.html'},
        'project_login'),
    (r'^profile/logout/$', 'django.contrib.auth.views.logout', 
        {'template_name': 'djtracker/profile/logout.html', 'next_page': '/'},
        'project_logout'),    
    (r'^profile/password_change/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'djtracker/profile/password_change_form.html'}, 
        'password_change'),
    (r'^profile/password_change/done/$', 'django.contrib.auth.views.password_change_done',
        {'template_name': 'djtracker/profile/password_change_done.html'}, 
        'password_change_done'),
    (r'^profile/password_reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'djtracker/profile/password_reset_form.html'}, 
        'password_reset'),    
    (r'^profile/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', 
        {'template_name': 'djtracker/profile/password_reset_done.html'}, 
        'password_reset_done'),     
    (r'^profile/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'djtracker/profile/password_reset_confirm.html'}, 
        'password_reset_confirm'),
    (r'^profile/reset/done/$', 'django.contrib.auth.views.password_reset_complete',
         {'template_name': 'djtracker/profile/password_reset_complete.html'}, 
        'password_reset_complete'),     
)

## feeds
urlpatterns += patterns('',

    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
  {'feed_dict': feeds}, 'feeds'),
)