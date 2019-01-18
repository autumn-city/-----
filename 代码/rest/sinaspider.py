# -*- coding:utf-8 -*-
# python 3
# author: achetair

import requests
import re
import os
from urllib.parse import unquote
from urllib.parse import quote
from bs4 import BeautifulSoup
import SinaHtmlAnalyze as sinaHA
import SinaPageNum as sinaPN
import json

# 网易登录的网址
sina_login_url = 'https://passport.weibo.cn/sso/login'
sina_search_url = 'https://weibo.cn/search/?tf=5_012'

def generate_file_path(topic_id):
    # 使用的是绝对路径
    base_path = os.getcwd()
    child_path = base_path + '\\' + topic_id + '\\'
    return child_path




class Sina():
    def __init__(self, username, password):
        self.data = {
            'username': username,
            'password': password,
            'savestate': '1',
            'r':'https://weibo.cn/',
            'ec': 0,
            'pagerefer': 'https://weibo.cn/pub/',
            'entry': 'mweibo',
            'wentry':'',
            'loginfrom':'',
            'client_id':'',
            'code':'',
            'qq':'',
            'mainpageflag': 1,
            'hff':'',
            'hfp':''
        }

        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '186',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': '_T_WM=970d208bb637a6358f046853f0475cd8; SUHB=0G0ePzTJD0jyl9; SCF=Aq5_3vVwt1HOJDaO9yKyX3pQPvbiPhN-woGTwo9fT2XAc2VypTOGQn9FEQLEkGxMUiO0dmnqfImKD-Ni82iTQEc.; SUB=_2AkMsgbUrdcPxrAVSnv4QzWzlbo1H-jyfVNzdAn7oJhMyPRgv7go_qSdutBF-XEFSAJBu5rBKK3hx-alU1x28cPO-',
            'Host': 'passport.weibo.cn',
            'Origin': 'https://passport.weibo.cn',
            'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.__longin()

    # 登录函数
    # return：返回值为 session()
    def __longin(self):
        # 利用session进行登录
        self.s = requests.session()
        # r 局部变量， session类
        r=self.s.post(sina_login_url, data=self.data, headers=self.headers)
        # 获取session
        # print(r.text)
        # print(r.status_code)
        print('==============================')
        # print(r.text.encode(r.encoding).decode('utf-8'))
        # uni_json = json.loads(r.text)
        # msg= uni_json.get('msg')
        # print(msg.encode('utf-8').decode('unicode-escape'))

        # 状态为 200 ，表示登录成功
        if r.status_code == 200:
            print('*****Login Success************')
        else:
            print(r.status_code)
            print(r.text)
            print('*****Login Failed*************')
            exit(1)
        return self.s

    # 将获得的内容存入本地文件
    def write_file_content(self, file_name, content):
        open(file_name, 'w', encoding='utf-8').write(content.encode(self.encoding).decode('utf-8'))

    # 获取热搜的内容
    # return: {中文内容：search_url},search_url=http://....
    # html 为获取的页面
    def get_hot_search(self, html):
        print('**Beign to get compile search content')
        # 用Beautifulsoup 解析页面
        hot_soup = BeautifulSoup(html, 'html.parser')
        # 获取 html 的body
        body = hot_soup.body
        # print_lc(body.contents)
        # count = 4 ， 热搜的标签位置
        count = 0
        # hot_content 记录热搜的标签
        hot_content = ''
        # print(body)
        for i in body.contents:
            # print('attrs:'+str(i.attrs))
            # 获取相应的标签属性，存入 hot_content
            if 'c' in i.attrs['class']:
                count = count+1
                if count==4:
                    hot_content=i

        # 获取的网址格式是 /search/......
        # 创建网址的前缀
        url_base_path = 'https://weibo.cn'

        # 正则匹配页的内容
        # 匹配的表达式
        pa = re.compile(r'"[A-Za-z0-9%?+=/]{5,300}"')
        # 寻找对应标签的内容
        hot_uri = pa.findall(str(hot_content))
        # 将获取的内容存入字典
        word_url_key = {}
        for i in hot_uri:
            # hot_url 热搜的网址
            hot_url = url_base_path + i[1:-1]

            TIP that

            # 热搜的中文名称
            china_word = i[24:-1]
            # 热搜名称是 网络编码%32，需要进行解码
            word = unquote(china_word)
            # 存入字典
            word_url_key[word] = hot_url
        # 返回键值对
        return word_url_key

    # return： 返回页面 html 的纯文本信息
    # url： 需要爬取网址
    def get_url_content(self, url):
        # url = 'https://weibo.cn/search/?tf=5_012'
        r = self.s.get(url)
        self.encoding = r.encoding
        # print(r.text)
        return r.text

    def spider_topic(self, topic_id, url):
        print("=" * 40)
        print("Hot topic: {}, url:{}".format(topic_id, url))
        # 获取对应热搜的网页
        content = self.get_url_content(url)

        # 获取当前热搜对应的所有页数的url
        page_url_list = sinaPN.get_page_urllist(url=url, html=content)

        # 获取对应的网页并解析里面的内容
        weibo_list = []
        # 获取所有的页
        for i in  page_url_list:
            print('='*40)
            print("当前页数：" + i)
            print('='*40)
            html = self.get_url_content(i)
            # 获取所有的微博内容
            weibo_list.extend(sinaHA.get_weibo_list(html))

        # 生成文件夹存储内容
        # dir_path = generate_file_path(topic_id)
        # if not os.path.exists(dir_path):
        #     os.mkdir(topic_id)
        #
        result = json.dumps(weibo_list)

        # file_path = dir_path + topic_id + '.json'
        # self.write_file_content(file_path, result)
        return result
        # 热搜的文件单独存个文件夹
        # filename = 'hot_topic' + word + '.html'
        # print("="*40)
        # print("Hot topic page 1")
        # print(content)
        # self.write_file_content(filename, content)


    def auto_main(self):
        # 获取搜索界面的内容
        search_content = self.get_url_content(sina_search_url)
        # 获取热搜的字典
        hot_dic = self.get_hot_search(search_content)
        # 获取热搜字典的 第一个键值对
        word,url = get_dic_key_value(hot_dic)
        # 传入 spider_topic, 进一步操作
        json_data =  self.spider_topic(word, url)
        print("="*40)
        print("Spider is Over!")
        return json_data

    def manual_main(self, search_word):
        # 请输入你要搜索的内容
        uri = "https://weibo.cn/search/mblog/?keyword="
        # 对汉字进行url编码
        search = quote(search_word, 'utf-8')
        # 搜索的网页
        url = uri + search
        json_data = self.spider_topic(search_word, url)
        print("="*40)
        print("Spider is Over!")
        return json_data

def print_lc(lc):
    print('\n')
    print('-'*20)
    for i in lc:
        print('='*20)
        print(i)

# 返回字典的一个值
def get_dic_key_value(dic):
    for i in dic:
        return i, dic.get(i)

# Sina(username='15918248149', password='8oyd36rvei').main()
# Sina(username='18011298036', password='505514').main()
#Sina(username='tamheede@sina.com', password='giller7076').auto_main()

def ui():
    flag = True
    while flag:
        flag = False
        print('='*40)
        print('欢迎使用简易爬虫系统')
        print("请选择：")
        print('1:自动运行')
        print('2:手动输出搜索内容')
        choice = input('请输入您的选择数字：')
        if choice == '1':
            json_data = Sina(username='tamheede@sina.com', password='giller7076').auto_main()
            # print(json_data)
        elif choice == '2':
            search_word = input("请输入您的搜索内容：")
            json_data = Sina(username='tamheede@sina.com', password='giller7076').manual_main(search_word)
        else:
            print("您的输入不合法，请输入数字1或者2")
            flag = True


if __name__ == '__main__':
    ui()

