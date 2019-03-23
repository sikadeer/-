import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

da=pd.read_excel('data.xls')
def whole():
    df=da.drop(['Unnamed: 0','houseloc','north_latitude','east_longitude'],axis=1)
    sns.set_style('darkgrid')
    sns.pairplot(df,diag_kind='kde',plot_kws={'alpha':0.05},dropna=True)#绘制四个参量的矩阵图
    plt.suptitle('joint plot of the houseage,the housesize,the unitprice and the distance from the downtown')
    plt.savefig('pairplot.jpg')
    plt.show()
def histo():
    def h_p(s,f=np.inf):
        df=da[s]
        df=df[df<f]
        df=np.log(df)
        sns.distplot(df,bins=30)
    plt.tight_layout()
    sns.set_style('darkgrid')
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

def u_a():
    d=da[['houseage','unitprice']]
    d['houseage'] = np.log(d['houseage'])
    d['unitprice'] = np.log(d['unitprice'])
    sns.set(style="darkgrid")
    p=np.corrcoef(list(d.iloc[:,0]),list(d.iloc[:,1]))
    sns.jointplot(x='houseage', y=r'unitprice', data=d, kind='reg')
    plt.suptitle('joint relation between unitprice and houseage')
    plt.text(3,12.5, 'correlation coefficient={0:.3f}'.format(p[0][-1]))
    plt.savefig('jointplot of unitprice and age.jpg',format='jpg')
    plt.show()
def u_s():
    d=da[['housesize', 'unitprice']]
    d['unitprice']=np.log(d['unitprice'])
    d['housesize']=np.log(d['housesize'])
    sns.set(style="darkgrid")
    p=np.corrcoef(list(d.iloc[:, 0]), list(d.iloc[:, 1]))
    sns.jointplot(x='housesize', y='unitprice', data=d, kind='reg')
    plt.suptitle('joint relation between unitprice and housesize')
    plt.text(4.5, 12.3, 'correlation coefficient={0:.3f}'.format(p[0][-1]))
    plt.savefig('jointplot of unitprice and size.jpg', format='jpg')
    plt.show()
def u_d():
    d=da[['distance', 'unitprice']]
    d['distance']=np.log(d['distance'])
    d['unitprice']=np.log(d['unitprice'])
    sns.set(style="darkgrid")
    p=np.corrcoef(list(d.iloc[:, 0]), list(d.iloc[:, 1]))
    sns.jointplot(x='distance', y='unitprice', data=d, kind='reg')
    plt.suptitle('joint relation between unitprice and distance')
    plt.text(0,12, 'correlation coefficient={0:.3f}'.format(p[0][-1]))
    plt.savefig('jointplot of unitprice and distance.jpg', format='jpg')
    plt.show()
u_s()