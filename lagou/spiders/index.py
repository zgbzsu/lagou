# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from lagou.items import *
import json
class IndexSpider(scrapy.Spider):
    name = "index"
    allowed_domains = ["lagou.com"]
    start_urls = (
        'http://www.lagou.com/',
    )
    def parse_item(self,response):
        item = response.meta['item'].copy()
        sel =  BeautifulSoup(response.body,"html5lib")
        div = sel.find("dd",attrs={"class":"job_bt"})
        item['workDuty'] = div.get_text().strip().replace(" ","").replace("\n","")
        yield item
    def parse_list(self,response):
        item = response.meta['item']
        url= response.url;
        tmp = url.split("=")
        pn = int(tmp[-1])
        data = json.loads(response.body)
        if len(data['content']['result'])!=0:
            url = "=".join(tmp[:-1])+"="+str(pn+1)
            yield Request(url,meta={'item': item},callback=self.parse_list)
        if 1:
            for i in data['content']['result']:
                nitem = item.copy()
                nitem['name'] = i['positionName']
                nitem['workLocation'] = i['city']
                nitem['publishTime'] = i['createTime'][:-2]
                nitem['company'] = i['companyShortName']
                nitem['exp'] = i['workYear']
                nitem['degrees'] = i['education']
                nitem['property'] = i['jobNature']
                nitem['temptation'] = i['positionAdvantage']
                nitem['salary'] = i['salary']
                nitem['detailLink'] = self.start_urls[0]+"jobs/"+str(i['positionId'])+".html"
                yield Request(nitem['detailLink'],meta={'item': nitem},callback=self.parse_item)
    def parse(self, response):
        sel =  BeautifulSoup(response.body,"html5lib")
        mboxs = sel.find_all("div",attrs={"class":"menu_box"})
        for m in mboxs:
            cate1 = m.find("h2").get_text().strip()
            dls = m.find_all("dl",attrs={"class":"reset"})
            for dl in dls:
                cate2 = dl.find("dt").get_text().strip()
                dds = dl.find("dd").find_all('a')
                for dd in dds:
                    cate3 = dd.get_text().strip()
                    href = dd['href']
                    item = LagouItem()
                    item['catalog'] = cate1+","+cate2+","+cate3
                    kd = href.split("/")[-1]
                    #if not kd=="Python":continue
                    url = self.start_urls[0]+"jobs/positionAjax.json?px=default&first=true&kd="+kd+"&pn=1"
                    yield Request(url,meta={'item': item},callback=self.parse_list)
