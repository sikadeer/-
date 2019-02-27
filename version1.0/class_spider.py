import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time


class DataSpider(object):
    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        self.s = requests.Session()
        self.s.headers.update(self.headers)
        self.link = []
        self.unitprice = []
        self.structure = []
        self.storey = []
        self.size = []
        self.age = []
        self.decorate = []
        self.loc = []
        self.xp=[]
        self.yp=[]

    def GetLink(self, url):  # 爬取网页并返回其文本内容
        try:
            req_link = self.s.get(url)
            req_link.encoding = req_link.apparent_encoding
            text1 = req_link.text
            text1 = BeautifulSoup(text1, "html.parser")
            div1 = text1.find_all(name='a', attrs={'class': 'img'})
            self.link.extend([re.findall(r'href="(.*?)"', str(x))[0] for x in div1])
            return self.link
        except:
            print('爬取异常')
            pass

    def GetHtmlText(self, url):
        req_text = requests.get(url, headers=self.headers)
        req_text.encoding = req_text.apparent_encoding
        text = req_text.text
        return text

    def GetUnitprice(self, text):
        self.unitprice.append(re.findall(r'<b>(\d+?)</b>', text)[0] if re.findall(r'<b>(\d+?)</b>', text) else np.nan)
        return self.unitprice

    def GetStructure(self, text):
        self.structure.append(
            re.findall(r'房屋户型</span>(.*?)</li>', text)[0] if re.findall(r'房屋户型</span>(.*?)</li>', text) else np.nan)
        return self.structure

    def GetStorey(self, text):
        self.storey.append(
            re.findall(r'所在楼层</span>(.*?)楼层', text)[0] if re.findall(r'所在楼层</span>(.*?)楼层', text) else np.nan)
        return self.storey

    def GetSize(self, text):
        self.size.append(
            re.findall(r'建筑面积</span>(.*?)㎡', text)[0] if re.findall(r'建筑面积</span>(.*?)㎡', text) else np.nan)
        return self.size

    def GetAge(self, text):
        self.age.append(
            re.findall(r'建成年代</span>(.*?)</li>', text)[0] if re.findall(r'建成年代</span>(.*?)</li>', text) else np.nan)
        return self.age

    def GetDecorate(self, text):
        self.decorate.append(
            re.findall(r'装修情况</span>(.*?)</li>', text)[0] if re.findall(r'装修情况</span>(.*?)</li>', text) else np.nan)
        return self.decorate

    def GetLoc(self, text):
        self.loc.append(re.findall(r'<div class="wrapper">(.*?)\d', text)[0] if re.findall(r'<div class="wrapper">(.*?)\d',                                                                    text) else np.nan)
        return self.loc

    def GetXY(self,loc):
        loc=['上海'+str(x) for x in loc]
        for i in loc:
            url = '''https://apis.map.qq.com/jsapi?qt=poi&wd={0:s}&pn=0&rn=10&rich_source=qipao
                    &rich=web&nj=0&c=1&key=FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS&output=jsonp&pf=jsapi
                    &ref=jsapi&cb=qq.maps._svcb3.search_service_0'''.format(i)
            text=self.GetHtmlText(url)
            x= re.findall(r'"pointx":"?(.*?)"?,', text)
            y= re.findall(r'"pointy":"?(.*?)"?,', text)
            print('正在获取第{0:d}/{1:d}条数据…………'.format(loc.index(i)+1,len(loc)))
            self.xp.append(x[1] if x else np.nan)
            self.yp.append(y[1] if y else np.nan)
        return self.xp,self.yp


if __name__ == '__main__':
    COUNT = 100
    DELAY = 30

    spider = DataSpider()

    for i in range(COUNT):  # 爬取、抓取网页前500页的有效信息
        if i % 20 == 0 and i > 0:  # 每爬取50页sleep30s防止被识别
            time.sleep(DELAY)
        url = r'https://sh.lianjia.com/chengjiao/pg{:d}ng1nb1/'.format(i + 1)
        link = spider.GetLink(url)
        for j in link:
            print('正在获取第{0:d}页第{1:d}条数据…………'.format(i+1,link.index(j)+1))
            text = spider.GetHtmlText(j)
            spider.GetUnitprice(text)
            spider.GetStructure(text)
            spider.GetStorey(text)
            spider.GetSize(text)
            spider.GetAge(text)
            spider.GetDecorate(text)
            spider.GetLoc(text)
    link = spider.link
    unitprice = spider.unitprice
    structure = spider.structure
    storey = spider.storey
    size = spider.size
    age = spider.age
    decorate = spider.decorate
    loc = spider.loc
    spider.GetXY(loc)
    xp=spider.xp
    yp=spider.yp

    datafram = pd.DataFrame(np.array([unitprice,structure,storey,size,age,decorate,loc,xp,yp]))
    datafram.to_csv('data1.csv')
    d = pd.read_csv('data1.csv')
    d=d.drop('Unnamed: 0', axis=1)
    d.index =['unitprice','structure','storey','size','age','decorate','loc','xp','yp']
    d.T.to_excel('data1.xls')