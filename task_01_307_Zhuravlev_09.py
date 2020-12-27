import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path as pth

p = pth('results') 
res = p / 'task_01_307b_Zhuravlev_9.txt' 
if not p.exists(): 
  p.mkdir(exist_ok=True) 
  if p.exists(): 
    with res.open('w') as f:
    def y(x): 
      y = 0.5 + ((np.sin(x**2))**2-0.5)/(1 + 0.001*(x**2))**2;
      y1 = round(y, 2);
      return y1
    
    f.write("X    Y")
    x = -10
    while x <= 10: 
      f.write("\n" + str(x) + "    " + str(y(x))) \
      x = x + 0.5

    x = np.arange(-10, 10)
    fig, ax = plt.subplots()
    ax.plot(x, y(x))  
    lgnd = ax.legend(['y'], loc='upper center', shadow=True)
    lgnd.get_frame().set_facecolor('green')
    plt.show()

