# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 11:24:39 2022

@author: biubiu皮卡康
"""

import pdfplumber as pdfr
import os
import re
from selenium import webdriver
import time
import jieba
from wordcloud import WordCloud
from imageio import imread

# hrefs=[]
# #<span class="total-box" style="">共 11 条 当前显示1-10条</span>
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser=webdriver.Chrome(options=chrome_options)
# #browser = webdriver.Chrome()
# url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=飞机'
# browser.get(url)

# data = browser.page_source
# pnumber='<span class="total-box" style="">共.*?(\d+).*?条.*?当前'
# number=re.findall(pnumber,data)
# #pages=int(eval(number[0])/10)+1

# for i in range(70):
#     time.sleep(3)
    
#     data = browser.page_source
#     # print(data)
    
#     p_title = '<span title="" class="r-title">(.*?)</span>'
#     p_href = '<a target="_blank" href="(.*?)" data-id='
#     p_date = '<span class="time">(.*?)</span>'
    
#     title = re.findall(p_title, data)[5:]
#     href = re.findall(p_href, data)[5:]
#     date = re.findall(p_date, data, re.S)[5:]
#     #print(number[0])
#     #print(title)
    
    
#     for j in range(len(title)):
        
#         title[j]=re.sub('<.?em>','',title[j])
#         href[j] = 'http://www.cninfo.com.cn' + href[j]
#         href[j] = re.sub('amp;', '', href[j])
#         date[j] = date[j].strip()  # 清除空格和换行符
#         date[j] = date[j].split(' ')[0]  # 只取“年月日”信息，不用“时分秒”信息
    
#     #去重
    
            
        
#     #     if '腾讯控股' not in title[j]:
#     #         title[j]=''
#     #         href[j]=''
#     #         date[j]=''
            
#     #     print(str(j + 1) + '.' + title[j] + ' - ' + date[j])
#     #     print(href[j])
        
#     # while '' in title:
#     #     title.remove('')
#     # while '' in href:
#     #     href.remove('')
#     # while '' in date:
#     #     date.remove('')
#     print(title)
#     print('第{}页成功'.format(i+1))
    
#     for m in range(len(href)):
        
#         if 'http://www.cninfo.com.cn' not in href[m]:
#             href[m]='http://www.cninfo.com.cn'+href[m]
#         href[m]=re.sub('amp;','',href[m])
#         #amp;出现在链接中
#         hrefs.append(href[m])
#     #InvalidArgumentException: invalid报错原因是网址格式错误
        
#     browser.find_element("css selector",'i.el-icon-arrow-right').click()

# print(len(hrefs))
# browser.quit()

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')

# chrome_options = webdriver.ChromeOptions()
# prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'D:\学校课程\大数据分析及应用\第10章源代码汇总\第10章源代码汇总\公告'} #这边你可以修改文件储存的位置
# chrome_options.add_experimental_option('prefs', prefs)
# browser = webdriver.Chrome(chrome_options=chrome_options)
# #browser=webdriver.Chrome()
# for n in hrefs:
    
#     url = n
#     time.sleep(3)
#     print(url)
#     browser.get(url)
#     data2 = browser.page_source
    
#     try:
#         browser.find_element("css selector",'button.el-button:nth-child(1)').click()
#     except:
#         print('发生错误')
#         #为什么打印不出来？
        
# time.sleep(20)      
# browser.quit()


filedir=r'D:\学校课程\大数据分析及应用\第10章源代码汇总\第10章源代码汇总\公告'
fileslist=[]
for files in os.walk(filedir):
    for file in files[2]:
        
        if os.path.splitext(file)[1]=='.pdf' or os.path.splitext(file)[1]=='.PDF':
            fileslist.append(filedir+'\\'+file)
#获取文件列表

textall=[]
tableall=[]
for i in range(len(fileslist)):
    pdf=pdfr.open(fileslist[i])
    pages=pdf.pages
    for page in pages:
        text=page.extract_text()
        textall.append(text)
        table=page.extract_table()
        if not table:
            continue
        tableall.append(table)
    pdf.close()
    print('\n\n\n')
    print('第{}个pdf爬取成功'.format(i+1))
textall=''.join(textall)
tabletext=''
for table in tableall:
    for rc in table:
        for cc in rc:
            if not cc:
                continue
            tabletext+=cc
tabletext=re.sub('\n','',tabletext)
alltext=textall+tabletext

#一张表格在两页怎么办

# print(textall)
# print(tabletext)

for ch in '。；，：」「“”（）、？《》!"#$%&()*+,-./:;<=>?@`[\\]^_‘{|}~\'0123456789':
    alltext=alltext.replace(ch," ")
alltext=alltext.replace('\u3000'," ")
alltext=alltext.replace('\n'," ")
words = jieba.lcut(alltext)                                #汉字精确分词


smtext=set(words)

dictw={}
for h in smtext:
    #print(words.count(h))
    dictw[h]=words.count(h)
lsdic=list(dictw.items())

lsdic.sort(key = lambda x:x[1], reverse=True)

qian50=[]
d=lsdic[0][1]
count=1
for l in lsdic:
    if l[1]<d:
        count+=1
    if count>51:
        break
    qian50.append(l)
print(qian50[1:])
print(len(qian50))

lisnew=[]
for g in qian50[1:]:
    for k in range(g[1]):
        lisnew.append(g[0])

newtxt = ' '.join(lisnew)                                      #空格拼接中文词

bg_pic = imread('plane.jpg')

wordcloud = WordCloud(background_color='white',max_words=50,mask=bg_pic,font_path=r"C:\Windows\Fonts\SIMKAI.TTF").generate(' '.join(words))   #生成词云，font_path="msyh.ttc"为选择微软雅黑字体

image = wordcloud.to_image()
#display(image)
wordcloud.to_file('pdfanalyze.png')	# 保存图片
    


    
