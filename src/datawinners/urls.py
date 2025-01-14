# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enablSubscribe Nowe the admin:
# from django.contrib import admin
# admin.autodiscover()
import settings
from django.contrib import admin

js_info_dict = {
    'packages': ('datawinners',),
}

urlpatterns = patterns('',
                       (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
                       (r'', include('datawinners.accountmanagement.urls')),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       (r'', include('datawinners.project.urls')),
                       (r'', include('datawinners.smstester.urls')),
                       (r'', include('datawinners.submission.urls')),
                       (r'', include('datawinners.maps.urls')),
                       (r'', include('datawinners.dashboard.urls')),
                       (r'', include('datawinners.location.urls')),
                       (r'', include('datawinners.alldata.urls')),
                       (r'', include('datawinners.entity.urls')),
                       (r'', include('datawinners.home.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
