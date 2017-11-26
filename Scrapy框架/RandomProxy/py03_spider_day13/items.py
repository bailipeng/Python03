# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Py03SpiderDay13Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class XiciItem(scrapy.Item):
    host = scrapy.Field()
    port = scrapy.Field()
    http_type = scrapy.Field()