import sqlite3
import math
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


class Wash(object):
    def __init__(self):
        self.df = None

    def GetData(self, database):
        conn = sqlite3.connect(database)
        cu = conn.cursor()
        cu.execute('select * from data')
        d = cu.fetchall()
        self.df = pd.DataFrame(d,
                               columns=['unit_price', 'structure', 'storey', 'size', 'age', 'decorate', 'loc', 'xp','yp'])
        self.df.to_excel('RawData.xls')
        return self.df

    def UnitPriceWash(self):
        unit_price = np.array(self.df['unit_price'], dtype=float)
        # means=np.mean(unit_price)
        # var=np.var(unit_price)
        # unit_price=(unit_price-means)/var
        self.df['unit_price'] = unit_price
        return self.df

    def StructureWash(self):
        structure = self.df['structure']
        bedroom_num = []
        living_num = []
        kitchen_num = []
        lavatory_num = []
        for i, j in enumerate(structure):
            try:
                bedroom = int(list(j)[0])
                bedroom_num.append(bedroom)
                livingroom = int(list(j)[2])
                living_num.append(livingroom)
                kitchen = int(list(j)[4])
                kitchen_num.append(kitchen)
                lavatory = int(list(j)[6])
                lavatory_num.append(lavatory)
            except:
                self.df = self.df.drop(index=i)
        self.df['bedroom_num'] = bedroom_num
        self.df['livingroom_num'] = living_num
        self.df['kitchen_num'] = kitchen_num
        self.df['lavatory_num'] = lavatory_num
        return self.df

    def StoreyWash(self):
        self.df = self.df.replace(['高', '中', '低'], [2, 1, 0])
        return self.df

    def SizeWash(self):
        size = np.array(self.df['size'], dtype=float)
        # mean=np.mean(size)
        # var=np.var(size)
        # size=(size-mean)/var
        self.df['size'] = size
        return self.df

    def AgeWash(self):
        self.df = self.df.replace(['未知 '], [np.nan])
        self.df['age'] = 2019 - np.array(self.df['age'], dtype=float)
        self.df = self.df.replace([-1], [np.mean(self.df['age'])])
        # means=np.mean(self.df['age'])
        # var=np.var(self.df['age'])
        # self.df['age']=(self.df['age']-means)/var
        return self.df

    def DecorateWash(self):
        self.df = self.df.replace(['毛坯     ', '精装     ', None, '简装     ', '其他     '], [0, 2, -1, 1,-1])
        return self.df

    def XYWash(self):
        self.df['xp'] = np.array(self.df['xp'], dtype=float)
        self.df['yp'] = np.array(self.df['yp'], dtype=float)
        return self.df

    def Select(self):
        self.df = self.df[self.df['unit_price'].between(10000,110000)]
        self.df = self.df[self.df['age'].between(0,40)]
        self.df = self.df[self.df['size'] < 200]
        self.df = self.df[self.df['xp'] > 120]
        self.df = self.df[self.df['yp'] > 30]

        return self.df

    def Norm(self,columns):
        means=np.mean(self.df[columns])
        var=np.var(self.df[columns])
        self.df[columns]=(self.df[columns]-means)/var
        max=np.max(self.df[columns])
        min=np.min(self.df[columns])
        self.df[columns]=(self.df[columns]-min)/(max-min)
        return self.df

    def GetDistance(self,n):
        data = self.df[['xp', 'yp', 'unit_price']]
        k = KMeans(n_clusters=n).fit_predict(data[['xp', 'yp']], data['unit_price'])
        data['label'] = k
        xc, yc = [], []
        for i in range(n):
            d = data[data['label'] == i]
            xe = sum(d['xp'] * d['unit_price']) / sum(d['unit_price'])
            ye = sum(d['yp'] * d['unit_price']) / sum(d['unit_price'])
            xc.append(xe)
            yc.append(ye)
        distance=np.zeros_like(data['xp'])
        for x, y in zip(xc, yc):
            dx = np.array(data['xp'] - x,dtype=float)
            dy = np.array(data['yp'] - y,dtype=float)
            distance+=np.hypot(96*dx,57*dy)
        print(distance)
        self.df['distance']=distance
        return self.df


if __name__ == '__main__':
    w = Wash()
    w.GetData('data.db')
    w.UnitPriceWash()
    w.StructureWash()
    w.StoreyWash()
    w.SizeWash()
    w.AgeWash()
    w.DecorateWash()
    w.XYWash()
    w.Select()
    for i in ['age','unit_price','size']:
        w.Norm(i)
    w.GetDistance(2)
    w.Norm('distance')
    dataframe=w.df
    dataframe=dataframe.drop_duplicates(['unit_price', 'structure', 'storey', 'size'])
    dataframe.to_excel('WashedData.xls')
