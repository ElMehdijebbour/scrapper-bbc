# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapperbbcItem(scrapy.Item):
    # Item key for Url
    url=scrapy.Field()
    
    # Item key for menu
    menu= scrapy.Field()

    # Item key for submenu
    submenu=scrapy.Field()

    # Item key for topic

    topic=scrapy.Field()

    # Item key for Title of the article
    title = scrapy.Field()
     
    # Item key for subtitle of the article
    subtitle = scrapy.Field()
     
    # Item key for text
    text = scrapy.Field()

    # Item key for date
    date= scrapy.Field()

    # Item key for images
    images = scrapy.Field()

    # Item key for authors
    authors = scrapy.Field()

    # Item key for videos
    video = scrapy.Field()
    pass
