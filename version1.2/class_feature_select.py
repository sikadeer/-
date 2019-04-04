import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class FeatureSelect(object):
    def __init__(self):
        self.feature=None
        self.data=None

    def GetDataFromDataframe(self,filename):
        self.data=pd.read_excel(filename)
        return self.data
    
    def SelectDistance(self):
        return self.data
    
    def SelectAge(self):
        return self.data
    
    def SelectDecorate(self):
        self.data = self.data[self.data['decorate'] != -1]
        return self.data
    
    def SelectBedroom_Lavatory(self):
        self.data = self.data[self.data['lavatory_num']<3]
        self.data['b_l'] = (self.data['bedroom_num'] - self.data['lavatory_num']) / (self.data['bedroom_num'])
        self.data['b_l']=np.around(self.data['b_l'], decimals=2)
        return self.data

    def NewData(self,data):
        self.feature = data[['unit_price','distance','age','decorate','b_l']]
        self.feature.to_excel('FinalData.xls')
        return self.feature

    def HeatPlot(self,data,save=False):
        data = data.corr()
        sns.set(font_scale=0.8)
        plt.subplots(figsize=(8, 8))
        pc=sns.heatmap(data, annot=True, square=True)
        name = 'Heatmap Correlation Coefficient between Each Other'
        plt.suptitle(name)
        if save:
            plt.savefig(name)
        return pc