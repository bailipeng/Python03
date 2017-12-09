# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree


xname = input('请输入小说名:')
baseurl = "http://zhannei.baidu.com/cse/search?searchtype=complex&q={}&s=18140131260432570322".format(xname)

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

res = requests.get(baseurl,headers=headers)
html_doc=str(res.content,'utf-8')
text = etree.HTML(html_doc)
novel_link = text.xpath('//div[@class="result-list"]/div[1]//h3/a/@href')[0]

detail = requests.get(novel_link,headers=headers)
detail_doc = str(detail.content,'utf-8')
detail_text = etree.HTML(detail_doc)
c_links = detail_text.xpath('//div[@id="yulan"]/li/a/@href')
c_titles = detail_text.xpath('//div[@id="yulan"]/li/a/text()')

for c_link,c_title in zip(c_links,c_titles):
    print('正在下载: {}'.format(c_title))
    c_doc = requests.get(c_link,headers=headers)
    try:
        c_doc = str(c_doc.content,'gbk')
        c_text = etree.HTML(c_doc)
        c_txt = ''.join(c_text.xpath('//div[@class="book_content"]/text()')).replace('\r\n','\n').replace('\xa0',' ')
        print(c_txt)
        with open(xname+'.txt','a',encoding='utf-8') as f:
            f.write(c_txt)
    except Exception as e:
        print(e,'下载失败')
