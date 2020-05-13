import cv2
from path import Path
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F

root = Path('./data')
files = root.files('*.png')
files.sort()
imgs = []
for file in files:
    temp = cv2.imread(file)
    temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
    temp = np.expand_dims(temp, axis=0)
    temp = np.expand_dims(temp, axis=0)
    imgs.append(temp / 255)
batch = np.concatenate(imgs, axis=0)
batch = 1-batch




def erode(batch):
    def conv(batch, weight):
        return F.conv2d(input=batch, weight=weight,padding=1)
#    weight = torch.ones([1, 1, 5, 5]).type(torch.float)
    weight75 = torch.tensor([0, 0, 0,0,0,
                           1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           1,1,1,1,1,
                           1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           0,0,0,0,0]).type(torch.float).reshape([1,1,7,5])

    weight33 = torch.tensor([0,1,0,
                           1, 1, 1,
                           0, 1, 0]).type(torch.float).reshape([1, 1, 3, 3])
    weight55 = torch.tensor([0, 0, 0,0,0,
                             0, 0, 0, 0, 0,
                             1, 1, 1,1,1,
                             0, 0, 0, 0, 0,
                             0, 0, 0,0,0]).type(torch.float).reshape([1, 1, 5,5])

    weight = weight33
    w_sum = weight.sum()
    batch = torch.tensor(batch).type_as(weight)


    cnt = 0
    ret = batch
    while(cnt<4):

        ret = conv(ret, weight)
        ret[ret<w_sum] = 0
        ret/=w_sum
        cnt+=1


    return ret

def dilation(batch):
    def conv(batch, weight):
        return F.conv2d(input=batch, weight=weight,padding=1)
#    weight = torch.ones([1, 1, 5, 5]).type(torch.float)
    weight = torch.tensor([0, 0, 0,0,0,
                           1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           1,1,1,1,1,
                           1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           0,0,0,0,0]).type(torch.float).reshape([1,1,7,5])

    weight33 = torch.tensor([0,1, 0,
                           1, 1, 1,
                           0, 1, 0]).type(torch.float).reshape([1, 1,3, 3])
    weight55 = torch.tensor([0, 1, 0,
                             1, 1, 1,
                             0, 1, 0]).type(torch.float).reshape([1, 1, 3, 3])

    w_sum = weight33.sum()
    batch = torch.tensor(batch).type_as(weight33.clone().detach().requires_grad_(True))

    cnt = 0
    ret  = batch
    while(cnt<2):

        ret = conv(ret, weight33)
        ret[ret>0] = 1
        cnt+=1


    return ret

def torch_test():
    save = True
    ret =batch
    #ret0 = dilation(batch)
    #ret1 = erode(ret)
    ret2 = dilation(ret)

    num = 16
    src = batch[num-1][0]
    dst1 = ret[num-1][0]
    dst2 = ret2[num-1][0]


    plt.subplot(3,1,1)
    plt.imshow(src)
    plt.subplot(3,1,2)
    plt.imshow(dst1)
    plt.subplot(3, 1, 3)
    plt.imshow(dst2)
    plt.show()

    if save==True:
        plt.imsave('src.png',src,cmap='bone')
        plt.imsave('erosion.png',dst1,cmap='bone')
        plt.imsave('dilation.png',dst2,cmap='bone')


    print('ok')



def opcv(batch):


    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3,1))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1,3))

    # 先erosion 再 dilation 去除孤立点， 并将rigid 区域变大一些
    img = batch[2][0]
    ret = cv2.erode(img, kernel1, iterations=5)
    ret = cv2.dilate(ret, kernel2, iterations=2)


    plt.subplot(3,1,1)
    plt.imshow(img)
    plt.subplot(3,1,2)
    plt.imshow(ret)
    plt.subplot(3,1,3)
    plt.imshow(img-ret)
    plt.show()


    print('ok')

if __name__ == '__main__':
    torch_test()
    #opcv(batch)