import scrapy
# from py03_spider_day13 import settings
from scrapy.conf import settings
import random

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    # allow_domains = ['xicidaili.com']
    start_urls = ['http://www.douban.com']

    def parse(self, response):
        #print(dir(response.request))
        # print(response.request.headers)
        # print(response.request.meta)
        print(response.text)
        # headers = {
        #     'User-Agent' : random.choice(settings['USER_AGENTS'])
        # }
        # yield scrapy.Request('http://www.xicidaili.com',headers=headers,callback=self.parsexici)