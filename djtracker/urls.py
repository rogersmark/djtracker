from django.conf.urls.defaults import patterns

urlpatterns = patterns('djtracker.views',
    (r'^$', 'index', None, 'index'),
    (r'project/(?P<project_slug>\w+)/$', 'project_index', None, 'project-index'),
)
