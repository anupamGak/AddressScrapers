# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AddressItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    pureaddr = scrapy.Field()
    pin = scrapy.Field()
    city = scrapy.Field()
    loc = scrapy.Field()
    subloc = scrapy.Field()
    lmark = scrapy.Field()

class AirtItem(scrapy.Item):
    city = scrapy.Field()
    sname = scrapy.Field()
    address = scrapy.Field()
