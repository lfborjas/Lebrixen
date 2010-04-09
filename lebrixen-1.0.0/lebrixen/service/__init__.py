import simplejson as json
from django.http import HttpResponse

def json_view():
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
		    j = request.REQUEST or None	

		resp = func(req, j, *args, **kwargs)

		if isinstance(resp, HttpResponse):
		    return resp

		return HttpResponse(json.dumps(resp, ensure_ascii=False), mimetype="application/json")

	return wrap
	
