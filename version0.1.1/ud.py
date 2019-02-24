from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk

gui=Tk()
gui.title('Anaiysis of Unitprice,Houseage,Housesize and Distance')



tabcontrol=ttk.Notebook(gui)
tab1 = ttk.Frame(tabcontrol)       
tabcontrol.add(tab1, text='pairplot')
sl=Scrollbar(tab1,orient=VERTICAL)
sl.pack(side=RIGHT,fill=Y)



tab2 = ttk.Frame(tabcontrol)          
tabcontrol.add(tab2, text='Tab 2')
tabcontrol.pack(expand=1, fill="both")

im1=Image.open('pairplot.jpg')
img1=ImageTk.PhotoImage(image=im1,size=(120,120))
im1label=Label(tab1,image=img1).pack()

gui.mainloop()