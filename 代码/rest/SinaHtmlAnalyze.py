# -*- coding:utf-8 -*-
# python 3
# author: zou peinie

import bs4
from bs4 import BeautifulSoup
import json
import re

weibo_list=[]
# 一个字典的初始化
def init_dic():
    dict = {
        "weibo_id":None, # 微博名
        "content":None, # 内容
        "trans_num":None, # 转发量
        "comment_num":None, # 评论量
        "good_num":None, # 点赞数
        "pictures":[]
    }
    return dict


def match_num(string):
    #构建匹配数字的正则表达式
    pattern_flag=r'\d+'
    # 利用 re 库进行正则表达式的匹配
    num_find = re.compile(pattern=pattern_flag)
    try:
        temp = num_find.search(string).group(0)
    except AttributeError as abe:
        print("\33存在错误的字符串："+string)
        temp = 0
    except Exception as e:
        temp = 0
        print("\33未知的错误")
    return temp

# 输入 html
def func2(i, content):
    flag=0

    content_dic = init_dic()

    for j in i.find_all('div'):

        for child in j.descendants:
            if(type(child) == bs4.element.NavigableString):
                #print("In one "+child.string)
                content.join(str(child.string).strip())
                #print('content: '+content)
                content_dic['content'] = content
                if(flag == 0):
                    # 进行微博名称的匹配
                    print("微博名："+child)
                    content_dic['weibo_id'] = str(child)
                    flag=1
                    continue
                if('评论[' in child):
                    # 进行评论数的匹配
                    comment_num_str = child.string
                    print('评论数: '+comment_num_str)
                    comment_num = match_num(comment_num_str)
                    content_dic['comment_num'] = comment_num
                    content_dic['content'] = content
                    #评论是最后一个,所以直接return
                    return  content_dic
                if('转发[' in child):
                    if len(child.string) > 12:
                        continue
                    # 转发量的匹配
                    trans_num_str = child.string
                    if len(child.string) > 12:
                        continue
                    print('转发数: '+trans_num_str)
                    trans_num = match_num(trans_num_str)
                    content_dic["trans_num"]=trans_num
                    print("内容" + content)
                    continue
                if('赞[' in child):
                    if len(child.string) > 12:
                        continue
                    # 点赞数的匹配
                    good_num_str = child.string
                    print('点赞数: '+ good_num_str)
                    #print('内容:'+content)
                    good_num = match_num(good_num_str)
                    content_dic['good_num']=good_num
                    content_dic['content']=str(content)
                    continue
                else:
                    content= content+str(child.string).strip()
            elif(type(child.string) == bs4.element.Comment):
                continue
            elif('src' in child.attrs):
                print('图片:'+child.attrs['src'])
                # 存储的是picture的网址
                content_dic["pictures"].append(child.attrs['src'])

# 获取当前页面的微博
def get_weibo_list(html):
    # print(file_object.read())
    Soup=BeautifulSoup(html, 'html.parser')
    coun=0
    content=''
    for i in Soup.find_all('div', class_ = 'c', id = True):
        weibo_list.append(func2(i,content))
        print("="*40)
        coun=coun + 1
    print('='*40)
    #打印字典
    # for i in weibo_list:
    #     print(i)
    return weibo_list


if __name__ == '__main__':
    html_doc = open('1.html', encoding='utf-8').read()
    get_weibo_list(html_doc)
