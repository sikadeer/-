import requests
import re
import pandas as pd
import numpy as np
import time

xp,yp=[],[]
b=pd.read_excel('data1.xls')
houseloc=['上海'+x for x in list(b.loc[:,'houseloc'])]
for i in houseloc:
    url=r'https://apis.map.qq.com/jsapi?qt=poi&wd={0:s}&pn=0&rn=10&rich_source=qipao&rich=web&nj=0&c=1&key=FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS&output=jsonp&pf=jsapi&ref=jsapi&cb=qq.maps._svcb3.search_service_0'.format(i)
    head={'User-Agent':'Mozilla/5.0'}
    n=requests.get(url,headers=head)
    n.encoding=n.apparent_encoding
    text = n.text
    x=re.findall(r'"pointx": "?(.*?)"?,',text)
    y=re.findall(r'"pointy": "?(.*?)"?,',text)
    if len(x)*len(y)>0:
        xp.append(x[-1])
        yp.append(y[-1])
    else:
        xp.append(np.nan)
        yp.append(np.nan)
    print(r'正在获取{0:s}的数据,已完成{1:d}/{2:d}'.format(i,houseloc.index(i),len(houseloc)-7500))
    if houseloc.index(i)%500==0 and houseloc.index(i)>500:
        time.sleep(15)

da=pd.DataFrame(np.array([xp,yp],dtype=str))
da=da.drop('Unnamed: 0',axis=1)
d=pd.DataFrame(data=da,index=['east_longitude','north_latitude']).T
d.to_csv('data2.csv')
a=pd.read_csv('data2.csv')
a.to_excel('data2.xls')
