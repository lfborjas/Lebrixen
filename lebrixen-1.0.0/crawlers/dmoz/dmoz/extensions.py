from scrapy.xlib.pydispatch import dispatcher
from scrapy.core import signals
import os
from scrapy.mail import MailSender
from scrapy.conf import settings

class EmailInClosing(object):
	def __init__(self):
	        dispatcher.connect(self.engine_closed, signal=signals.engine_stopped)
	
	def engine_closed(self):
		script = os.path.join(settings.get('ROOT_PATH'), 'asciitree.py')		
		result = os.path.join(settings.get('ROOT_PATH'), 'dirtree.txt')
		dirtree = os.path.join(settings.get('ROOT_PATH'), 'Top')
		os.system("%s -f %s > %s" % (script, dirtree, result))
		attached_file = open(result, 'r')
		mailer = MailSender()
		mailer.send(to = ['lfborjas@unitec.edu'],
			   subject = "All the docs are downloaded!",
			   body = "Attached is the directory structure",
			   attachs = [('structure', 'text/plain', attached_file)])
		attached_file.close()

