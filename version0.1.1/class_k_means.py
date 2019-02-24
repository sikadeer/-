import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from class_select_k import Select_k

class K_means(Select_k):#由select_k部分所显示的折线图得出：k=7较为合适
    def __init__(self,n_clusters=7,name=['上海交大闵行校区','上海南站','世纪广场','上海站','南汇汽车站','佘山','南翔']):#聚类后7个中心所对应的位置
        super().__init__()
        self.n_clusters = n_clusters
        self.name=name
    def calculate(self):#将分类的标签分别与地名相绑定
        k = KMeans(n_clusters=self.n_clusters).fit_predict(self.da, self.weight)
        data =self.df[['north_latitude', 'east_longitude', 'unitprice']]
        name = ['佘山', '南翔', '上海南站', '上海站', '上海交大闵行校区', '世纪广场', '南汇']
        data['label'] = k

        xc, yc = [], []
        for i in range(self.n_clusters):
            d = data[data['label'] == i]
            xe = sum(d['east_longitude'] * d['unitprice']) / sum(d['unitprice'])
            ye = sum(d['north_latitude'] * d['unitprice']) / sum(d['unitprice'])
            xc.append(xe)
            yc.append(ye)
        ctx= [xc[i] for i in k]
        cty= [yc[i] for i in k]
        data['x_c'] = ctx
        data['y_c'] = cty
        data = data.sort_values(by='x_c', ascending=True)
        label = [sorted(xc).index(i) for i in list(data['x_c'])]
        data['label'] = label
        centre = [name[i] for i in label]
        data['centre'] = centre
        return data,xc,yc
    def paint(self,data,xc,yc):#对聚类结果进行可视化
        sns.set_style('darkgrid')
        zh = matplotlib.font_manager.FontProperties(fname=r'C:\Windows\Fonts\simkai.ttf')
        sns.set(font=zh.get_name())
        sns.relplot(x='east_longitude', y='north_latitude', hue='centre', size='unitprice', data=data, sizes=(1, 200))
        plt.scatter(xc,yc,c='black', marker='x')
        plt.title('7 clusters divided by k-means')
        plt.savefig('7 clusters divided by k-means.jpg', format='jpg')
        plt.show()

if __name__ == '__main__':
    sk=Select_k()
    distance=sk.calculate()
    sk.paint(distance)
    km=K_means()
    data,xc,yc=km.calculate()
    km.paint(data,xc,yc)



