# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.conf import settings
from scrapy.core.exceptions import NotConfigured
from scrapy.contrib.exporter import jsonlines
import re
import os
from scrapy.contrib.exporter import BaseItemExporter
import cStringIO
import pyPdf
try:
	import json
except:
	import simplejson as json

ROOT_PATH = settings.get("ROOT_PATH")
if not ROOT_PATH:
	raise NotConfigured('A root path MUST be provided in settings!')

class DmozPipeline(object):
	def __init__(self):
		self.exporter = BaseItemExporter()
	
	def process_item(self, domain, item):
	        """Store the item, serialized as json, in a file within a directory hierarchy corresponding to it's
		   place in the ontology
	        """
        	#the path is of the form: cat/subcat/leaf
	        filedir = os.path.join(ROOT_PATH,'Top',item['category'])	
		#replace evil characters for an underscore 
		#cf. http://www.linfo.org/file_name.html
		filename = os.path.join(filedir, re.sub('[ /.$%]+','_',item['name']))
		if item['type'] == 'pdf':
			content_str = "%s(pdf).pdf" % filename
			temp = open( content_str, 'wb')
			temp.write(item['content'])
			temp.close()	
			item['content'] = content_str
		if not os.path.isdir(filedir):
			os.makedirs(filedir)
		file = open(filename, 'w')
		itemdict = dict(self.exporter._get_serialized_fields(item))
		json.dump(itemdict, file)
		file.close()
		return item
		
       	
