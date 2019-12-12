# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
import os
import glob

def product_info(response,value):
    xpth='//th[text()="'+ value +'"]/following-sibling::td/text()'
    return response.xpath(xpth).extract_first()


class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    #def __init__(self,category=None): # scrapy crawl books -a category="http://books.toscrape.com/catalogue/category/books/philosophy_7/index.html"
        # Here we used cateory as an cmd-line argument
        # for our particular site if you want to scrap
        # only philosophy related urls
        # then we need to set start_url on the go
        # instead of setting it in the start as above
        # and comment start_urls above
        #self.start_urls=[category]
        #pass


    def parse(self, response):
        '''
        # if self.cateory:
        #    print('category is intialized')
        '''

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
        title = response.css('h1::text').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_url=response.xpath('//img/@src').extract_first()
        image_url=image_url.replace('../..','http://books.toscrape.com')
        rating=response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating=rating.replace('star-rating','')
        description= response.xpath('//*[@id="content_inner"]/article/p/text()').extract_first()
        upc=product_info(response,"UPC")
        availablity=product_info(response,"Availability")

        yield{
        'title':title,
        'price':price,
        'image_url':image_url,
        'rating':rating,
        'description':description,
        'upc':upc,
        'availablity':availablity
        }

    '''
    def close(self,reason):
    # this function is called when the scraper
    #has finished scraping
        csv_file=max(glob.iglob('*.csv'),key=os.path.getctime) # get the .csv file
        # which has been created just now. So to say the file that
        # has been passed as argument.
        os.rename(csv_file,'foobar.csv') # rename the file
    '''
