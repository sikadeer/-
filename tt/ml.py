import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

xl = pd.read_excel('2_13try1.xls', 'train')
cs = pd.read_excel('2_13try1.xls', 'test')

# xl = train_set.drop('date', axis=1)
# xl = xl.dropna()
# xl.columns = ['label', 'c1', 'c2', 'c3', 'c4', 'c5']
# xl.index = list(range(len(xl.index)))
#
# cs = test_set.drop('date', axis=1)
# cs = cs.dropna()
# cs.columns = ['label', 'c1', 'c2', 'c3', 'c4', 'c5']
# cs.index = list(range(len(cs.index)))
# '''以上是数据清洗部分，请忽略'''

'''确定训练、测试集'''
x_train = xl.iloc[:, 1:]
y_train = xl.iloc[:, 0]
x_test = cs.iloc[:, 1:]
y_test = cs.iloc[:, 0]

'''
二维图
'''
pca=PCA(n_components=2)
reduced_x_train=pca.fit_transform(x_train)
reduced_x_test=pca.fit_transform(x_test)

c1=[i[0] for i in reduced_x_train]
c2=[i[1] for i in reduced_x_train]
y=y_train
print(len(c1),len(c2),len(y))
df=pd.DataFrame({'label':y,
    'c1':c1,
    'c2':c2
})
print(df)
rise_high=df[df['label']>2]
rise_low=df[df['label'].between(left=0.5,right=2.5)]
still=df[df['label']==0]
fall_low=df[df['label'].between(left=-2.5,right=-0.5)]
fall_high=df[df['label']<-2]
plt.scatter(x=rise_high['c1'],y=rise_high['c2'],c='r',marker='x')
plt.scatter(x=rise_low['c1'],y=rise_low['c2'],c='y',marker='v')
plt.scatter(x=still['c1'],y=still['c2'],c='g',marker='D')
plt.scatter(x=fall_low['c1'],y=fall_low['c2'],c='b',marker='o')
plt.scatter(x=fall_high['c1'],y=fall_high['c2'],c='black',marker='s')
plt.show()

pca=PCA(n_components=3)
reduced_x_train=pca.fit_transform(x_train)
reduced_x_test=pca.fit_transform(x_test)

c1=[i[0] for i in reduced_x_train]
c2=[i[1] for i in reduced_x_train]
c3=[i[2] for i in reduced_x_train]
y=y_train
print(len(c1),len(c2),len(c3),len(y))
df=pd.DataFrame({'label':y,
    'c1':c1,
    'c2':c2,
    'c3':c3
})
print(df)
rise_high=df[df['label']>2]
rise_low=df[df['label'].between(left=0.5,right=2.5)]
still=df[df['label']==0]
fall_low=df[df['label'].between(left=-2.5,right=-0.5)]
fall_high=df[df['label']<-2]
fig=plt.figure()
ax=Axes3D(fig)
ax.scatter(xs=rise_high['c1'],ys=rise_high['c2'],zs=rise_high['c3'],c='r',marker='x')
ax.scatter(xs=rise_low['c1'],ys=rise_low['c2'],zs=rise_low['c3'],c='y',marker='v')
ax.scatter(xs=still['c1'],ys=still['c2'],zs=still['c3'],c='g',marker='D')
ax.scatter(xs=fall_low['c1'],ys=fall_low['c2'],zs=fall_low['c3'],c='b',marker='o')
ax.scatter(xs=fall_high['c1'],ys=fall_high['c2'],zs=fall_high['c3'],c='black',marker='s')
plt.show()
# '''
# KNN
# '''
#
# knn = KNeighborsClassifier(n_neighbors=5)
# knn.fit(x_train, y_train)
# y_predict = knn.predict(x_test)
# score_c = knn.score(x_train, y_train)
# score_x = knn.score(x_test, y_test)
# print('训练，测试集准确度分别为：{0:.2f};{1:.2f}'.format(score_c, score_x))
# cs['pre_label'] = y_predict
# cs.to_excel('try_knn.xls')
#
# '''以下单纯判断符号'''
# yp = list(np.sign(y_predict))
# ya = list(np.sign(y_test))
# acc = 0
# for i, j in zip(yp, ya):
#     if i == j:
#         acc += 1
# print(acc / len(ya))
#
# """
# Logistic Regression
# """
#
# ### liblinear
# from sklearn.linear_model import LogisticRegression
# from sklearn import metrics
#
# lr = LogisticRegression()
# # all_solvers = ['liblinear', 'newton-cg', 'lbfgs', 'sag', 'saga']
# lr.fit(x_train, y_train)
# train_predict = lr.predict(x_train)
# test_predict = lr.predict(x_test)
#
# train_accuracy = metrics.accuracy_score(train_predict, y_train)
# test_accuracy = metrics.accuracy_score(test_predict, y_test)
#
# print()
# print("With Logistic Regression")
# print('Training accuracy: %0.2f%%' % (train_accuracy * 100))
# print('Testing accuracy: %0.2f%%' % (test_accuracy * 100))
#
# """
# BernoulliNB
# """
# from sklearn.naive_bayes import BernoulliNB
#
# bnb = BernoulliNB()
# bnb.fit(x_train, y_train)
# train_predict = bnb.predict(x_train)
# test_predict = bnb.predict(x_test)
#
# train_accuracy = metrics.accuracy_score(train_predict, y_train)
# test_accuracy = metrics.accuracy_score(test_predict, y_test)
# print()
# print("With BernoulliNB")
# print('Training accuracy: %0.2f%%' % (train_accuracy * 100))
# print('Testing accuracy: %0.2f%%' % (test_accuracy * 100))
#
# """
# LinearSVC
# """
# from sklearn.svm import LinearSVC
#
# lsvc = LinearSVC()
# lsvc.fit(x_train, y_train)
# train_predict = lsvc.predict(x_train)
# test_predict = lsvc.predict(x_test)
#
# train_accuracy = metrics.accuracy_score(train_predict, y_train)
# test_accuracy = metrics.accuracy_score(test_predict, y_test)
#
# print()
# print("With LinearSVC")
# print('Training accuracy: %0.2f%%' % (train_accuracy * 100))
# print('Testing accuracy: %0.2f%%' % (test_accuracy * 100))
