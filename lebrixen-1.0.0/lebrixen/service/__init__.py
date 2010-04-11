#utility functions to support the web service
import simplejson as json
from django.http import HttpResponse
from topia.termextract import extract
from django.utils.html import strip_tags
from urllib2 import urlopen
from django.utils.http import urlencode
from django.conf import settings
from xml.dom.minidom import parse
import re
import logging

#some more listed here: http://en.wikipedia.org/wiki/Term_extraction
#and here: http://maui-indexer.blogspot.com/2009/07/useful-web-resources-related-to.html
#and here: http://stackoverflow.com/questions/1100549/term-extraction-generatings-tags-out-of-text
#also here: http://faganm.com/blog/2010/01/02/1009/
WEB_SERVICES = {
    #http://www.alchemyapi.com/api/keyword/textc.html
    'alchemy': 'http://access.alchemyapi.com/calls/text/TextGetRankedKeywords',
    #http://wordsfinder.com/api_Keyword_Extractor.php
    'wordsfinder': 'http://www.wordsfinder.com/extraction/api1.php',
    #http://developer.yahoo.com/search/content/V1/termExtraction.html
    'yahoo': 'http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction',
}

class WebServiceException(Exception):
    def __init__(self, service, msg):
        self.service = service
        self.msg= msg
    def __str__(self):
        return "An error ocurred with a call to %s: %s" % (self.service, self.msg)

def json_view(func):
	"""
		Decorator for web-service views: takes the request and json-izes it, and
		also takes any response that is not a direct HttpResponse and json-izes it
		taken from: http://andrewwilkinson.wordpress.com/2009/04/08/building-better-web-services-with-django-part-1/
	"""
	def wrap(req, *args, **kwargs):
		try:
		    j = json.loads(req.raw_post_data)
		except ValueError:
		    #this means that the necessary data is in the request.REQUEST
		    #j = None
		    j = req.REQUEST or None

		resp = func(req, j, *args, **kwargs)

		if isinstance(resp, HttpResponse):
		    return resp

		return HttpResponse(json.dumps(resp, ensure_ascii=False), mimetype="application/json")

	return wrap

def _sanitize_text(raw_text):
    """
        Does whatever is needed to get just text from the input
    """
    return strip_tags(raw_text)

def web_extract_terms(text, service='yahoo'):
    """
        Given a text, extract keyword terms with the selected web_service
    """
    service = service.lower().strip()

    if not service in WEB_SERVICES.keys():
        raise Exception('%s is an invalid web service, possible choices are %s' % (service, repr(WEB_SERVICES.keys())))

    #1. Build the query:
    query = {}
    apikey = settings.WEB_SERVICES_KEYS.get(service, '')

    if service == 'wordsfinder':
        query = {
            'apikey' : apikey,
            'context': text
        }
    elif service == 'alchemy':
        query = {
            'apikey' : apikey,
            'text' : text,
            'outputMode' : 'json'
        }
    elif service == 'yahoo':
        query = {
            'appid': apikey,
            'context': text,
            'output': 'json'
        }

    #2. Try to call the service:
    resp = None
    try:
        logging.debug('requesting %s' % WEB_SERVICES[service]+'?%s'%urlencode(query))
        resp_url = urlopen(WEB_SERVICES[service], urlencode(query))
        resp = resp_url.read()
        logging.debug( "%s returned %s" % (service, resp))
    except Exception as e:
        #TODO: retry in timeouts and stuff
        logging.debug('Error in request: %s' % e)
        pass

    #3. Process the response:    
    if resp:
        if service == 'alchemy':
            data = json.loads(resp)
            if data['status'] == 'ERROR':
                raise WebServiceException(service, 'call returned error status')
            return [re.sub('-[^ ] ', '', e['text']) for e in data['keywords']]
            
        elif service == 'yahoo':
            data = json.loads(resp)
            return data['ResultSet']['Result']

        elif service == 'wordsfinder':
            parsed_response = parse(resp)
            e = parsed_response.getElementsByTagName('error')
            if e:
                raise WebServiceException(service, 'error code %s' % e)
            else:
                return parsed_response.getElementsByTagName('keyword')

    # TODO: maybe find a way to call 'em all and have a super-set of kws?
    else:
        return ''

def build_query(text, language='', use_web_service = False, web_service='yahoo'):
    """
        Given raw text and a language, build a query to submit to the search engine.
        The use of a web service is optional only for english. For other languages,
        a web service will be used regardless of the use_web_service param.
    """
    query_terms = []
    #process english language queries, use the topia.termextract utility
    if 'en' in language.lower() and not use_web_service:
        #currently, there's a bug in the topia software which initializes incorrectly if
        #another tagger is passed in the constructor
        extractor = extract.TermExtractor()

        #sanitize the text (remove html tags)
        text = _sanitize_text(text)

        #extract terms from the text:
        query_terms = extractor(text)
    else:
        #if not in english, use a webservice to get the terms:
        query_terms = web_extract_terms(text, service=web_service)

    return u' '.join(query_terms)


        


