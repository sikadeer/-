import matplotlib.pyplot as plt
import seaborn as sns
from class_WholePainting import WholePainting

class UA_Plot(WholePainting):
    def histopaint(self):
        wh=WholePainting()
        sns.set_style('whitegrid')
        plt.subplot(121)
        wh.histo('houseage', bins=20, axlabel='houseage(year)', log=False)
        plt.subplot(122)
        wh.histo('houseage', bins=20, axlabel='houseage(after taking logarithm)(year)')
        plt.savefig('the Histogram of houseage.jpg')
        plt.show()
    def jointPaint(self):
        wh = WholePainting()
        wh.joint('houseage','unitprice',x=2.75,y=12)
        plt.savefig('Jointplot between unitprice and houseage')
        plt.show()

ua=UA_Plot()
ua.histopaint()
ua.jointPaint()
