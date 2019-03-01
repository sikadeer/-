import sqlite3
import numpy as np
import pandas as pd


class wash(object):
    def __init__(self):
        self.df = None

    def GetData(self, database):
        conn = sqlite3.connect(database)
        cu = conn.cursor()
        cu.execute('select * from data')
        d = cu.fetchall()
        self.df = pd.DataFrame(d,
                               columns=['unit_price', 'structure', 'storey', 'size', 'age', 'decorate', 'loc', 'xp','yp'])
        self.df.drop_duplicates(['unit_price', 'structure', 'storey', 'size'])
        self.df.to_excel('RawData.xls')
        return self.df

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
        return self.df

    def DecorateWash(self):
        self.df = self.df.replace(list(set(self.df['decorate'])), [0, 1, -1, 2])
        return self.df

    def XYWash(self):
        self.df['xp'] = np.array(self.df['xp'], dtype=float)
        self.df['yp'] = np.array(self.df['yp'], dtype=float)
        return self.df

if __name__ == '__main__':
    w = wash()
    w.GetData('data.db')
    w.UnitPriceWash()
    w.StructureWash()
    w.StoreyWash()
    w.SizeWash()
    w.AgeWash()
    w.DecorateWash()
    w.XYWash()
    dataframe=w.df
    dataframe.to_excel('WashedData.xls')
