from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rsvp/', include('rsvp.urls')),
    url(r'^', include('tqv.urls')),
)

if not settings.PRODUCTION:
    #TODO: get this automatically, settings.MEDIA_URL without first /
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT},
            name='media'),
    )
