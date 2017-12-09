from urllib import request
import json
from lxml import etree

headers = {'User-Agent':'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;'}
for i in range(1,100):
    base_url = "https://www.qiushibaike.com/8hr/page/{}/".format(i)
    print('正在解析第{}页'.format(i))
    response = request.Request(base_url,headers=headers)
    html = request.urlopen(response).read().decode('utf-8')
    text = etree.HTML(html)

    node_list = text.xpath('//div[contains(@id, "qiushi_tag")]')

    items ={}
    for node in node_list:
        # xpath返回的列表，这个列表就这一个参数，用索引方式取出来，用户名
        username = node.xpath('.//div[1]//h2')[0].text
        # 图片连接
        image = node.xpath('.//div[@class="thumb"]//@src')#[0]
        # 取出标签下的内容,段子内容
        content = node.xpath('.//div[@class="content"]/span')[0].text
        # 取出标签里包含的内容，点赞
        zan = node.xpath('.//i')[0].text
        # 评论
        comments = node.xpath('.//i')[1].text

        items = {
            "username" : username.replace('\n',''),
            "image" : image,
            "content" : content.replace('\n',''),
            "zan" : zan,
            "comments" : comments
        }

        with open("qiushi.json", "a",encoding='utf-8') as f:
            f.write(json.dumps(items, ensure_ascii = False) + "\n")