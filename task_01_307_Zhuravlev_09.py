import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

p = Path('C:/python/result')
p.mkdir(parents=True)
p.is_dir()
# True
p.is_file()
# False
p.rmdir()

f = open("C:/python/result/task_01_307_Zhuravlev_9.txttest.txt", "w")
x = -10
def y(x): { 
y = 0.5 + ((np.sin(x**2))**2-0.5)/(1 + 0.001*(x**2))**2;
y1 = round(y, 2);
return y1;
}

f.write("X    Y")

while x <= 10: {
f.write("\n" + str(x) + "    " + str(y(x))); 
x = x + 0.5;
}
f.close()

x = np.arange(-10, 10)
fig, ax = plt.subplots()
ax.plot(x, y(x))  
lgnd = ax.legend(['y'], loc='upper center', shadow=True)
lgnd.get_frame().set_facecolor('green')
plt.show()
