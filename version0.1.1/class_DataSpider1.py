import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time

class DataSpider1(object):
    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        self.s = requests.Session()
        self.s.headers.update(self.headers)

    def GetHtmlText(self, url):  # 爬取网页并返回其文本内容
        try:
            req = self.s.get(url)
            req.encoding = req.apparent_encoding
            text = req.text
            text = BeautifulSoup(text, "html.parser")
            return text
        except:
            print('爬取异常')
            return

    def GetLocSize(self, text):  # 通过正则表达式抓取房屋位置和面积信息
        div = text.find_all(name='div', attrs={'class': 'houseInfo'})
        loc = [re.findall(r'target="_blank">(.*?)</a>', str(x))[0] for x in div]
        size = [x.split('|')[-1] for x in [re.findall(r'厅|(\d\d.*?)平', str(x))[0] for x in div]]
        return loc, size

    def GetAge(self, text):  # 通过正则表达式抓取房龄信息
        div = text.find_all(name='div', attrs={'class': 'positionInfo'})
        age = [re.findall(r'(\d+?)年', str(x))[0] if re.findall(r'(\d+?)年', str(x)) else np.nan for x in div]
        return age

    def GetPrice(self, text):  # 通过正则表达式抓取房屋单价信息
        div = text.find_all(name='div', attrs={'class': 'unitPrice'})
        price = [re.findall(r'data-price="(\d+?)"', str(x))[0] for x in div]
        return price


def SaveData1(houseloc, houseage, housesize, unitprice):  # 简单处理后分别存储数据的csv和excel文件
    houseloc = np.array(houseloc, dtype=str)
    houseage = 2019. - np.array(houseage, dtype=float)
    housesize = np.array(housesize, dtype=str)
    unitprice = np.array(unitprice, dtype=str)
    datafram = pd.DataFrame(np.array([houseloc, houseage, housesize, unitprice]))
    datafram.to_csv('data1.csv')
    d = pd.read_csv('data1.csv')
    d.drop('Unnamed: 0', axis=1)
    d.index = ['houseloc', 'houseage', 'housesize', 'unitprice']
    d.T.to_excel('data1.xls')


def save1():
    COUNT = 500
    DELAY = 30

    houseloc = []
    housesize = []
    houseage = []
    unitprice = []
    spider = DataSpider1()
    for i in range(COUNT):  # 爬取、抓取网页前500页的有效信息
        url = 'https://sh.lianjia.com/ershoufang/pg' + '{0:d}/'.format(i + 1)
        raw = spider.GetHtmlText(url)
        loc, size = spider.GetLocSize(raw)
        age = spider.GetAge(raw)
        price = spider.GetPrice(raw)

        houseloc.extend(loc)
        housesize.extend(size)
        houseage.extend(age)
        unitprice.extend(price)

        print('正在获取第{0:d}页数据…………'.format(i + 1))  # 显示运行过程
        if i % 50 == 0 and i > 0:  # 每爬取50页sleep30s防止被识别
            time.sleep(DELAY)
    SaveData1(houseloc, houseage, housesize, unitprice)


if __name__ == '__main__':
    save1()