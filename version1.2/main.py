from class_spider import DataSpider
from class_wash import Wash
from class_paint import Paint
from class_feature_select import FeatureSelect
from class_predict import Predict
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import sqlite3
import time
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


def spider():
    COUNT = 300
    DELAY = 30
    spider = DataSpider()
    for i in range(COUNT):  # 爬取、抓取网页前300页的有效信息
        if i % 20 == 0 and i > 0:  # 每爬取20页sleep30s防止被识别
            time.sleep(DELAY)
        url = r'https://sh.lianjia.com/chengjiao/pg{:d}ng1nb1/'.format(i + 1)
        link = spider.GetLink(url)  # 获取每条信息的地址
        for j in link:
            print('正在获取第{0:d}页第{1:d}条数据…………'.format(i + 1, link.index(j) + 1))
            text = spider.GetHtmlText(j)  # 获取当前页面的源代码
            unit_price = spider.Getunit_price(text)  # 爬取房屋单价
            structure = spider.GetStructure(text)  # 爬取房屋结构
            storey = spider.GetStorey(text)  # 爬取房屋楼层
            size = spider.GetSize(text)  # 爬取房屋面积
            age = spider.GetAge(text)  # 爬取房龄
            decorate = spider.GetDecorate(text)  # 爬取房屋装修情况
            loc = spider.GetLoc(text)  # 爬取房屋地址
            xp, yp = spider.GetXY(loc)  # 爬取房屋经纬度
            data = [unit_price, structure, storey, size, age, decorate, loc, xp, yp]
            spider.SaveData(data)  # 将此条信息存储至数据库中
    conn = spider.conn
    conn.close()

def wash():
    w = Wash()
    w.GetDataFromDatabase('data.db')
    w.UnitPriceWash()
    w.StructureWash()
    w.StoreyWash()
    w.SizeWash()
    w.AgeWash()
    w.DecorateWash()
    w.XYWash()
    raw_df=w.df
    raw_df.drop_duplicates(['unit_price', 'structure', 'storey', 'size'],inplace=True)

    p = Paint()
    p.GetDataFromDataframe(raw_df)
    plt.figure(figsize=(8, 8))
    pc1=p.xyplot()
    plt.savefig('图1：上海二手房价格与地段示意图')
    w.GetDistance(2)
    w.Select()
    df=w.df
    df.to_excel('RawData.xls')

def norm():
    w=Wash()
    w.GetDataFromExcel('RawData.xls')
    for i in ['unit_price','size','age','distance']:
        w.MaxMinNorm(i)
        w.LogNorm(i)
        w.ZscoreNorm(i)
    df=w.df
    p=Paint()
    p.GetDataFromDataframe(df)
    plt.figure(figsize=(8, 8))
    plt.subplot(221)
    pc2=p.histo('unit_price',bins=30,x=75000,y=0.00002)
    plt.subplot(222)
    pc3=p.histo('size',bins=30,x=120,y=0.012)
    plt.subplot(223)
    pc4=p.histo('age',bins=30,x=25,y=0.06)
    plt.subplot(224)
    pc5=p.histo('distance',bins=30,x=55,y=0.08)
    plt.suptitle('Histogram of Raw Data')
    plt.savefig('图2：未归一化的数据直方图')

    plt.figure(figsize=(8, 8))
    plt.subplot(221)
    pc6=p.histo('MaxMinNormunit_price', bins=30, x=0.6, y=2.5)
    plt.subplot(222)
    pc7=p.histo('MaxMinNormsize', bins=30, x=0.6, y=2.5)
    plt.subplot(223)
    pc8=p.histo('MaxMinNormage', bins=30, x=0.6, y=2.5)
    plt.subplot(224)
    pc9=p.histo('MaxMinNormdistance', bins=30, x=0.6, y=8)
    plt.suptitle('Histogram of Max-Min Normalization')
    plt.savefig('图3：max-min归一化的直方图')

    plt.figure(figsize=(8, 8))
    plt.subplot(221)
    pc6=p.histo('LogNormunit_price', bins=30, x=0.65, y=2)
    plt.subplot(222)
    pc7=p.histo('LogNormsize', bins=30, x=0.65, y=2)
    plt.subplot(223)
    pc8=p.histo('LogNormage', bins=30, x=0.65, y=4)
    plt.subplot(224)
    pc9=p.histo('LogNormdistance', bins=30, x=0.65, y=4)
    plt.suptitle('Histogram of Log Normalization')
    plt.savefig('图4：Log归一化的直方图')

    plt.figure(figsize=(8, 8))
    plt.subplot(221)
    pc10=p.histo('ZscoreNormunit_price', bins=30, x=0.65, y=2)
    plt.subplot(222)
    pc11=p.histo('ZscoreNormsize', bins=30, x=0.65, y=2)
    plt.subplot(223)
    pc12=p.histo('ZscoreNormage', bins=30, x=0.65, y=2)
    plt.subplot(224)
    pc13=p.histo('ZscoreNormdistance', bins=30, x=0.65, y=6)
    plt.suptitle('Histogram of Zscore Normalization')
    plt.savefig('图5：ZscoreNorm归一化的直方图')

    df['unit_price']=df['LogNormunit_price']
    df['size']=df['LogNormsize']
    df['age']=df['LogNormage']
    df['distance']=df['LogNormdistance']
    df.drop(['MaxMinNormunit_price', 'LogNormunit_price',
       'ZscoreNormunit_price', 'MaxMinNormsize', 'LogNormsize',
       'ZscoreNormsize', 'MaxMinNormage', 'LogNormage', 'ZscoreNormage',
       'MaxMinNormdistance', 'LogNormdistance', 'ZscoreNormdistance'],axis=1,inplace=True)
    df.to_excel('Washed Data.xls')

def select_feature():
    p=Paint()
    p.GetDataFromExcel('Washed Data.xls')
    p14=p.heat()
    plt.savefig('图6：诸特征之间相关系数热力图')

    p15=p.joint('unit_price','size')
    plt.savefig('图7：房屋单价及面积关系图')
    p16=p.joint('unit_price','age')
    plt.savefig('图8：房屋单价及房龄关系图')
    p17=p.box('decorate','unit_price')
    plt.savefig('图9：房屋单价及装修情况箱型图')
    p18=p.joint('unit_price','distance')
    plt.savefig('图10：房屋单价及距市中心距离关系图')

    sf=FeatureSelect()
    sf. GetDataFromDataframe('Washed Data.xls')
    sf.SelectAge()
    sf.SelectDistance()
    sf.SelectDecorate()
    sf.SelectBedroom_Lavatory()
    data=sf.NewData()
    p.GetDataFromExcel('FinalData.xls')
    p19=p.box('b_l','unit_price')
    plt.savefig('图11：房屋单价及卧室卫生间比率箱型图')
    p20=sf.HeatPlot(data)
    plt.savefig('图12：最终选取特征值之间相关系数热力图')

def predict():
    pr=Predict()
    x=['ridge','ridge','lasso','lasso','linear','linear','SVM','SVM','random','random']
    y=[]
    y+=pr.ridge()
    y+=pr.lasso()
    y+=pr.linear()
    y+=pr.SVM()
    y+=pr.random()
    hue=['train_accuracy','test_accuracy']*5
    data=pd.DataFrame({'algorithm':x,
                       'accuracy':y,
                       'kind':hue})
    p=Paint()
    p.GetDataFromDataframe(data)
    p21=p.bar('algorithm','accuracy','kind')
    plt.savefig('图13：各种回归算法及随机数预测准确率柱状图')

wash()
norm()
select_feature()
predict()

