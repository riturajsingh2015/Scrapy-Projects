# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
import os
import glob
from scrapy.loader import ItemLoader
from playing_with_images.items import PlayingWithImagesItem


class ImagesSpider(Spider):
    name = 'images'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    #for the purpose of this example we will use images pipeline
    # that is supplied by the scrapy itself
    # in Settings.py file change the following :-
    ######################################
    # Robot =False
    # itempipelines change to 'scrapy.pipelines.images.ImagesPipeline':1
    # set place where you want to store the downloaded Images
    # IMAGES_STORE = "C:\Users\Singh\Desktop\Scrapy\playing_with_images\downloaded_images"
    ######################################
    # if we want to rename the files to title of the files
    # for this purpose we use Pipelines
    # we make the changes to the Pipeline.py file:
    # as done in the file
    #

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url=response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        '''
        #process next page
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url=response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)
        '''
    def parse_book(self,response):
        l =ItemLoader(item=PlayingWithImagesItem(),response=response)
        title = response.css('h1::text').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_urls=response.xpath('//img/@src').extract_first() #image_urls should be named the same 
        image_urls=image_urls.replace('../..','http://books.toscrape.com')
        l.add_value('title',title)
        l.add_value('price',price)
        l.add_value('image_urls',image_urls)
        # note image is added automatically as item using the image pipeline
        return l.load_item()
