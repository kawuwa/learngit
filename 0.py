# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:44:59 2022

@author: biubiu皮卡康
"""

from selenium import webdriver
import re
import time

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

for i in range(50):
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
        
        
#browser.quit()
