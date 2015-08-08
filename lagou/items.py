# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    name = Field()
    catalog = Field()       #类别
    workLocation = Field()  #工作地点
    detailLink = Field()    #具体链接
    publishTime = Field()   #发布日期
    workDuty = Field()      #工作职责
    workRequire = Field()   #工作要求
    company = Field()       #招聘公司
    exp = Field()           #经验要求
    degrees  =  Field()     #学历要求
    property = Field()      #工作性质，全职或兼职
    temptation = Field()    #工作诱惑
    salary = Field()        #薪水
    
    pass
