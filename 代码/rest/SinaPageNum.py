# -*- coding:utf-8 -*-
# python 3
# author: huang yi

import requests
from bs4 import BeautifulSoup

def getallnum(html):
    allpage_num = None

    # url:要访问热搜的链接
    # headers:请求头
    # Query_parameters:请求参数
    soup = BeautifulSoup(html, "html.parser")
    # hrml_soup = soup.getHtmlText(url)
    # 获取总页码
    test_1=soup.find_all('input')
    # print(test_1)
    for i in test_1:
        if i['type']=='hidden':
            if i['name']=='mp':
                allpage_num = i['value']
                # print(i)
            # print(allpage_num)
    # nextPs = soup.find('div', class_='scott')


    # if nextPs:
    #     links=nextPs.find_all('a')
    #     if len(links)-2 <= 0:
    #         allpage_num = 1
    #     else:
    #         allpage_num = int(links[len(links)-2].text)
    # else:
    #     allpage_num = 1

    # print(allpage_num)
    return allpage_num

def get_page_urllist(url, html):
    if url == '':
        return None
    allpage_num = getallnum(html)
    url_list = []
    print("=" * 40)
    print("微博包含的页数")
    for i in range(1, int(allpage_num)+1):
        url_i = url +'&page='+str(i)
        print("url:"+url_i)
        url_list.append(url_i)
    return url_list



if __name__ == "__main__":
    html = open("1.html","r",encoding='utf-8')
    hot_uri = 'https://weibo.cn/search/mblog/?keyword=nba'
    get_page_urllist(hot_uri, html)


