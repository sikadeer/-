import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn import mixture
xl=pd.read_excel('2_13try1.xls','train')
cs=pd.read_excel('2_13try1.xls','test')
x_train=xl.iloc[:,1:]
y_train=xl.iloc[:,0]
x_test=cs.iloc[:,1:]
y_act =cs.iloc[:,0]
g = mixture.GMM(n_components=5)
