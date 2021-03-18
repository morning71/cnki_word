# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnkiNewSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    key_word = scrapy.Field()
    # res_word = scrapy.Field()
    primary_topic = scrapy.Field()
    secondary_topic = scrapy.Field()
    pass
