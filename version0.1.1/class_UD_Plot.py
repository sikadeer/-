import matplotlib.pyplot as plt
import seaborn as sns
from class_WholePainting import WholePainting

class UD_plot(WholePainting):
    def histopaint(self):
        wh=WholePainting()
        sns.set_style('whitegrid')
        plt.subplot(121)
        wh.histo('distance', bins=20, axlabel='distance(km)', log=False)
        plt.subplot(122)
        wh.histo('distance', bins=20, axlabel='distance(after taking logarithm)(km)')
        plt.savefig('the Histogram of distance.jpg')
        plt.show()
    def jointPaint(self):
        wh = WholePainting()
        wh.joint('distance','unitprice',x=0.88,y=180000,log=False)
        plt.savefig('Jointplot between unitprice and distance')
        plt.show()

ud=UD_plot()
ud.histopaint()
ud.jointPaint()