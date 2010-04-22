import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from dmoz.items import DmozItem

class DmozSpider(CrawlSpider):
    domain_name = 'dmoz.org'
    start_urls = [#'http://www.dmoz.org/World/Espa%C3%B1ol/Ciencia_y_tecnolog%C3%ADa/',
		  'http://www.dmoz.org/Science/']
    #the sub-categories of a category (names):
    #//table[2]/tr/td/ul/li/a/b/text()

    #the sub-category links of a category:
    #//table[2]/tr/td/ul/li/a/@href
   
    #the sub-category list: 
    #//table[2]/tr/td/ul/li

    #(for es)
    #it appears that in some categories the sub-categories are in table 4, not 3, or 2 :(
    #(for en) the sub-cats are always in the table 2

    #the resources for a category (uniform for es and en): '//ul[2]/li'
    #description: //ul[2]/li/text()
    #title: '//ul[2]/li/a/text()'
    #link: //ul[2]/li/a/@href	    

    rules = (
        Rule(SgmlLinkExtractor(allow_domains='dmoz.org',deny=r'.*/?Regional/?.*' restrict_xpaths='//table[2]/tr/td/ul/li'), 'parse_item', follow=True),
    )

    def parse_item(self, response):
        xs = HtmlXPathSelector(response)
        i = DmozItem()
	route = xs.select('/html/head/title/text()').extract()
        i['parent_category'], i['title'] = route[0].split(':')[-2:]
        i['path'] = {'url':str(response.url), 'ontology_path': route[0]}
	i_resources = []
        resources = xs.select('//ul[2]/li')
	try:
		for resource in resources:
			description = resource.select('text()').extract()[0]
			title = resource.select('a/text()').extract()[0]
			link = resource.select('a/@href').extract()[0]
			i_resources += [{'title': title, 'description': description, 'link': link},]
	except:
		pass
	i['resources'] = i_resources

	i_subcats= []
	subcats = xs.select('//table[2]/tr/td/ul/li')
	try:
		for subcat in subcats:
			title = subcat.select('a/b/text()').extract()[0]
			link = subcat.select('a/@href').extract()[0]
			i_subcats += [{'title': title, 'link': link},]
	except:
		pass
	i['sub_categories'] = i_subcats
	
        return i

SPIDER = DmozSpider()
