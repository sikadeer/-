import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

class WholePainting(object):
    def __init__(self):
        self.da=pd.read_excel('data.xls').drop(['Unnamed: 0','houseloc','north_latitude','east_longitude'],axis=1)
    def pairplot(self):#绘制四个变量的矩阵图
        sns.set_style('darkgrid')
        pc=sns.pairplot(np.exp(self.da),diag_kind='kde',plot_kws={'alpha':0.05},dropna=True)
        plt.suptitle('joint plot of the houseage,the housesize,the unitprice and the distance from the downtown')
        return pc
    def HistoWhole(self):#绘制四个变量的直方图
        for x,y in enumerate(['houseage','housesize','unitprice','distance']):
            plt.subplot('22{:d}'.format(x))
            df=self.da[y]
            sns.set_style('darkgrid')
            sns.distplot(df,bins=30)
        plt.suptitle('the histograme of houseage,housesize,unitprice and distance')
        plt.savefig('histo.jpg')
        plt.show()
    def histo(self,s,f=np.inf,bins=10,axlabel=None,log=True):#绘制单个变量的直方图
        df = self.da[self.da[s] < f]
        if log:
            pc=sns.distplot(df[s], bins=bins,fit=norm,kde=False,axlabel=axlabel)
        else:
            pc=sns.distplot(np.exp(df[s]),bins=bins,axlabel=axlabel)
        plt.suptitle('the histograme of {:s}'.format(s))
        return pc
    def joint(self,s1,s2,x,y,lim1=np.Infinity,lim2=np.Infinity,log=True):#绘制两个变量之间的散点图
        d=self.da[[s1,s2]]
        d1=d[d[s1]<lim1]
        d2=d1[d1[s2]<lim2]
        if log:
            pass
        elif not log:
            d2[s2]=np.exp(d2[s2])
        sns.set(style="darkgrid")
        p=np.corrcoef(list(d2.iloc[:,0]),list(d2.iloc[:,1]))
        pc=sns.jointplot(x=s1, y=s2, data=d2, kind='reg',color='g')
        plt.suptitle('joint relation between {0:s} and {1:s}'.format(s1,s2))
        plt.text(x,y,'correlation coefficient={0:.3f}'.format(p[0][-1]))
        return pc



