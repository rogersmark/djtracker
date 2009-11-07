from django.conf.urls.defaults import patterns

urlpatterns = patterns('djtracker.views',
    (r'^$', 'index', None, 'index'),
)
