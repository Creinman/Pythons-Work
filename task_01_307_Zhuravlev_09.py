import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path as pth

filename = pth('C:/python/result/task_01_307_Zhuravlev_9.txttest.txt')
filename.touch(exist_ok=True)  
file = open(filename, "w")
#file = open("C:/python/result/task_01_307_Zhuravlev_9.txttest.txt", "w")
x = -10
def y(x): 
  y = 0.5 + ((np.sin(x**2))**2-0.5)/(1 + 0.001*(x**2))**2;
  y1 = round(y, 2);
  return y1
file.write("X    Y")
while x <= 10: 
file.write("\n" + str(x) + "    " + str(y(x))) 
x = x + 0.5
file.close()
x = np.arange(-10, 10)
fig, ax = plt.subplots()
ax.plot(x, y(x))  
lgnd = ax.legend(['y'], loc='upper center', shadow=True)
lgnd.get_frame().set_facecolor('green')
plt.show()

