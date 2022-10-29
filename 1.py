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

hrefs=[]
#<span class="total-box" style="">共 11 条 当前显示1-10条</span>
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser=webdriver.Chrome(options=chrome_options)
#browser = webdriver.Chrome()
url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=中泰证券'
browser.get(url)

data = browser.page_source
pnumber='<span class="total-box" style="">共.*?(\d+).*?条.*?当前'
number=re.findall(pnumber,data)
#pages=int(eval(number[0])/10)+1

for i in range(60):
    time.sleep(3)
    
    data = browser.page_source
    # print(data)
    
    p_title = '<span title="" class="r-title">(.*?)</span>'
    p_href = '<a target="_blank" href="(.*?)" data-id='
    p_date = '<span class="time">(.*?)</span>'
    
    title = re.findall(p_title, data)
    href = re.findall(p_href, data)
    date = re.findall(p_date, data, re.S)
    #print(number[0])
    print(title)
    
    
    for j in range(len(title)):
        title[j] = re.sub(r'<.*?>', '', title[j])
        href[j] = 'http://www.cninfo.com.cn' + href[j]
        href[j] = re.sub('amp;', '', href[j])
        date[j] = date[j].strip()  # 清除空格和换行符
        date[j] = date[j].split(' ')[0]  # 只取“年月日”信息，不用“时分秒”信息
        if '公告' not in title[j]:
            title[j]=''
            href[j]=''
            date[j]=''
            
        print(str(j + 1) + '.' + title[j] + ' - ' + date[j])
        print(href[j])
        
    while '' in title:
        title.remove('')
    while '' in href:
        href.remove('')
    while '' in date:
        date.remove('')
    
    print('第{}页成功'.format(i+1))
    
    for m in range(len(href)):
        
        if 'http://www.cninfo.com.cn' not in href[m]:
            href[m]='http://www.cninfo.com.cn'+href[m]
        href[m]=re.sub('amp;','',href[m])
        #amp;出现在链接中
        hrefs.append(href[m])
    #InvalidArgumentException: invalid报错原因是网址格式错误
        
    browser.find_element("css selector",'i.el-icon-arrow-right').click()
    
browser.quit()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

chrome_options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'D:\学校课程\大数据分析及应用\第10章源代码汇总\第10章源代码汇总\公告'} #这边你可以修改文件储存的位置
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)
#browser=webdriver.Chrome()
for n in hrefs:
    
    url = n
    time.sleep(3)
    print(url)
    browser.get(url)
    data2 = browser.page_source
    
    try:
        browser.find_element("css selector",'button.el-button:nth-child(1)').click()
    except:
        print('此链接不是一个pdf文件')
        #为什么打印不出来？
        
time.sleep(20)      
browser.quit()


filedir=r'D:\学校课程\大数据分析及应用\第10章源代码汇总\第10章源代码汇总\公告'
fileslist=[]
for files in os.walk(filedir):
    for file in files[2]:
        print(file)
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
            tabletext+=cc
tabletext=re.sub('\n','',tabletext)
alltext=textall+tabletext

#一张表格在两页怎么办

# print(textall)
# print(tabletext)
print(alltext)

words = jieba.lcut(alltext)                                        #汉字精确分词
newtxt = ' '.join(words)                                       #空格拼接中文词
wordcloud = WordCloud(font_path=r"C:\Windows\Fonts\FZSTK.TTF").generate(newtxt)   #生成词云，font_path="msyh.ttc"为选择微软雅黑字体
image = wordcloud.to_image()
display(image)                              #显示词云图
#wordcloud.to_file('pdfanalyze.png')	# 保存图片

    
