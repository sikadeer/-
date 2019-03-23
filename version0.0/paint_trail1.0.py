import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import math

a=[]
df=pd.read_excel('data.xls')
da=df[['north_latitude','east_longitude']].values
weight=df['unitprice'].values
for x in range(2,21):
    sr,sv =[],[]
    n_clusters =x
    k=KMeans(n_clusters =n_clusters ).fit_predict(da,weight)
    data=df[['north_latitude','east_longitude','unitprice']]
    data['label']=k
    sns.set_style('whitegrid')
    sns.relplot(x='east_longitude',y='north_latitude',hue=k,size='unitprice',data=data,sizes=(1,200))
    xc,yc=[],[]
    print('下'+str(x)*3)
    for i in range(n_clusters):
        d=data[data['label']==i]
        xe=sum(d['east_longitude']*d['unitprice'])/sum(d['unitprice'])
        ye=sum(d['north_latitude']*d['unitprice'])/sum(d['unitprice'])
        xc.append(xe)
        yc.append(ye)
        print(np.array([yc,xc]).T)
        plt.scatter(xc,yc,c='r',marker='x')
        delta_x=d['east_longitude']-xc[i]
        delta_y=d['north_latitude']-yc[i]
        d_r=np.array([math.hypot(96*x,57*y) for x,y in zip(delta_x,delta_y)])
        d_v=np.array([math.hypot(x,y) for x,y in zip(delta_x,delta_y)])*data[data['label']==i]['unitprice']
        print(np.corrcoef(d_r,data[data['label']==i]['unitprice'])[0][-1])
        print('上'+str(i)*3)
        sr=sr+list(d_r)
        sv=sv+list(d_v)
    a.append((sum(sv)))
plt.plot(list(range(2,21)),a)
plt.show()