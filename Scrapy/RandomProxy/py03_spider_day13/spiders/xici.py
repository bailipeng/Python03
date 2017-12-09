# -*- coding: utf-8 -*-
import scrapy
from py03_spider_day13.items import XiciItem

class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/1']

    def parse(self, response):
        proxy_list = response.css('table#ip_list tr')[1:]
        for proxy in proxy_list:
            item = XiciItem()
            # css 选择器获取代理信息
            td_list = proxy.css('td::text').extract()
            host = td_list[0]
            port = td_list[1]
            http_type = td_list[5]
            if http_type.strip() == '':
                http_type = 'http'

            item['host'] = host
            item['port'] = port
            item['http_type'] = http_type

            yield item

        # 构造下一页请求
        next_url = response.css('a.next_page::attr(href)').extract()
        if next_url:
            yield scrapy.Request('http://www.xicidaili.com' + next_url[0],callback=self.parse)