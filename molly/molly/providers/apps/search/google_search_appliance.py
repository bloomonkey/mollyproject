import urllib, urllib2, logging, re

import xml.etree
import xml.parsers.expat

from django.http import Http404
from django.core.urlresolvers import Resolver404, reverse

from molly.apps.search.providers import BaseSearchProvider

logger = logging.getLogger("molly.providers.search.google_search_appliance")

class GSASearchProvider(BaseSearchProvider):

    SCHEME_HOST_RE = re.compile(r'[a-z\d]+:\/\/[a-z.\-\d]+\/')

    def __init__(self, search_url, domain, params={}, title_clean_re=None):
        self.search_url, self.domain, self.params = search_url, domain, params
        self.title_clean_re = re.compile(title_clean_re) if title_clean_re else None

    def perform_search(self, request, query, application=None):
    
        if application:
            domain = self.domain + reverse('%s:index' % application)[:-1]
        else:
            domain = self.domain 

        params = dict(self.params)
        params.update({
            'q': query,
            'output': 'xml',
            'ie': 'utf8',
            'oe': 'utf8',
            'as_sitesearch': domain,
        })

        try:
            response = urllib2.urlopen('?'.join((self.search_url, urllib.urlencode(params))))
        except urllib2.HTTPError, e:
            logger.exception("Couldn't fetch results from Google Search Appliance")
            return []

        try:
            xml_root = xml.etree.ElementTree.parse(response)
        except xml.parsers.expat.ExpatError, e:
            logger.exception("Couldn't parse results from Google Search Appliance")
            return []
            
        results = []
    
        for result in xml_root.findall('.//RES/R'):
            # Retrieve the URL and chop off the scheme and host parts, leaving
            # just the local part.
            url = result.find('U').text
            url = self.SCHEME_HOST_RE.sub('/', url)

            title = result.find('T').text
            try:
                title = self.title_clean_re.match(title).group(1)
            except AttributeError:
                pass
                            
            metadata = {
                'url': url,
                'excerpt': (result.find('S').text or '').replace('<br>', ''),
                'title': title,
            }
            
            try:
                metadata.update(self.get_metadata(request, url))
            except (Resolver404, Http404):
                continue
                
            results.append(metadata)
            
        return results
        