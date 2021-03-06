# Django settings for oxford project.

from oauth.oauth import OAuthSignatureMethod_PLAINTEXT
import os.path
from molly.conf.settings import Application, extract_installed_apps, Authentication, ExtraBase, Provider
from secrets import SECRETS

project_root = os.path.normpath(os.path.dirname(__file__))

DEBUG = False
DEBUG_SECURE = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = SECRETS.database_name             # Or path to database file if using sqlite3.
DATABASE_USER = SECRETS.database_user             # Not used with sqlite3.
DATABASE_PASSWORD = SECRETS.database_password         # Not used with sqlite3.
DATABASE_HOST = SECRETS.database_host             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site-media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = SECRETS.secret_key

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'molly.wurfl.middleware.WurflMiddleware',
#    'molly.auth.middleware.SecureSessionMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
#    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
#    'django.contrib.messages.context_processors.messages',
    'molly.wurfl.context_processors.wurfl_device',
    'molly.wurfl.context_processors.device_specific_media',
    'molly.geolocation.context_processors.geolocation',
    'molly.apps.feedback.context_processors.full_path',
)


ROOT_URLCONF = 'molly_oxford.urls'

TEMPLATE_DIRS = (
    os.path.join(project_root, 'templates'),
    # This is temporary until we move the templates to their rightful places
    #os.path.join(project_root, '..', '..', 'molly', 'templates'),
)

APPLICATIONS = [
    Application('molly.apps.home', 'home', 'Home',
        display_to_user = False,
    ),

    Application('molly.apps.contact', 'contact', 'Contact search',
        provider = 'molly.providers.apps.contact.ScrapingContactProvider',
    ),

    Application('molly.apps.places', 'places', 'Places',
        providers = [
            Provider('molly.providers.apps.maps.NaptanMapsProvider',
                method='ftp',
                username=SECRETS.journeyweb[0],
                password=SECRETS.journeyweb[1],
                areas=('340',),
            ),
            Provider('molly.providers.apps.maps.PostcodesMapsProvider',
                codepoint_path = '/var/cache/molly/codepo_gb.zip',
                import_areas = ('OX',),
            ),
            'molly.providers.apps.maps.OxontimeMapsProvider',
            'molly.providers.apps.maps.OxpointsMapsProvider',
            'molly.providers.apps.maps.OSMMapsProvider',
        ],
        nearby_entity_types = (
            ('Transport', (
                'bicycle-parking', 'bus-stop', 'car-park', 'park-and-ride',
                'taxi-rank', 'train-station')),
            ('Amenities', (
                'atm', 'bank', 'bench', 'medical', 'post-box', 'post-office',
                'public-library', 'recycling', 'bar', 'food', 'pub')),
            ('Leisure', (
                'cinema', 'theatre', 'museum', 'park', 'swimming-pool',
                'sports-centre', 'punt-hire')),
            ('University', (
                'university-library', 'college-hall', 'faculty-department',
                'building', 'room')),
        ),

    ),

    Application('molly.apps.z3950', 'library', 'Library search',
        verbose_name = 'Oxford Library Information System',
        host = 'library.ox.ac.uk',
        database = 'MAIN*BIBMAST',
    ),

    Application('molly.apps.podcasts', 'podcasts', 'Podcasts',
        providers = [
            Provider('molly.providers.apps.podcasts.OPMLPodcastsProvider',
                url = 'http://rss.oucs.ox.ac.uk/metafeeds/podcastingnewsfeeds.opml',
            ),
            Provider('molly.providers.apps.podcasts.RSSPodcastsProvider',
                podcasts = [
                    ('top-downloads', 'http://rss.oucs.ox.ac.uk/oxitems/topdownloads.xml'),
                ],
            ),
        ]
    ),

    Application('molly.apps.webcams', 'webcams', 'Webcams'),

    Application('molly_oxford.apps.results', 'results', 'Results releases'),

    Application('molly.apps.weather', 'weather', 'Weather',
        location_id = 'bbc/25',
        provider = Provider('molly.providers.apps.weather.BBCWeatherProvider',
            location_id = 25,
        ),
    ),

    Application('molly.apps.service_status', 'service_status', 'Service status',
        providers = [
            'molly.providers.apps.service_status.OUCSStatusProvider',
            Provider('molly.providers.apps.service_status.RSSModuleServiceStatusProvider',
                name='Oxford Library Information Services',
                slug='olis',
                url='http://www.lib.ox.ac.uk/olis/status/olis-opac.rss')
        ],
    ),

    Application('molly.apps.search', 'search', 'Search',
        providers = [
            Provider('molly.providers.apps.search.ApplicationSearchProvider'),
            Provider('molly.providers.apps.search.GSASearchProvider',
                search_url = 'http://googlesearch.oucs.ox.ac.uk/search',
                domain = 'm.ox.ac.uk',
                params = {
                    'client': 'oxford',
                },
                title_clean_re = r'm\.ox \| (.*)',
            ),
        ],
        display_to_user = False,
    ),

    Application('molly.apps.feeds', 'feeds', 'Feeds',
        providers = [
            Provider('molly.providers.apps.feeds.RSSFeedsProvider'),
        ],
        display_to_user = False,
    ),

    Application('molly.apps.feeds.news', 'news', 'News'),

    Application('molly.osm', 'osm', 'OpenStreetMap',
        display_to_user = False,
    ),

    Application('molly.geolocation', 'geolocation', 'Geolocation',
        prefer_results_near = (-1.25821, 51.75216, 5000),
        providers = [
            Provider('molly.providers.apps.geolocation.PlacesGeolocationProvider'),
            Provider('molly.providers.apps.geolocation.CloudmadeGeolocationProvider',
                search_locality = 'Oxford',
            ),
        ],
        display_to_user = False,
    ),

    Application('molly.apps.feedback', 'feedback', 'Feedback',
        display_to_user = False,
    ),

    Application('molly.apps.external_media', 'external_media', 'External Media',
        display_to_user = False,
    ),

    Application('molly.wurfl', 'device_detection', 'Device detection',
        display_to_user = False,
        expose_view = True,
    ),

#    Application('molly.apps.url_shortener', 'url_shortener', 'URL Shortener',
#        display_to_user = False,
#    ),

#    Application('molly.auth', 'auth', 'Authentication',
#        display_to_user = False,
#        secure = True,
#    ),

#    Application('molly.apps.sakai', 'weblearn', 'WebLearn',
#        host = 'https://weblearn.ox.ac.uk/',
#        service_name = 'WebLearn',
#        secure = True,
#        tools = [
#            ('signup', 'Tutorial sign-ups'),
#            ('poll', 'Polls'),
#            ('direct', 'User information'),
#            ('sites', 'Sites'),
#        ],
#        extra_bases = (
#            ExtraBase('molly.auth.oauth.views.OAuthView',
#                secret = SECRETS.weblearn,
#                signature_method = OAuthSignatureMethod_PLAINTEXT(),
#                base_url = 'https://weblearn.ox.ac.uk/oauth-tool/',
#                request_token_url = 'request_token',
#                access_token_url = 'access_token',
#                authorize_url = 'authorize',
#            ),
#        ),
#    ),

#    Application('molly.apps.feeds.events', 'events', 'Events',
#    ),
]

API_KEYS = {
    'cloudmade': SECRETS.cloudmade,
    'google': SECRETS.google,
    'yahoo': SECRETS.yahoo,
    'fireeagle': SECRETS.fireeagle,
}

SITE_MEDIA_PATH = os.path.join(project_root, 'site-media')

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'molly.batch_processing',
    'molly.utils',
#    'debug_toolbar',
) + extract_installed_apps(APPLICATIONS)

CACHE_DIR = '/var/cache/molly'
SRID = 27700

FIXTURE_DIRS = [
    os.path.join(project_root, 'fixtures'),
]

INTERNAL_IPS = ('127.0.0.1',)  # for the debug_toolbar
