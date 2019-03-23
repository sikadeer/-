import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from class_operation import Operation
from class_operation import Operate

class Paint(Operation):
    def whole(self):
        df=da.drop(['Unnamed: 0','houseloc','north_latitude','east_longitude'],axis=1)
        sns.set_style('darkgrid')
        sns.pairplot(df,diag_kind='kde',plot_kws={'alpha':0.05},dropna=True)#绘制四个参量的矩阵图
        plt.suptitle('joint plot of the houseage,the housesize,the unitprice and the distance from the downtown')
        plt.savefig('pairplot.jpg')
        plt.show()
    def histo(self):
        def h_p(s,f=np.inf):
            df=da[s]
            df=df[df<f]
            sns.set_style('darkgrid')
            sns.distplot(df,bins=30)
        plt.tight_layout()
        plt.subplot(221)
        h_p('houseage')
        plt.subplot(222)
        h_p('housesize')
        plt.subplot(223)
        h_p('unitprice')
        plt.subplot(224)
        h_p('distance')
        plt.suptitle('the histograme of houseage,housesize,unitprice and distance')
        plt.savefig('histo.jpg')
        plt.show()
    def joint(self,s1,s2,x,y,lim1=np.Infinity,lim2=np.Infinity):
        d=da[[s1,s2]]
        d=d[d[s1]<lim1]
        d=d[d[s2]<lim2]
        sns.set(style="darkgrid")
        p=np.corrcoef(list(d.iloc[:,0]),list(d.iloc[:,1]))
        sns.jointplot(x=s1, y=s2, data=d, kind='reg')
        plt.suptitle('joint relation between {0:s} and {1:s}'.format(s1,s2))
        plt.text(x,y,'correlation coefficient={0:.3f}'.format(p[0][-1]))
        plt.savefig('jointplot of {0:s} and {1:s}.jpg'.format(s2,s1),format='jpg')
        plt.show()


da=pd.read_excel('data.xls')
if __name__ == '__main__':
    Operate()
    pa=Paint()
    pa.whole()
    pa.histo()
    pa.joint('houseage','unitprice',lim1=40,x=20,y=200000)
    pa.joint('housesize','unitprice',lim1=305,x=100,y=200000)
    pa.joint('distance','unitprice',x=20,y=180000)
