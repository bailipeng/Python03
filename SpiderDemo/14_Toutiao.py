import requests,json,re
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import RequestException
from hashlib import md5
import os
def get_page_index(offset,keyword):
    data={
        "offset": offset,
        "format": "json",
        "keyword": keyword,
        "autoload": "true",
        "count": "20",
        "cur_tab": "1",
    }

    url = "https://www.toutiao.com/search_content/?"+urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求错误')
        return None
def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print(e)
        print('请求详情页错误')
        return None

def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    image_pattern = re.compile(r'gallery: JSON.parse[(]"(.*?)"[)],\n', re.S)
    result = re.search(image_pattern, html)
    if result:
        result = result.group(1).replace('\\', '')
    try:
        data = json.loads(result)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images_urls = [item['url'] for item in sub_images]
            for image_url in images_urls:download_image(image_url)
            return {
                'title': title,
                'url': url,
                'images_url': images_urls
            }


    except Exception as e:
        print('解析失败')

def download_image(url):
    print('正在下载:',url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException as e:
        print(e)
        print('请求图片错误',url)
        return None
def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
def main():
    html = get_page_index(0,'街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            parse_page_detail(html,url)

if __name__ == '__main__':
    main()
