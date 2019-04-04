from class_spider import DataSpider
from class_wash import Wash
from class_paint import Paint
from class_feature_select import FeatureSelect
from class_predict import Predict
import time
import pandas as pd
import matplotlib.pyplot as plt
import warnings

'''请确保程序运行环境是python3.5或以上版本！！！'''

warnings.filterwarnings('ignore')
def spider():#爬取数据
    COUNT = 300
    DELAY = 30
    spider = DataSpider()
    for i in range(COUNT):  # 爬取、抓取网页前300页的有效信息,当网络中断时请更改此行继续运行！！！
        if i % 20 == 0 and i > 0:  # 每爬取20页sleep30s防止被识别
            time.sleep(DELAY)
        url = r'https://sh.lianjia.com/chengjiao/pg{:d}ng1nb1/'.format(i + 1)
        link = spider.GetLink(url)  # 获取每条信息的地址
        for j in link:
            print('正在获取第{0:d}页第{1:d}条数据…………'.format(i + 1, link.index(j) + 1))
            text = spider.GetHtmlText(j)  # 获取当前页面的源代码
            unit_price = spider.Getunit_price(text)  # 爬取房屋单价
            structure = spider.GetStructure(text)  # 爬取房屋结构
            storey = spider.GetStorey(text)  # 爬取房屋楼层
            size = spider.GetSize(text)  # 爬取房屋面积
            age = spider.GetAge(text)  # 爬取房龄
            decorate = spider.GetDecorate(text)  # 爬取房屋装修情况
            loc = spider.GetLoc(text)  # 爬取房屋地址
            xp, yp = spider.GetXY(loc)  # 爬取房屋经纬度
            data = [unit_price, structure, storey, size, age, decorate, loc, xp, yp]
            spider.SaveData(data)  # 将此条信息存储至数据库中
    conn = spider.conn
    conn.close()
    print('爬虫部分已完成')


def wash():#对得到的数据进行初步处理
    w = Wash()  # 下10行对各特征值进行数据类型转换和过滤极端异常值
    w.GetDataFromDatabase('data.db')
    w.UnitPriceWash()
    w.StructureWash()
    w.StoreyWash()
    w.SizeWash()
    w.AgeWash()
    w.DecorateWash()
    w.XYWash()
    raw_df = w.df
    raw_df.drop_duplicates(['unit_price', 'structure', 'storey', 'size'], inplace=True)  # 去重

    p = Paint()#绘制价格和地段示意图，用于分析找到城市中心位置
    p.GetDataFromDataframe(raw_df)
    plt.figure(figsize=(8, 8))
    pc1 = p.xyplot()
    plt.savefig('图1：上海二手房价格与地段示意图')
    w.GetDistance(2)#通过Kmeans聚类找到房价的两个质心位置，并计算各房屋距离两个质心的平均距离
    w.Select()
    df = w.df
    df.to_excel('RawData.xls')  # 将初步清洗的数据存储于excel中
    print('数据初步清洗部分已完成')


def norm():#对初步清洗的数据进行归一化
    w = Wash()
    w.GetDataFromExcel('RawData.xls')
    for i in ['unit_price', 'size', 'age', 'distance']:  # 对数据进行不同方式的归一化并比较其效果
        w.LogTrans(i)
        w.SqrtTrans(i)
        w.BoxCoxTrans(i)
    df = w.df
    p = Paint()
    p.GetDataFromDataframe(df)
    plt.figure(figsize=(8, 8))#对未归一化的效果进行可视化，并计算其偏度和峰度
    plt.subplot(221)
    pc2 = p.histo('unit_price', bins=30, x=75000, y=0.00002)
    plt.subplot(222)
    pc3 = p.histo('size', bins=30, x=120, y=0.012)
    plt.subplot(223)
    pc4 = p.histo('age', bins=30, x=25, y=0.06)
    plt.subplot(224)
    pc5 = p.histo('distance', bins=30, x=55, y=0.08)
    plt.suptitle('Histogram of Raw Data')
    plt.savefig('图2：未归一化的数据直方图')


    plt.figure(figsize=(8, 8))#对对数归一化的效果进行可视化，并计算其偏度和峰度
    plt.subplot(221)
    pc6 = p.histo('LogTransunit_price', bins=30, x=0.65, y=2)
    plt.subplot(222)
    pc7 = p.histo('LogTranssize', bins=30, x=0.65, y=2)
    plt.subplot(223)
    pc8 = p.histo('LogTransage', bins=30, x=0.65, y=4)
    plt.subplot(224)
    pc9 = p.histo('LogTransdistance', bins=30, x=0.5, y=4)
    plt.suptitle('Histogram of Log Normalization')
    plt.savefig('图3：Log归一化的直方图')

    plt.figure(figsize=(8, 8))#对Sqrt归一化的效果进行可视化，并计算其偏度和峰度
    plt.subplot(221)
    pc10 = p.histo('SqrtTransunit_price', bins=30, x=0.65, y=2)
    plt.subplot(222)
    pc11 = p.histo('SqrtTranssize', bins=30, x=0.65, y=2)
    plt.subplot(223)
    pc12 = p.histo('SqrtTransage', bins=30, x=0.65, y=2)
    plt.subplot(224)
    pc13 = p.histo('SqrtTransdistance', bins=30, x=0.65, y=6)
    plt.suptitle('Histogram of Sqrt Normalization')
    plt.savefig('图4：Sqrt归一化的直方图')

    plt.figure(figsize=(8, 8))#对Sqrt归一化的效果进行可视化，并计算其偏度和峰度
    plt.subplot(221)
    pc10 = p.histo('BoxCoxTransunit_price', bins=30, x=0.65, y=2)
    plt.subplot(222)
    pc11 = p.histo('BoxCoxTranssize', bins=30, x=0.65, y=2)
    plt.subplot(223)
    pc12 = p.histo('BoxCoxTransage', bins=30, x=0.65, y=2)
    plt.subplot(224)
    pc13 = p.histo('BoxCoxTransdistance', bins=30, x=0.2, y=2)
    plt.suptitle('Histogram of Sqrt Normalization')
    plt.savefig('图5：BoxCox归一化的直方图')
    df['unit_price'] = df['BoxCoxTransunit_price']#对比后最终选用对数归一化方法
    df['size'] = df['BoxCoxTranssize']
    df['age'] = df['BoxCoxTransage']
    df['distance'] = df['BoxCoxTransdistance']
    df.drop(['LogTransunit_price','SqrtTransunit_price','BoxCoxTransunit_price','LogTranssize','SqrtTranssize','BoxCoxTranssize','LogTransage','SqrtTransage','BoxCoxTransage','LogTransdistance','SqrtTransdistance','BoxCoxTransdistance'], axis=1, inplace=True)
    df.to_excel('Washed Data.xls')  # 将归一化的数据存储于excel中
    print('数据归一化部分已完成')


def select_feature():#选取用于拟合的特征
    p = Paint()
    p.GetDataFromExcel('Washed Data.xls')
    p14 = p.heat()
    plt.savefig('图6：诸特征之间相关系数热力图')

    p15 = p.joint('size','unit_price')
    plt.savefig('图7：房屋单价及面积关系图')
    p16 = p.joint('age','unit_price')
    plt.savefig('图8：房屋单价及房龄关系图')
    p17 = p.box('decorate', 'unit_price')
    plt.savefig('图9：房屋单价及装修情况箱型图')
    p18 = p.joint('distance','unit_price')
    plt.savefig('图10：房屋单价及距市中心距离关系图')

    sf = FeatureSelect()#最终选定房屋单价、房龄、距离、装修状况和卧室与卫生间数量的比值作为最终拟合的特征值
    sf.GetDataFromDataframe('Washed Data.xls')
    sf.SelectAge()
    sf.SelectDistance()
    sf.SelectDecorate()
    sf.SelectBedroom_Lavatory()
    data = sf.NewData()
    p.GetDataFromExcel('FinalData.xls')
    p19 = p.box('b_l', 'unit_price')
    plt.savefig('图11：房屋单价及卧室卫生间比率箱型图')
    p20 = sf.HeatPlot(data)
    plt.savefig('图12：最终选取特征值之间相关系数热力图')
    print('数据特征选取部分已完成')


def predict():
    pr = Predict()
    x = ['ridge', 'ridge', 'lasso', 'lasso', 'linear', 'linear', 'SVM', 'SVM', 'random', 'random']
    y = []
    y += pr.ridge()  # 分别比较各种回归算法（岭回归、套索回归、线性回归、支持向量机）和纯随机数之间的准确率
    y += pr.lasso()
    y += pr.linear()
    y += pr.SVM()
    y += pr.random()
    hue = ['train_accuracy', 'test_accuracy'] * 5
    data = pd.DataFrame({'algorithm': x,
                         'accuracy': y,
                         'kind': hue})
    print(data)
    p = Paint()
    p.GetDataFromDataframe(data)
    plt.figure(figsize=(8, 8))
    p21 = p.bar('algorithm', 'accuracy', 'kind')
    plt.savefig('图13：各种回归算法及随机数预测准确率柱状图')
    print('数据拟合部分部分已完成')

def main():
    wash()
    norm()
    select_feature()
    predict()
    print('请查看原文件中生成的数据及图像')

main()