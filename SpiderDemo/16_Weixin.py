from urllib.parse import urlencode
from requests.exceptions import ConnectionError
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
keyword = 'python'
headers = {
    'Cookie':'IPLOC=CN1100; SUID=521545791F2D940A0000000059F9A690; weixinIndexVisited=1; CXID=DB3554B9EA9DF4165F2C264B998D5443; SUV=00784AE4794515525A14F19E9475E023; ad=pyllllllll2zjl@4lllllVokxkllllllWUUqUkllll9lllll4Oxlw@@@@@@@@@@@; SUID=521545792313940A0000000059F9A690; SMYUV=1512614655485540; UM_distinctid=1602edbf6b363a-034544f90e17f2-7b113d-e1000-1602edbf6b4bd0; ABTEST=0|1512614720|v1; SNUID=B6F1A09CE5E1BA52EBF09245E5183B89; sct=2; JSESSIONID=aaaa2o73nSttY9GcjSv8v; ppinf=5|1512616673|1513826273|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozOTolRTUlOTMlQTYlN0UlRTUlQTUlQkQlRTclOUElODQlRTMlODAlODJ8Y3J0OjEwOjE1MTI2MTY2NzN8cmVmbmljazozOTolRTUlOTMlQTYlN0UlRTUlQTUlQkQlRTclOUElODQlRTMlODAlODJ8dXNlcmlkOjQ0Om85dDJsdUJnRUR5QXVaTVVKT3RYbnotUm44Q0VAd2VpeGluLnNvaHUuY29tfA; pprdig=W-rqWmOvr6Ju_hYLJoLcc0bVcLtG1kHFMBHfrI2c0KvXLYTs8rvS-H0T9988wUy1D5QiyX7eeGtwODznUr9mhANCYGk9pDS40b2HAqYe7DHYGnrbRyo3Wiz172RRSghPqRZAG2yv9Cr4kVFrrhAncHZ9FYkny7NHfA-iNk_XygA; sgid=01-23363283-AVoosuHptQTl2zqXt5nPxlw; ppmdig=1512616673000000687c0b1afbec3387bfd3bf177919a120',
    'Host':'weixin.sogou.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}
base_url = "http://weixin.sogou.com/weixin?"
proxy = None
max_count = 5
def get_proxy():
    try:
        r = requests.get('http://127.0.0.1:5555/random')
        if r.status_code == 200:
            proxy = BeautifulSoup(r.text, "lxml").get_text()
            return proxy.strip()
        return None
    except ConnectionError:
        return None

def get_html(url):
    global proxy
    print('正在抓取',url)
    # print('第{}次请求'.format(count))
    # if count>=max_count:
    #     print('请求超出次数限制')
    #     return None
    try:
        if proxy:
            proxies = {
                'http':'http://'+str(proxy),
                'https':'https://'+str(proxy)
            }
            response = requests.get(url,allow_redirects = False,headers=headers,proxies=proxies)
        else:
            response = requests.get(url,allow_redirects = False,headers=headers)
        if response.status_code ==200:
            return response.text
        if response.status_code == 302:
            print('302错误')
            proxy = get_proxy()
            if proxy:
                print('使用代理',proxy)
                return get_html(url)
            else:
                print('获取代理失败')
                return None
    except ConnectionError as e:
        # print('超出最大请求次数:{}'.format(count))
        proxy = get_proxy()
        # count+=1
        return get_html(url)


def get_index(keyword,page):
    data = {
        'query' : keyword,
        'type' : 2,
        'page' : page
    }
    queries = urlencode(data)
    url = base_url+queries
    html = get_html(url)
    return html
def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None
def parse_detail(html):
    doc = pq(html)
    title = doc('.rich_media_title').text()
    content = doc('.rich_media_content').text()
    date = doc('#post-date').text()
    nickname = doc('#post-user').text()
    # wechat = doc('#js_profile_qrcode > div > p:ntn-child(3) > span').text()
    return {
        'title':title,
        'content':content,
        'date':date,
        'nickname':nickname,
        # 'wechat':wechat,
    }
def main():
    for page in range(1,101):
        html = get_index(keyword,page)

        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    print(article_data)
if __name__ == '__main__':
    main()
