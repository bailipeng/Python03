import requests
from urllib import request
from lxml import etree

# 处理详情页
def parse_detail(url):
    pre_url = 'https://tieba.baidu.com'
    response = requests.get(pre_url + url)
    html = response.text
    html = etree.HTML(html)

    pic_list = html.xpath('//cc//img[@class="BDE_Image"]/@src')
    for url in pic_list:
        fname = url.split('/')[-1]
        request.urlretrieve(url,'./images/' + fname)

# 获取列表页
def getPage():
    pn = 0
    while pn < 50:
        base_url = 'https://tieba.baidu.com/f?pn=%d'
        response = requests.get(base_url % pn,params={'kw':'美女'})
        html = response.text
        print(html)
        html = etree.HTML(html)

        detai_urls = html.xpath('//div[@id="content_leftList"]//div[@class="threadlist_title pull_left j_th_tit "]//a/@href')
        for detai_url in detai_urls:
            print(detai_url)
            parse_detail(detai_url)
        pn += 50

if __name__ == '__main__':
    getPage()
