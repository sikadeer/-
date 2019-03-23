import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import math

zh=matplotlib.font_manager.FontProperties(fname=r'C:\Windows\Fonts\simkai.ttf')

df=pd.read_excel('data.xls')
df=df[df['housesize']<200]
da=df[['north_latitude','east_longitude']].values
weight=df['unitprice'].values

n_clusters=7
k=KMeans(n_clusters=n_clusters).fit_predict(da,weight)

data=df[['north_latitude','east_longitude','unitprice']]
data['label_k']=k
xc,yc=[],[]
for i in range(n_clusters):
    d=data[data['label']==i]
    xe=sum(d['east_longitude']*d['unitprice'])/sum(d['unitprice'])
    ye=sum(d['north_latitude']*d['unitprice'])/sum(d['unitprice'])
    xc.append(xe)
    yc.append(ye)
x_c=


name=['佘山','南翔','上海南站','上海站','上海交大闵行校区','世纪广场','南汇汽车站']
