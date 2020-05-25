import numpy as np
import cv2
import matplotlib.pyplot as plt
def pltshow(list,names=None,type='width'):
    lenth = len(list)
    row=0
    col=0
    if lenth>10:
        return

    if lenth>6:
        col=3
        row=3
    if lenth >3 and lenth<=6:
        col = 2
        row = 3
    if lenth<=3:
        col=1
        row=lenth
    print(col,row)
    if col!=0 and row !=0:
        for i in range(lenth):
            plt.subplot(row,col,i+1)
            plt.imshow(list[i])
            if names!=None:
                plt.title(names[i])

        plt.show()

def rectify(img):
    kernel = np.array([0, 1, 0,
                     0, 1, 0,
                     0, 1, 0]).reshape([3, 3]).astype(np.uint8)

    img = cv2.dilate(img, kernel, iterations=4)

    img = cv2.erode(img, kernel, iterations=4)

    return img

def zoom(list):
    x1,x2,y1,y2 = 0,20,247,260
    ret_list=[]
    for item in list:
        ret_list.append(item[x1:x2,y1:y2])
    return ret_list