# -*- coding: utf-8 -*-
# @Time    : 2022/12/17
# @Author  : muyuweifeng
# @File    : bilitracker-1.0.py

print('欢迎使用bilibili搜索工具')
print('正在导入基本环境')
import os
os.system("cls")
print('正在导入其他依赖库')
from bs4 import BeautifulSoup #导入依赖库
import requests
import re
import time
from tqdm import tqdm,trange
import jieba
print('成功')
os.system("cls")

#函数定义
def strToValue(valueStr): #数字单位转换
    valueStr = str(valueStr)
    Yi       = valueStr.find('亿')
    Wan      = valueStr.find('万')
    if Yi != -1 and Wan != -1:
        return int(float(valueStr[:Yi])*1e8 + float(valueStr[Yi+1:Wan])*1e4)
    elif Yi != -1 and Wan == -1:
        return int(float(valueStr[:Yi])*1e8)
    elif Yi == -1 and Wan != -1:
        return int(float(valueStr[Yi+1:Wan])*1e4)
    elif Yi == -1 and Wan == -1:
        return int(valueStr)

def userInput():#将用户搜索内容转化为链接
    global keyword
    keyword   = input("请输入需要在 bilibi搜索引擎 分析的关键词   ")
    print("\n\n\n1.全部分区 2.动画 3.番剧 4.国创 5.音乐 \n6.舞蹈 7.游戏 8.知识 9.科技 10.运动 \n11.汽车 12.生活 13.美食 14.动物圈 15.鬼畜 \n16.时尚 17.资讯 18.娱乐 19.影视 20.纪录片 \n21.电影 22.电视剧")
    num = input('请输入所需要分析的分区编号')
    arealist = [0,1,13,167,3,129,4,36,188,234,223,160,211,217,119,155,202,5,181,177,23,11] #B站对应的分区号
    area = str(arealist[int(num)-1])
    urlo='https://search.bilibili.com/all?keyword='+ keyword + '&from_source=web_search&order=click&duration=0&tids_1=' + area + '&page='
    os.system("cls")
    return urlo

def totalPageGet(url): #获取总页码数量
    html          = requests.get(url)
    html.encoding ='utf-8'
    sp=BeautifulSoup(html.text,'html.parser')

    pageso = sp.select('#all-list > div.flow-loader > div.page-wrap > div > ul > li')  #总页数获取
    pages=[]
    for html in pageso:     #正则去除html标签
        dr = re.compile(r'<[^>]+>|\n| ',re.S)
        dd = dr.sub('',str(html))
        pages.append(dd)

    if len(pages)>0: #补充单页时页码
        totalpage = pages[len(pages)-2]
    else:
        totalpage= 1
    print("共计",totalpage,"页")
    return totalpage

def removeHtmlTags(list,type): #正则去除html标签,附加数字中含单位转换
    data=[]
    if type=='str': #文本类型不转换
        for html in list:     
            dr = re.compile(r'<[^>]+>|\n| ',re.S)
            dd = dr.sub('',str(html))
            data.append(dd)
    else:
        for html in list:     
            dr = re.compile(r'<[^>]+>|\n| ',re.S)
            dd = dr.sub('',str(html))
            df = strToValue(dd)
            data.append(df)
    return data

def wordFrequency(wordlist):
    frequency = ''
    counts ={}
    txt = jieba.lcut(str(wordlist))
    for word in txt:
        if len(word)==1:
            continue
        else:
            counts[word] = counts.get(word,0) + 1
    li = list(counts.items()) # 由大到小排序
    li.sort(key=lambda x:x[1], reverse=True)

    if len(li)>=20:
        max =21
    else:
        max = len(li)

    for i in range(1,max):
        key,value = li[i]
        frequency = frequency +'\n'+ ('{:<3}{:<6}{:>5}'.format(i,key,value))
    return frequency


####程序执行####
totalData     = []
totalTitle    = []
pageNum       = 1
urlo          = userInput()    #urlo为不含页码的链接,url为含页码的完全链接
url           = urlo + str(pageNum)
totalpage     = totalPageGet(url=url)
    
for pageNum in tqdm(range(1, int(totalpage) +1)):
    url = urlo + str(pageNum)
    html=requests.get(url)
    html.encoding='utf-8'
    sp=BeautifulSoup(html.text,'html.parser')

    bofang =sp.select('#all-list > div.flow-loader > ul > li > div > div > span.so-icon.watch-num')#原始数据获取(未去除html标签)
    
    for i in bofang:
        totalData.append(i)
    for i in range(1,21):
        selector ='#all-list > div.flow-loader > ul > li:nth-child('+str(i)+') > div > div.headline.clearfix > a'
        title  =sp.select(str(selector))
        if len(title)>=1:
            totalTitle.append(title[0])
    time.sleep(0.45)#防止速度过快被封禁
    pageNum=pageNum + 1

totalData = removeHtmlTags(list=totalData,type='num')
totalTitle = removeHtmlTags(list=totalTitle,type='str')
bfSum = sum(totalData)
result = wordFrequency(wordlist=totalTitle)
os.system("cls")
print('以下为分析结果：','\n'*2)
print('在与“',keyword,'”有关的',len(totalData),'个视频中',',所有视频总计有',bfSum,'个播放量。')
print('\n'*2,'在这些视频中,UP主们经常提到了这些词:')
print(result)
input()