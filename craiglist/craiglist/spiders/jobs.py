# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['berlin.craigslist.org']
    start_urls = ['https://berlin.craigslist.org/']

    def parse(self, response):
        country_name=response.xpath('//h2[@class="area"]/text()').extract_first()
        jobs_text=response.xpath('//*[@id="jjj"]/h4/a/span/text()').extract_first()
        urls=response.xpath('//*[@id="jjj0"]/li/a/@href').extract()
        abs_urls=[response.urljoin(url) for url in urls]
        titles = response.xpath('//*[@id="jjj0"]/li/a/span/text()').extract()
        #for title , url in zip(titles,abs_urls):
        #    print((title,url))
        search_urls=['software', 'system', 'web']
        #top_page_urls=
        for url in abs_urls:
            # if we want to pass the data in parse method to parse_page we use
            # meta argument.
            if any(x in url for x in search_urls):
                print('Searching in :', url)
                yield Request(url , callback=self.parse_page , meta ={'country_name': country_name , 'jobs_text':jobs_text})

    def parse_page(self, response):
        # note inorder to generalize we need to make it language independent as well ####
        # to access the meta in parse_page do this #
        country_name=response.meta['country_name']
        jobs_text=response.meta['jobs_text']
        #print(country_name)
        #print(jobs_text)

        page_header=response.xpath('//*[@id="query"]/@placeholder').extract_first().replace('durchsuchen','')

        link_titles=response.xpath('//*[@id="sortable-results"]/ul/li/p/a/text()').extract()
        link_urls=response.xpath('//*[@id="sortable-results"]/ul/li/p/a/@href').extract()

        for url in link_urls:
            yield Request(url , callback=self.parse_job)

    def parse_job(self, response):
        job_title=response.xpath('//*[@id="titletextonly"]/text()').extract_first()
        info_title1= response.xpath('/html/body/section/section/section/div[1]/p/span[1]/text()').extract_first()
        info_data1= response.xpath('/html/body/section/section/section/div[1]/p/span[1]/b/text()').extract_first()
        info_title2= response.xpath('/html/body/section/section/section/div[1]/p/span[2]/text()').extract_first()
        info_data2= response.xpath('/html/body/section/section/section/div[1]/p/span[2]/b/text()').extract_first()
        desc= response.xpath('//*[@id="postingbody"]/text()').extract()
        '''
        print('Title :',job_title)
        print(info_title1 ,':', info_data1)
        print(info_title2 ,':', info_data2)
        print('\n')
        print('Description ')
        print('=============================')

        print(desc)
        print('==========END================')
        print('\n\n')
        '''
        desc=''.join(desc)
        yield {
        'Job Title' : job_title,
        info_title1:info_data1,
        info_title2:info_data2#,
        #'Description': desc

        }
