# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PsnGameItem(scrapy.Item):
    game_name = scrapy.Field()
    game_url = scrapy.Field()
    platform = scrapy.Field()
    domain = scrapy.Field()
    image_url = scrapy.Field()
    origin_price = scrapy.Field(serializer=int)
    buy_price = scrapy.Field(serializer=int)
    ps_plus_price = scrapy.Field(serializer=int)


