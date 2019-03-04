import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
class FeatureSelect(object):
    def __init__(self):
        self.data = pd.read_excel('WashedData.xls')
        self.feature=None
    
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
        return self.data

    def NewData(self):
        self.feature = self.data[['unit_price','distance','age','decorate','b_l']]
        return self.feature

    def HeatPlot(self,data,save=True):
        data = data.corr()
        sns.set(font_scale=0.8)
        plt.subplots(figsize=(8, 8))
        pc=sns.heatmap(data, annot=True, square=True)
        name = 'Heatmap Correlation Coefficient between Each Other'
        plt.suptitle(name)
        if save:
            plt.savefig(name)
        plt.show()

if __name__ == '__main__':
    f=FeatureSelect()
    f.SelectDistance()
    f.SelectAge()
    f.SelectDecorate()
    f.SelectBedroom_Lavatory()
    data=f.NewData()
    f.HeatPlot(data)

        
    


# data.drop(['xp', 'yp'], axis=1,inplace=True)




# d1=data[data['distance']<0.017]
# d2=data[data['distance'].between(0.017,0.069)]
# d3=data[data['distance'].between(0.069,0.180)]
# d4=data[data['distance']>0.180]
# for i in [d1,d2,d3,d4]:
#     p = np.corrcoef(list(i.loc[:, 'unit_price']), i.loc[:, 'kitchen_num'])
#     print(p)