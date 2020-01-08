#d(dx,alpha,h)
#当dx增大时, d的关系为越大越正比

import numpy as np
import matplotlib.pyplot as plt
import math
from math import pi
from numpy import sin,sqrt,tan
#x = [0:0.1:pi]
theta = np.linspace(0,pi/4,100)
#ag = 45
#alpha = ag*2*pi/360
alpha45 = pi/8
alpha30 = pi/36
h=50
dx = np.linspace(0,30*h,100)

#print(temp)
#y= (sin(alpha+theta)/sin(pi/2 + theta))
d45 = sqrt((1+tan(pi/4-alpha45)**2)*h**2 + dx**2 +2*h*dx*tan(pi/4 - alpha45))
d30 = sqrt((1+tan(pi/4-alpha30)**2)*h**2 + dx**2 +2*h*dx*tan(pi/4 - alpha30))
plt.plot(dx,d45,'b',label = 'alpha45')
plt.plot(dx,d30,'r',label='alpha30')
plt.legend()
plt.show()