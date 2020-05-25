
import cv2
import numpy as np
from path import Path
import matplotlib.pyplot as plt
path = Path('./poles/10.png')
img = cv2.imread(path)
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# canny(): 边缘检测
img = cv2.GaussianBlur(img,(7,7),0)
canny = cv2.Canny(img, 100, 150)

# 形态学：边缘检测
_,Thr_img = cv2.threshold(img,210,255,cv2.THRESH_BINARY)#设定红色通道阈值210（阈值影响梯度运算效果）
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))         #定义矩形结构元素
kernel2 = np.array([1, 0, 1,
                    1, 0, 1,
                    1, 0, 1]).astype(np.uint8).reshape([3, 3])  # 向右卷积， src中暗处(小)点在src‘中值较大
gradient = cv2.morphologyEx(Thr_img, cv2.MORPH_GRADIENT, kernel2) #梯度
shows = [
    img,
    canny,
    gradient
]
pltshow(shows)
#plt.imshow("original_img", original_img)
#plt.imshow("gradient", gradient)





