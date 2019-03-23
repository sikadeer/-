import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time

houseloc,housesize,houseage,unitprice=([] for i in range(4))
for i in range(500):
    url=r'https://sh.lianjia.com/ershoufang/pg'+'{0:s}/'.format(str(i+1))
    head={'User-Agent':'Mozilla/5.0'}
    req = requests.get(url,headers=head)
    req.encoding = req.apparent_encoding
    text = req.text
    text = BeautifulSoup(text, "html.parser")
    div1=text.find_all(name='div',attrs={'class':'houseInfo'})
    houseloc.extend([re.findall(r'target="_blank">(.*?)</a>',str(x))[0] for x in div1])
    houseinfo=[re.findall(r'厅|(\d\d.*?)平',str(x))[0] for x in div1]
    housesize.extend([x.split('|')[-1] for x in houseinfo])
    div2=text.find_all(name='div',attrs={'class':'positionInfo'})
    houseage.extend([re.findall(r'(\d+?)年',str(x))[0] if re.findall(r'(\d+?)年',str(x))!=[] else np.nan for x in div2])
    div3=text.find_all(name='div',attrs={'class':'unitPrice'})
    unitprice.extend([re.findall(r'data-price="(\d+?)"',str(x))[0] for x in div3])
    print('正在获取第{0:d}页数据…………'.format(i+1))

    if i%50==0 and i>0:
        time.sleep(30)

houseloc=np.array(houseloc,dtype=str)
houseage=2019.-np.array(houseage,dtype=float)
housesize=np.array(housesize,dtype=str)
unitprice=np.array(unitprice,dtype=str)
datafram=pd.DataFrame(np.array([houseloc,houseage,housesize,unitprice]))
datafram.to_csv('data1.csv')
d=pd.read_csv('data1.csv')
d.drop('Unnamed: 0',axis=1)
d.index=['houseloc','houseage','housesize','unitprice']
d.T.to_excel('data1.xls')
