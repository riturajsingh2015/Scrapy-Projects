# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os


class PlayingWithImagesPipeline(object):
    def process_item(self, item, spider):
        os.chdir(r'C:\Users\Singh\Desktop\Scrapy\playing_with_images\downloaded_images')

        if item['images'][0]['path']:
        # if the file is already downloaded
        # successfully then rename it.
            new_image_name=item['title'][0]+'.jpg'
            new_image_path='full/'+new_image_name
            os.rename(item['images'][0]['path'],new_image_path)

        return item
