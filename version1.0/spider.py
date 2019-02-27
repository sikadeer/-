import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time

link=[]
url1=r'https://sh.lianjia.com/chengjiao/'
head = {'User-Agent': 'Mozilla/5.0'}
req = requests.get(url1, headers=head)
req.encoding = req.apparent_encoding
text1= req.text
text1= BeautifulSoup(text1, "html.parser")
div1=text1.find_all(name='a',attrs={'class':'img'})
link.extend([re.findall(r'href="(.*?)"',str(x))[0] for x in div1])

unitprice,structure,storey,size,age,decorate,loc=([] for i in range(7))
for url2 in link:
    reqq= requests.get(url2, headers=head)
    reqq.encoding = reqq.apparent_encoding
    text2= reqq.text
    unitprice.append(re.findall(r'<b>(\d+?)</b>',text2)[0] if re.findall(r'<b>(\d+?)</b>',text2) else np.nan)
    structure.append(re.findall(r'房屋户型</span>(.*?)</li>',text2)[0] if re.findall(r'房屋户型</span>(.*?)</li>',text2) else np.nan)
    storey.append(re.findall(r'所在楼层</span>(.*?)楼层',text2)[0] if re.findall(r'所在楼层</span>(.*?)楼层',text2) else np.nan)
    size.append(re.findall(r'建筑面积</span>(.*?)㎡',text2)[0] if re.findall(r'建筑面积</span>(.*?)㎡',text2) else np.nan)
    age.append(re.findall(r'建成年代</span>(.*?)</li>',text2)[0] if re.findall(r'建成年代</span>(.*?)</li>',text2) else np.nan)
    decorate.append(re.findall(r'装修情况</span>(.*?)</li>',text2)[0] if re.findall(r'装修情况</span>(.*?)</li>',text2) else np.nan)
    loc.append(re.findall(r'<div class="wrapper">(.*?)\d',text2)[0] if re.findall(r'<div class="wrapper">(.*?)\d',text2) else np.nan)
print(unitprice,structure,storey,size,age,decorate,loc)