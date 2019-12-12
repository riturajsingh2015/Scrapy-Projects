# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayingWithImagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title =scrapy.Field()
    price=scrapy.Field()
    image_urls=scrapy.Field() ##image_urls should be named the same
    images=scrapy.Field() #images should be named the same 
    # automatically generated using the "image pipeline"
    # this is due to changes made in the settings.py file
