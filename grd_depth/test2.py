
#alpha, h一定
#  d(theta;alpha,h)
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
#print(temp)
#y= (sin(alpha+theta)/sin(pi/2 + theta))
d45 = sqrt((1+tan(pi/4-alpha45+theta)**2)*h**2 )
d30 = sqrt((1+tan(pi/4-alpha30+theta)**2)*h**2 )
plt.plot(theta,d45,'b',label = 'alpha45')
plt.plot(theta,d30,'r',label='alpha30')
plt.legend()
plt.show()