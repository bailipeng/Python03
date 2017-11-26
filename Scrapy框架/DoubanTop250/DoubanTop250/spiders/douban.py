# -*- coding: utf-8 -*-
import scrapy
from DoubanTop250.items import Doubantop250Item

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    # allowed_domains = ['douban.com']
    page = 0
    url = "https://movie.douban.com/top250?start="
    start_urls = [url+str(page),]

    def parse(self, response):
        item = Doubantop250Item()
        movies = response.xpath("//div[@class='info']")
        for each in movies:
            # 标题
            item['title'] = each.xpath(".//span[@class='title'][1]/text()").extract()[0]
            # 信息
            item['bd'] = each.xpath(".//div[@class='bd']/p/text()").extract()[0].strip().replace('\xa0','')
            # 评分
            item['star'] = each.xpath(".//div[@class='star']/span[@class='rating_num']/text()").extract()[0]
            # 简介
            quote = each.xpath(".//p[@class='quote']/span/text()").extract()
            if len(quote) !=0:
                item['quote'] = quote[0]
            yield item

            if self.page <225:
                self.page += 25
                yield scrapy.Request(self.url+str(self.page),callback=self.parse)




