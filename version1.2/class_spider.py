import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import sqlite3
import time


class DataSpider(object):
    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        self.s = requests.Session()
        self.s.headers.update(self.headers)
        self.conn = sqlite3.connect('data.db')
        self.cu = self.conn.cursor()
        self.cu.execute('''create table if not exists data
            (unit_price,structure,storey,size,age,decorate,loc,xp,yp)''')

    def GetLink(self, url):
        try:
            link=[]
            req_link = self.s.get(url)
            req_link.encoding = req_link.apparent_encoding
            text1 = req_link.text
            text1 = BeautifulSoup(text1, "html.parser")
            div1 = text1.find_all(name='a', attrs={'class': 'img'})
            link.extend([re.findall(r'href="(.*?)"', str(x))[0] for x in div1])
            return link
        except:
            pass

    def GetHtmlText(self, url,data=None):
        req_text = requests.get(url, data=data,headers=self.headers)
        req_text.encoding = req_text.apparent_encoding
        text = req_text.text
        return text

    def Getunit_price(self, text):
        unit_price=re.findall(r'<b>(\d+?)</b>', text)[0] if re.findall(r'<b>(\d+?)</b>', text) else np.nan
        return unit_price

    def GetStructure(self, text):
        structure=re.findall(r'房屋户型</span>(.*?)</li>', text)[0] if re.findall(r'房屋户型</span>(.*?)</li>', text) else np.nan
        return structure

    def GetStorey(self, text):
        storey=re.findall(r'所在楼层</span>(.*?)楼层', text)[0] if re.findall(r'所在楼层</span>(.*?)楼层', text) else np.nan
        return storey

    def GetSize(self, text):
        size=re.findall(r'建筑面积</span>(.*?)㎡', text)[0] if re.findall(r'建筑面积</span>(.*?)㎡', text) else np.nan
        return size

    def GetAge(self, text):
        age=re.findall(r'建成年代</span>(.*?)</li>', text)[0] if re.findall(r'建成年代</span>(.*?)</li>', text) else np.nan
        return age

    def GetDecorate(self, text):
        decorate=re.findall(r'装修情况</span>(.*?)</li>', text)[0] if re.findall(r'装修情况</span>(.*?)</li>', text) else np.nan
        return decorate

    def GetLoc(self, text):
        loc=re.findall(r'<div class="wrapper">(.*?)\d', text)[0] if re.findall(r'<div class="wrapper">(.*?)\d',text) else np.nan
        return loc

    def GetXY(self,loc):
        location='上海'+str(loc)
        url = '''https://apis.map.qq.com'''
        data={'qt': 'poi',
                'wd': location,
                'pn': 0,
                'rn': 10,
                'rich_source': 'qipao',
                'rich': 'web',
                'nj': 0,
                'c': 1,
                'key': 'FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS',
                'output': 'jsonp',
                'pf': 'jsapi',
                'ref': 'jsapi',
                'cb': 'qq.maps._svcb3.search_service_0'}
        text=self.GetHtmlText(url,data=data)
        x= re.findall(r'"pointx":"?(.*?)"?,', text)
        y= re.findall(r'"pointy":"?(.*?)"?,', text)
        xp=x[1] if len(x)>1 else np.nan
        yp=y[1] if len(y)>1 else np.nan
        return xp,yp

    def SaveData(self,data):
        self.cu.execute('insert into data values(?,?,?,?,?,?,?,?,?)', data)
        self.conn.commit()


if __name__ == '__main__':
    COUNT = 300
    DELAY = 30
    spider = DataSpider()
    for i in range(COUNT):  # 爬取、抓取网页前300页的有效信息
        if i % 20 == 0 and i > 0:  # 每爬取20页sleep30s防止被识别
            time.sleep(DELAY)
        url = r'https://sh.lianjia.com/chengjiao/pg{:d}ng1nb1/'.format(i + 1)
        link = spider.GetLink(url)
        for j in link:
            print('正在获取第{0:d}页第{1:d}条数据…………'.format(i+1,link.index(j)+1))
            text = spider.GetHtmlText(j)
            unit_price=spider.Getunit_price(text)
            structure=spider.GetStructure(text)
            storey=spider.GetStorey(text)
            size=spider.GetSize(text)
            age=spider.GetAge(text)
            decorate=spider.GetDecorate(text)
            loc=spider.GetLoc(text)
            xp,yp=spider.GetXY(loc)
            data=[unit_price,structure,storey,size,age,decorate,loc,xp,yp]
            spider.SaveData(data)
    conn=spider.conn
    conn.close()