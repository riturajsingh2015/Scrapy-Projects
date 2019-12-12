# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from  pymongo import MongoClient
#from scrapy.conf import settings


'''
class BooksSpiderScrapyOnlyPipeline(object):
    def process_item(self, item, spider):
        return item

'''
MONGODB_SERVER='localhost'
MONGODB_PORT=27017
MONGODB_DB='books'
MONGODB_COLLECTION='products'


class MongoDBPipeline(object):
    def __init__(self):
        connection=MongoClient(
        MONGODB_SERVER,
        MONGODB_PORT
        )
        db=connection[MONGODB_DB]
        self.collection=db[MONGODB_COLLECTION]

    def process_item(self,item,spider):
        self.collection.insert(dict(item))
        return item
