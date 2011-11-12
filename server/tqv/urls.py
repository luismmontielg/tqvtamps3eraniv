from django.conf.urls.defaults import *

urlpatterns = patterns('tqv.views',
    url(r'^$', 'index', name='index'),
    url(r'^rsvp-ajax/$', 'handle_rsvp', name='handle_rsvp'),
)