# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self): # this function will not have response ,
    # since there is no start_url defined here.
        self.driver = webdriver.Chrome(r'C:\Users\Singh\Downloads\chromedriver_win32\chromedriver.exe')
        site_url='http://books.toscrape.com/'
        self.driver.get(site_url)
        page_source=self.driver.page_source
        sel=Selector(text=page_source)
        books=sel.xpath('//h3/a/@href').extract()# we will get the book url's
        for book in books:
            url= site_url + book
            yield Request(url,callback=self.parse_book)

        while True:
            try:
                next_page=self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 Seconds.')
                next_page.click()

                page_source=self.driver.page_source
                sel=Selector(text=page_source)
                books=sel.xpath('//h3/a/@href').extract()# we will get the book url's
                for book in books:
                    url= site_url +'catalogue/' + book
                    yield Request(url,callback=self.parse_book)
            except NoSuchElementException:
                self.logger.info('No More pages to load')
                self.driver.quit()
                break


    def parse_book(self,response):
        '''
        As you can see, all what you need is to use is  response.request.url
        to get the URL of the current request.
        Actually, you could even use response.url to get the URL from the response,
        but the former would be more accurate in the case there are redirections.

        '''
        title = response.css('h1::text').extract_first()
        url = response.request.url
        yield {'title': title, 'url':url}

        '''
        Yes, you should use this code *without* defining anything in items.py.
        Using a dictionary should be the same as using items.
        '''
        '''
        Second Method
        If you rather want to use items, your way should work as well. Add the following to items.py under  class BooksCrawlerItem(scrapy.Item)

        url = scrapy.Field()
        title = scrapy.Field()
        Then in the books.py import from books_crawler.items import BooksCrawlerItem changing the names based on your project.

        Then add the following parse function:

        def parse_book(self, response):
            items = BooksCrawlerItem()
            title = response.css('h1::text').extract_first()
            url = response.request.url

            items['title'] = title
            items['url'] = url
            yield items
        The items method should work as well. But do not use parts of one way in the other way to avoid unexpected results.

        '''
