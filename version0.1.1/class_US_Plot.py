import matplotlib.pyplot as plt
import seaborn as sns
from class_WholePainting import WholePainting

class US_Plot(WholePainting):
    def histopaint(self):
        wh=WholePainting()
        sns.set_style('whitegrid')
        plt.subplot(121)
        wh.histo('housesize', bins=20, axlabel='housesize(m^2)', log=False)
        plt.subplot(122)
        wh.histo('housesize', bins=20, axlabel='housesize(after taking logarithm)(m^2)')
        plt.savefig('the Histogram of housesize.jpg')
        plt.show()
    def jointPaint(self):
        wh = WholePainting()
        wh.joint('housesize','unitprice',x=4.5,y=175000,log=False)
        plt.savefig('Jointplot between unitprice and housesize')
        plt.show()
us=US_Plot()
us.jointPaint()
us.histopaint()
