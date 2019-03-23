import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans

xunlian=pd.read_excel('2_13try.xlsx','train')
ceshi=pd.read_excel('2_13try.xlsx','test')

xl=xunlian.drop('date', axis=1)
xl=xl.dropna()
xl.columns = ['label', 'c1', 'c2', 'c3', 'c4', 'c5']
xl.index = list(range(len(xl.index)))

cs=ceshi.drop('date', axis=1)
cs=cs.dropna()
cs.columns = ['label', 'c1', 'c2', 'c3', 'c4', 'c5']
cs.index = list(range(len(cs.index)))
'''以上是数据清洗部分，请忽略'''



# '''确定训练、测试集'''
# x_train=xl.iloc[:,1:]
# y_train=xl.iloc[:,0]
# x_test=cs.iloc[:,1:]
# y_act =cs.iloc[:,0]
#
#
# '''实行knn分类'''
# knn = KNeighborsClassifier(n_neighbors=5)
# knn.fit(x_train, y_train)
# y_predict = knn.predict(x_test)
# score_c = knn.score(x_train,y_train)
# score_x = knn.score(x_test, y_act)
# print('训练，测试集准确度分别为：{0:.2f};{1:.2f}'.format(score_c,score_x))
# cs['pre_label']=y_predict
# cs.to_excel('try_knn.xls')
#
#
#
# '''以下单纯判断符号'''
# yp=list(np.sign(y_predict))
# ya=list(np.sign(y_act))
# acc=0
# for i,j in zip(yp,ya):
#     if i==j:
#         acc+=1
# print(acc/len(ya))