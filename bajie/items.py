# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BajieItem(scrapy.Item):
    id = scrapy.Field()
    filmId = scrapy.Field()
    filmsName = scrapy.Field()
    tags = scrapy.Field()
    countries = scrapy.Field()
    years = scrapy.Field()
    directors = scrapy.Field()
    stars = scrapy.Field()
    douban = scrapy.Field()
    filmLength = scrapy.Field()
    language = scrapy.Field()
    content = scrapy.Field()
    playAddr = scrapy.Field()
    types = scrapy.Field()
    createTime = scrapy.Field()
    updateTime = scrapy.Field()
    picAddr = scrapy.Field()
    downLink = scrapy.Field()
    types = scrapy.Field()
    playAddr = scrapy.Field()
    isExist = scrapy.Field()
    pass
