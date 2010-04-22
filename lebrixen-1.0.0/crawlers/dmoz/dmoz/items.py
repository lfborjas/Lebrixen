# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class DmozItem(Item):
	parent_category = Field() #the parent of this category
	title = Field() #the title of this category
	path = Field() #the path to this category: {url, path}
	resources = Field(default = []) # the sites in this category: {title, desc, link}
	sub_categories = Field(default = []) #a dict of categories under this one: {title, desc}
