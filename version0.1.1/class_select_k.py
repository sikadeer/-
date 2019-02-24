import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import math

class Select_k(object):#采用elbow method确定分类的合适簇数
    def __init__(self):
        self.df=pd.read_excel('data.xls')
        self.da=self.df[['north_latitude', 'east_longitude']].values
        self.weight=self.df['unitprice'].values
    def calculate(self,floor=2,ceil=25):
        distance = []
        for k in range(floor,ceil):#进行kmeans聚类将数据分类为2-25簇
            s=[]
            kmeans=KMeans(n_clusters=k).fit_predict(self.da, self.weight)#对计入房屋单价为权重的地区分类
            data=self.df[['north_latitude', 'east_longitude', 'unitprice']]
            data['label']=kmeans
            for i in range(k):#分别计算各簇样本点距其质心的距离进行加和
                d=data[data['label']==i]
                xe=sum(d['east_longitude']*d['unitprice'])/sum(d['unitprice'])
                ye=sum(d['north_latitude']*d['unitprice'])/sum(d['unitprice'])
                delta_x=d['east_longitude']-xe
                delta_y=d['north_latitude']-ye
                dis=np.array([math.hypot(x,y) for x,y in zip(delta_x,delta_y)])*d['unitprice']
                s.append(dis.sum())
            distance.append(sum(s)/k)
        return distance
    def paint(self,distance):#绘制2-25簇下损失值的折线图
        sns.set_style('darkgrid')
        plt.plot(list(range(2, 25)), distance)
        plt.plot(list(range(2, 25)), distance, 'bo')
        plt.plot()
        plt.xticks(np.arange(0, 25, 1))
        plt.xlabel('k')
        plt.ylabel('Distortion')
        plt.title('The Elbow Method showing the optimal k')
        plt.savefig('The Elbow Method showing the optimal k.jpg', format='jpg')
        plt.show()
if __name__ == '__main__':
    sk=Select_k()
    dis=sk.calculate()
    sk.paint(dis)

