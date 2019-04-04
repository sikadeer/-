import sqlite3
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans


class Wash(object):
    def __init__(self):
        self.df = None

    def GetDataFromDatabase(self, database):
        conn = sqlite3.connect(database)
        cu = conn.cursor()
        cu.execute('select * from data')
        d = cu.fetchall()
        self.df = pd.DataFrame(d,
                               columns=['unit_price', 'structure', 'storey', 'size', 'age', 'decorate', 'loc', 'xp','yp'])
        return self.df

    def GetDataFromExcel(self, excel):
        self.df=pd.read_excel(excel)

    def GetDataFromDataframe(self,df):
        self.data=df
        return self.data

    def UnitPriceWash(self):
        unit_price = np.array(self.df['unit_price'], dtype=float)
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
        self.df['size'] = size
        return self.df

    def AgeWash(self):
        self.df = self.df.replace(['未知 '], [np.nan])
        self.df['age'] = 2019 - np.array(self.df['age'], dtype=float)
        self.df = self.df.replace([-1], [np.mean(self.df['age'])])
        return self.df

    def DecorateWash(self):
        self.df = self.df.replace(['毛坯     ', '精装     ', None, '简装     ', '其他     '], [0, 2, -1, 1,-1])
        return self.df

    def XYWash(self):
        self.df['xp'] = np.array(self.df['xp'], dtype=float)
        self.df['yp'] = np.array(self.df['yp'], dtype=float)
        self.df = self.df[self.df['xp'] > 120]
        self.df = self.df[self.df['yp'] > 30]
        return self.df

    def Select(self):
        self.df = self.df[self.df['unit_price'].between(10000,120000)]
        self.df = self.df[self.df['age'].between(0,40)]
        self.df = self.df[self.df['size'].between(20, 200)]
        return self.df


    def LogTrans(self,columns):
        self.df['LogTrans'+columns] = np.log(self.df[columns])
        max=np.max(self.df['LogTrans'+columns])
        min=np.min(self.df['LogTrans'+columns])
        self.df['LogTrans'+columns]=(self.df['LogTrans'+columns]-min)/(max-min)
        return self.df
    
    def SqrtTrans(self,columns):
        self.df['SqrtTrans'+columns] = np.sqrt(self.df[columns])
        max=np.max(self.df['SqrtTrans'+columns])
        min=np.min(self.df['SqrtTrans'+columns])
        self.df['SqrtTrans'+columns]=(self.df['SqrtTrans'+columns]-min)/(max-min)
        return self.df
    
    def BoxCoxTrans(self,columns):
        cl,param= stats.boxcox(self.df[columns])
        means=np.mean(cl)
        std = np.std(cl)
        self.df['BoxCoxTrans' + columns] = (cl - means) / std
        return self.df

    def ZscoreNorm(self,columns):
        means = np.mean(self.df[columns])
        std = np.std(self.df[columns])
        self.df['ZscoreNorm'+columns] = (self.df[columns] - means) / std
        max=np.max(self.df['ZscoreNorm'+columns])
        min=np.min(self.df['ZscoreNorm'+columns])
        self.df['ZscoreNorm'+columns]=(self.df['ZscoreNorm'+columns]-min)/(max-min)
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
        self.df['distance']=distance
        return self.df