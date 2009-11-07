from django.conf.urls.defaults import patterns

urlpatterns = patterns('djtracker.views',
    (r'^$', 'project_index', None, 'project_index'),
)
