import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


class Paint(object):
    def __init__(self):
        self.data = None
        self.zh = matplotlib.font_manager.FontProperties(fname=r'./simkai.ttf')

    def GetDataFromExcel(self, filename):
        self.data = pd.read_excel(filename)
        return self.data

    def GetDataFromDataframe(self, df):
        self.data = df
        return self.data

    def joint(self, x, y):  # 绘制两个变量的关系图
        sns.set(style="darkgrid")
        p = np.corrcoef(list(self.data.loc[:, x]), self.data.loc[:, y])
        pc = sns.jointplot(x=x, y=y, data=self.data.loc[:, [x, y]], kind='reg', color='g')
        name = 'joint relation between {0:s} and {1:s}'.format(y.capitalize(), x.capitalize())
        plt.suptitle(name)
        plt.text(0, 1.1, 'correlation coefficient={0:.3f}'.format(p[0][-1]))
        return pc

    def histo(self, s, x, y, bins=20):  # 绘制单个变量的直方图
        df = self.data[s]
        skewnes, sk = stats.skewtest(df)
        kurtosis, ku = stats.kurtosistest(df)
        sns.set(style="darkgrid")
        pc = sns.distplot(df, kde=True, bins=bins)
        plt.text(x=x, y=y, s='skewnes=%.2f\nkurtosis=%.2f' % (skewnes, kurtosis))
        name = 'the Histograme of {:s}'.format(s.capitalize())
        plt.suptitle(name)
        return pc

    def box(self, x, y):  # 绘制单个变量的箱型图
        sns.set(font=self.zh.get_name())
        plt.figure(figsize=(8, 8))
        data = self.data[[x, y]]
        pc = sns.boxplot(x=x, y=y, hue=x, data=data)
        name = 'Boxplot of {0:s} and {1:s}'.format(y.capitalize(), x.capitalize())
        plt.suptitle(name)
        return pc

    def heat(self):  # 绘制热力图
        data = self.data.drop(['xp', 'yp'], axis=1)
        data = data.corr()
        sns.set(font_scale=1)
        plt.subplots(figsize=(10, 10))
        pc = sns.heatmap(data, annot=True, square=True)
        name = 'Heatmap of Correlation Coefficient between Each Other'
        plt.suptitle(name)
        return pc

    def xyplot(self):  # 绘制散点图
        plt.figure(figsize=(8, 8))
        sns.set(font=self.zh.get_name(), font_scale=0.8)
        pc = sns.scatterplot(x=self.data['xp'], y=self.data['yp'], \
                             hue=self.data['unit_price'], s=70, palette="hot")
        referance = {'南京西路': [121.457901, 31.23881328496342],
                     '陆家嘴': [121.50218, 31.238310402283478],
                     '世纪广场': [121.54183906745911, 31.225971889682427],
                     '徐家汇': [121.44076999999997, 31.193350664073645],
                     '五角场': [121.52983205165101, 31.25512357635329],
                     '虹桥': [121.33760000000002, 31.19759773404437],
                     '莘庄': [121.37894999999999, 31.106021171603967],
                     '宝山': [121.48941, 31.40581942393495],
                     '奉贤': [121.47409999999999, 30.918582256612243],
                     '嘉定': [121.33154861160276, 31.353433401508816],
                     '佘山': [121.18755000000002, 31.103561185882107],
                     '滴水湖': [121.94091999999999, 30.898330624249144],
                     '金山': [121.34242000000003, 30.74240327105306]
                     }
        for i, j in zip(referance.keys(), referance.values()):
            plt.scatter(x=j[0], y=j[1], c='g', marker='x')
            plt.text(x=j[0], y=j[1], s=str(i))
        name = '上海二手房价格与地段示意图'
        plt.suptitle(name)
        return pc

    def bar(self, x, y, hue):  # 绘制柱状图
        sns.set_style('whitegrid')
        pc = sns.barplot(x=x, y=y, hue=hue, data=self.data)
        plt.title('the Accuracy of Different Algorithm ')
        return pc