import sqlite3
import numpy as np
cx=sqlite3.connect('data.db')
cu=cx.cursor()
# cu.execute('''create table data
# (name,age,sex,height)''')
# data=[(x,x,x,x) for x in range(1000)]
# for i in data:
#     cu.execute('insert into data values(?,?,?,?)',i)
#     cx.commit()
cu.execute('select * from data')
print(cu.fetchall())