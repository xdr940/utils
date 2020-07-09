from path import Path
import numpy as np
data = Path('./poles')
out=Path('./out')
out.mkdir_p()
files =data.files()
import cv2
import matplotlib.pyplot as plt

kernel = np.array([0, 1, 0,
                   0, 1, 0,
                   0, 1, 0]).reshape([3, 3]).astype(np.uint8)
kernel_ = np.array([0, 0, 0,
                   1, 1, 1,
                   0, 0, 0]).reshape([3, 3]).astype(np.uint8)
from utils import pltshow,rectify,zoom
def main():
    pass
    path = Path('./poles/10.png')
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #img = cv2.GaussianBlur(img, (7, 7), 0)
    img[img>0]=1
    src = np.copy(img)
    #img = 1-img

    #ernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    # 先erosion 再 dilation 去除孤立点， 并将rigid 区域变大一些
    img = rectify(img)



    left = np.array([1, 0, -1,
                      2, 0, -2,
                      1, 0, -1]).reshape([3, 3])

    left = np.array([1, 0, -1,
                     2, 0, -2,
                     1, 0, -1]).reshape([3, 3])
    right = np.array([-1, 0, 1,
                      -2, 0, 2,
                      -1, 0, 1]).reshape([3, 3])  # 向右卷积， src中暗处(小)点在src‘中值较大



    img_l = cv2.filter2D(src=img, kernel=left, ddepth=-2)
    img_l[img_l<1]=0

    #img_l=rectify(img_l)

    img_r = cv2.filter2D(src=img, kernel=right, ddepth=-2)
    img_r[img_r < 1] = 0


    #[22:115,513:528]

    combined = img_l+img_r
    combined[combined>0]=1
    #combined2 = img_ll+img_rr
    #combined2[combined2>0]=1

    combined = cv2.dilate(combined, kernel_, iterations=1)
    combined = cv2.erode(combined, kernel, iterations=1)
    last = combined + src
    last[last > 0] = 1

    shows = [
        src,
        img,
        img_l,
        img_r,
        #img_lr,
        #img_rl,
        combined,
        last
    ]


    #shows = zoom(shows)
    names = [
        'src',
        'img',
        'img_l',
        'img_lr',
        'img_r',
        'l+r'

    ]
    pltshow(shows,names=None)

if __name__ == '__main__':
    main()