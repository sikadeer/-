import re
import pandas as pd
import numpy as np
import time
from class_DataSpider1 import DataSpider1
from class_DataSpider1 import save1


class DataSpider2(DataSpider1):  # 继承DataSpider1
    def FindXY(self, text):  # 通过正则表达式抓取经纬度
        x = re.findall(r'"pointx":"?(.*?)"?,', text)
        y = re.findall(r'"pointy":"?(.*?)"?,', text)
        return x, y


def SaveData2(xp, yp):  # 简单处理后分别存储数据的csv和excel文件
    da = pd.DataFrame(np.array([xp, yp], dtype=str))
    da = da.drop('Unnamed: 0', axis=1)
    d = pd.DataFrame(data=da, index=['east_longitude', 'north_latitude']).T
    d.to_csv('data2.csv')
    a = pd.read_csv('data2.csv')
    a.to_excel('data2.xls')


def save2():  # 起个好点的名字
    xp, yp = [], []
    b = pd.read_excel('data1.xls')
    houseloc = ['上海' + x for x in list(b.loc[:, 'houseloc'])]

    sp2 = DataSpider2()
    for i in houseloc:
        # 写成这样三个引号：容易分行
        url = '''https://apis.map.qq.com/jsapi?qt=poi&wd={0:s}&pn=0&rn=10&rich_source=qipao
        &rich=web&nj=0&c=1&key=FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS&output=jsonp&pf=jsapi
        &ref=jsapi&cb=qq.maps._svcb3.search_service_0'''.format(i)
        raw = sp2.GetHtmlText(url)
        x, y = sp2.FindXY(raw)
        if len(x) and len(y):
            xp.append(x[-1])
            yp.append(y[-1])
        else:
            xp.append(np.nan)
            yp.append(np.nan)
        print(r'正在获取{0:s}的数据,已完成{1:d}/{2:d}'.format(i, houseloc.index(i), len(houseloc) - 7500))
        if houseloc.index(i) % 500 == 0 and houseloc.index(i) > 500:
            time.sleep(15)
    SaveData2(xp, yp)


if __name__ == '__main__':
    save1()
    save2()