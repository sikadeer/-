import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import math



zh=matplotlib.font_manager.FontProperties(fname=r'C:\Windows\Fonts\simkai.ttf')

df=pd.read_excel('data.xls')


loc=df[['north_latitude','east_longitude']].values
weight=df['unitprice'].values
n_clusters=6
k=KMeans(n_clusters=n_clusters).fit_predict(loc,weight)

data=df[['north_latitude','east_longitude','unitprice']]
name=['佘山','南翔','上海南站','上海站','上海交大闵行校区','世纪广场']
data['label']=k

xc,yc=[],[]
for i in range(n_clusters):
    d=data[data['label']==i]
    xe = sum(d['east_longitude'] * d['unitprice']) / sum(d['unitprice'])
    ye = sum(d['north_latitude'] * d['unitprice']) / sum(d['unitprice'])
    xc.append(xe)
    yc.append(ye)
print(np.array([yc,xc]).T)
ct=[xc[i] for i in k]
data['x_c']=ct
data=data.sort_values(by='x_c',ascending=True)
label=[sorted(xc).index(i) for i in list(data['x_c'])]
data['label']=label
centre=[name[i] for i in label]
data['centre']=centre
sns.set_style('darkgrid')
zh=matplotlib.font_manager.FontProperties(fname=r'C:\Windows\Fonts\simkai.ttf')
sns.set(font=zh.get_name())
sns.relplot(x='east_longitude',y='north_latitude',hue='centre',size='unitprice',data=data,sizes=(1,200))
plt.scatter(xc, yc, c='black', marker='x')
plt.title('7 clusters divided by k-means')
plt.savefig('7 clusters divided by k-means.jpg',format='jpg')
plt.show()
#
# d=np.zeros_like(k,dtype=float)
# for x,y in zip(xc,yc):
#     delta_x=data['east_longitude']-x
#     delta_y=data['north_latitude']-y
#     d_r=np.array([math.hypot(96*x1,57*y1) for x1,y1 in zip(delta_x,delta_y)])/n_clusters
#     d+=d_r
# print(np.array([yc,xc]).T)
# print(np.corrcoef(data['unitprice'],d))