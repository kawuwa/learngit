# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 11:24:39 2022

@author: biubiu皮卡康
"""

import pdfplumber as pdfr
import os

filedir=r'D:\学校课程\大数据分析及应用\第10章源代码汇总\第10章源代码汇总\公告'
fileslist=[]
for files in os.walk(filedir):
    for file in files[2]:
        print(file)
        if os.path.splitext(file)[1]=='pdf' or os.path.splitext(file)[1]=='PDF':
            fileslist.append(filedir+'\\'+file)
print(fileslist)

textall=[]
for i in range(len(fileslist)):
    pdf=pdfr.open(fileslist[i])
    pages=pdf.pages
    for page in pages:
        text=page.extract_text()
        textall.append(text)
    pdf.close()
textall=''.join(textall)

print(textall)

    
