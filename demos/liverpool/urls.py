from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from molly.conf import applications, all_apps

admin.autodiscover()

all_apps()

urlpatterns = patterns('',
    (r'^adm/', include(admin.site.urls)),

    # These are how we expect all applications to be eventually.
    (r'^contact/', applications.contact.urls),
#    (r'^service-status/', applications.service_status.urls),
    (r'^weather/', applications.weather.urls),
    (r'^library/', applications.library.urls),
    (r'^archives/', applications.archives.urls),
#    (r'^podcasts/', applications.podcasts.urls),
#    (r'^webcams/', applications.webcams.urls),
#    (r'^results/', applications.results.urls),
#    (r'^search/', applications.search.urls),
    (r'^geolocation/', applications.geolocation.urls),
    (r'^places/', applications.places.urls),
#    (r'^transport/', applications.transport.urls),
    (r'^feedback/', applications.feedback.urls),
#    (r'^news/', applications.news.urls),
    (r'^external-media/', applications.external_media.urls),
    (r'^device-detection/', applications.device_detection.urls),
    (r'^maps/', applications.maps.urls),
    (r'^desktop/', applications.desktop.urls),
    (r'^url-shortener/', applications.url_shortener.urls),
    (r'^feature-suggestions/', applications.feature_vote.urls),
    (r'^favourites/', applications.favourites.urls),

    (r'^comments/', include('django.contrib.comments.urls')),

    (r'', applications.home.urls),

#    (r'^auth/', applications.auth.urls),
#    (r'^weblearn/', applications.weblearn.urls),
    (r'^stats/', applications.stats.urls),

    (r'^reverse/$', 'molly.utils.views.ReverseView', {}, 'reverse'),
#    (r'^events/', applications.events.urls),

    # These ones still need work

)

# Redirecting old URLs
urlpatterns += patterns('django.views.generic.simple',
    (r'^maps/busstop:(?P<atco>[A-Z\d]+)/(?P<remain>.*)$', 'redirect_to', {'url': '/places/atco:%(atco)s/%(remain)s'}),
    (r'^maps/[a-z]\-+:(?P<id>\d{8})/(?P<remain>.*)$', 'redirect_to', {'url': '/places/oxpoints:%(id)s/%(remain)s'}),
    (r'^maps/[a-z]\-+:(?P<id>[NW]\d{8})/(?P<remain>.*)$', 'redirect_to', {'url': '/places/osm:%(id)s/%(remain)s'}),
    (r'^maps/(?P<remain>.*)$', 'redirect_to', {'url': '/places/%(remain)s'}),
    (r'^osm/(?P<remain>.*)$', 'redirect_to', {'url': '/maps/osm/%(remain)s'}),
)


handler500 = 'molly.apps.home.views.handler500'

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.SITE_MEDIA_PATH})
    )
