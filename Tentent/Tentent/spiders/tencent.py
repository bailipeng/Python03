# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule#
from Tentent.items import TencentItem

class TencentSpider(CrawlSpider):
    name = 'tencent'
    # allowed_domains = ['tencent.com']
    start_urls = ["http://hr.tencent.com/position.php?&start=0#a"]

    #rules中包含一个或多个Rule对象，每个Rule对爬取网站的动作定义了某种特定操作，比如提取当前相应内容里的特定链接，是否对提取的链接跟进爬取
    rules = (
        # Rule(link_extractor, callback = None, cb_kwargs = None, follow = None,process_links = None, process_request = None)
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_item', follow=True),
            #LinkExtractor()匹配所需要的url链接, 返回一个linkextractor对象 它是Rule()里所需要的参数之一,
    )

    def parse_item(self, response):
        for each in response.xpath('//*[@class="even"]'):
            name = each.xpath('./td[1]/a/text()').extract()[0]
            detailLink = each.xpath('./td[1]/a/@href').extract()[0]
            positionInfo = each.xpath('./td[2]/text()').extract()[0]

            peopleNumber = each.xpath('./td[3]/text()').extract()[0]
            workLocation = each.xpath('./td[4]/text()').extract()[0]
            publishTime = each.xpath('./td[5]/text()').extract()[0]


            item = TencentItem()
            item['name']=name
            item['detailLink']=detailLink
            item['positionInfo']=positionInfo
            item['peopleNumber']=peopleNumber
            item['workLocation']=workLocation
            item['publishTime']=publishTime

            yield item

