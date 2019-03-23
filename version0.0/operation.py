import pandas as pd
import numpy as np
import math
class Operation(object):#合并两个爬虫得到的数据
    def combine(self):
        d1=pd.read_excel('data1.xls')
        d2=pd.read_excel('data2.xls')
        d1['north_latitude']=d2['north_latitude']
        d1['east_longitude']=d2['east_longitude']
        return d1

    def wash(self,d1):#清洗数据中的异常
        for i in d1.index:
            if len(list(d1.at[i,'housesize']))>7 \
                    or abs(d1.at[i,'north_latitude']-31)>2 \
                    or abs(d1.at[i,'east_longitude']-121)>2:
                d1=d1.drop(i)
                #(1)删除房屋面积数据中出现的乱码
                #(2),(3)删除位置明显偏离上海的数据

        d1['houseage']=np.array(d1['houseage'],dtype=float)
        ct_lat=31.230498437532088
        ct_long=121.47431154365539
        #计算距离时假定市中心位于人民广场，即上海市政府的位置
        dx=d1['north_latitude']-ct_lat
        dy=d1['east_longitude']-ct_long
        distance=[math.hypot(96*x,57*y) for x,y in zip(dx,dy)]
        d1['distance']=distance#通过经纬度与实际距离的换算计算各地距离市中心的距离
        d1=d1.drop_duplicates(['houseage','housesize','unitprice'])#删除由于发布时间不同而重复发布的房源信息
        d1=d1.dropna()#删除空缺值
        d1=d1.sort_values(by='unitprice',ascending=True)#将数据按照房屋单价升序排列
        d1.index=list(range(len(d1.index)))#重置dataframe的行索引
        return d1
    def SaveData3(self,d1):#分别存储数据的csv和excel文件
        d1.to_csv('data.csv')
        a=pd.read_csv('data.csv')
        a.to_excel('data.xls')

def Operate():
    o=Operation()
    d1=o.combine()
    d1=o.wash(d1)
    o.SaveData3(d1)