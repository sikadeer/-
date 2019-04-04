import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge,Lasso,LinearRegression
from sklearn import svm


class Predict(object):
    def __init__(self):
        self.df = pd.read_excel('FinalData.xls')
        self.data = self.df.iloc[:, 1:]
        self.target = self.df.iloc[:, 0]

    def ridge(self):
        '''Ridge Regression'''
        train_accuracy, test_accuracy = 0, 0
        for i in range(10):#运用十折交叉运算平均计算其准确率，下亦同。
            x_train, x_test = train_test_split(
                self.data, test_size=0.9, random_state=i)
            y_train, y_test = train_test_split(
                self.target, test_size=0.9, random_state=i)
            clf = Ridge(alpha=1)
            clf.fit(x_train, y_train)
            train_predict = clf.predict(x_train)
            test_predict = clf.predict(x_test)
            delta_train = abs(np.array(y_train) - np.array(train_predict)) / np.array(y_train)
            train_accuracy+= len(delta_train[delta_train < 0.10]) / len(delta_train)
            delta_test = abs(np.array(y_test) - np.array(test_predict)) / np.array(y_test)
            test_accuracy+= len(delta_test[delta_test < 0.10]) / len(delta_test)#预测值与真实值误差小于10%判定为相对准确。
        return train_accuracy / 10 * 100,test_accuracy / 10 * 100

    def lasso(self):
        '''Lasso'''
        train_accuracy, test_accuracy = 0, 0
        for i in range(10):
            x_train, x_test, y_train, y_test = train_test_split(
                self.data, self.target, test_size=0.9, random_state=i)
            clf = Lasso(alpha=0.01)
            clf.fit(x_train, y_train)
            train_predict = clf.predict(x_train)
            test_predict = clf.predict(x_test)
            delta_train = abs(np.array(y_train) - np.array(train_predict)) / np.array(y_train)
            train_accuracy+= len(delta_train[delta_train < 0.10]) / len(delta_train)
            delta_test = abs(np.array(y_test) - np.array(test_predict)) / np.array(y_test)
            test_accuracy+= len(delta_test[delta_test < 0.10]) / len(delta_test)

        return train_accuracy / 10 * 100, test_accuracy / 10 * 100

    def linear(self):
        '''Linear Regression'''
        train_accuracy, test_accuracy = 0, 0
        for i in range(10):
            x_train, x_test, y_train, y_test = train_test_split(
                self.data, self.target, test_size=0.9, random_state=i)
            clf = LinearRegression()
            clf.fit(x_train, y_train)
            train_predict = clf.predict(x_train)
            test_predict = clf.predict(x_test)
            delta_train = abs(np.array(y_train) - np.array(train_predict)) / np.array(y_train)
            train_accuracy+= len(delta_train[delta_train < 0.10]) / len(delta_train)
            delta_test = abs(np.array(y_test) - np.array(test_predict)) / np.array(y_test)
            test_accuracy+= len(delta_test[delta_test < 0.10]) / len(delta_test)
        return train_accuracy / 10 * 100, test_accuracy / 10 * 100

    def SVM(self):
        '''SVM'''
        train_accuracy, test_accuracy = 0, 0
        for i in range(10):
            x_train, x_test, y_train, y_test = train_test_split(
                self.data, self.target, test_size=0.9, random_state=i)
            clf = svm.SVR()
            clf.fit(x_train, y_train)
            train_predict = clf.predict(x_train)
            test_predict = clf.predict(x_test)
            delta_train = abs(np.array(y_train) - np.array(train_predict)) / np.array(y_train)
            train_accuracy+= len(delta_train[delta_train < 0.10]) / len(delta_train)
            delta_test = abs(np.array(y_test) - np.array(test_predict)) / np.array(y_test)
            test_accuracy+= len(delta_test[delta_test < 0.10]) / len(delta_test)
        return train_accuracy / 10 * 100, test_accuracy / 10 * 100


    def random(self):
        random_data=np.random.rand(*self.data.shape)
        random_target=np.random.rand(*self.target.shape)
        train_accuracy, test_accuracy = 0, 0
        for i in range(10):
            x_train, x_test = train_test_split(
                random_data, test_size=0.9, random_state=i)
            y_train, y_test = train_test_split(
                random_target, test_size=0.9, random_state=i)
            clf = Ridge(alpha=1)
            clf.fit(x_train, y_train)
            train_predict = clf.predict(x_train)
            test_predict = clf.predict(x_test)
            delta_train = abs(np.array(y_train) - np.array(train_predict)) / np.array(y_train)
            train_accuracy += len(delta_train[delta_train < 0.10]) / len(delta_train)
            delta_test = abs(np.array(y_test) - np.array(test_predict)) / np.array(y_test)
            test_accuracy += len(delta_test[delta_test < 0.10]) / len(delta_test)
        return train_accuracy / 10 * 100, test_accuracy / 10 * 100