
import torch
import numpy as np
from path import Path
import matplotlib.pyplot as plt
from sampler import Sampler
from random import random
import matplotlib.pyplot as plt
import torch
def main1():
    file = Path('./0000002.png')
    img = plt.imread(file)
    img = torch.tensor(img)
    mask1 = torch.ones(img.shape,dtype=torch.uint8)
    for i in range(mask1.shape[0]):
        for j in range(mask1.shape[1]):
            if i%2==0 and j%2 ==0:
                mask1[i][j] = True
            else:
                mask1[i][j]=False
    s1 = img[mask1].reshape(300,400)
    s1 = s1.data.numpy()
    #plt.imshow(mask1)
    print(img)
    plt.imshow(s1)
    plt.show()

def main2():
    #记录下tensor index
    a = torch.tensor([1,2,3,4,5,6,7,8,9,10]).reshape(1,1,2,5)
    b = torch.tensor([1,0,1,0,1,0,1,0,1,0]).reshape(1,1,2,5)
    d = torch.tensor([True,False,True,False,True,False,True,False,True,False]).reshape(1,1,2,5)
    c = a[d]
    print(c)

    pass
def main3():
    file = Path('./0000002.png')
    img = plt.imread(file)
    img = torch.tensor(img)

    img = img.unsqueeze(dim=0)
    img = img.unsqueeze(dim=0)
    img2 = torch.ones(4, 1, 128, 192)

    sam = Sampler(batch=1,channels=1,height=128,width=192, scales=6)
    scale_list = sam.down_resolution_sampling([img])

    #ims show
    nps = []
    for i in range(len(scale_list)):
      nps.append(scale_list[i].data.numpy())

    plt.subplot(2,3,1)
    plt.imshow(scale_list[0][0][0])
    plt.subplot(2, 3, 2)
    plt.imshow(scale_list[1][0][0])
    plt.subplot(2, 3, 3)
    plt.imshow(scale_list[2][0][0])
    plt.subplot(2, 3, 4)
    plt.imshow(scale_list[3][0][0])
    plt.subplot(2, 3, 5)
    plt.imshow(scale_list[4][0][0])
    plt.subplot(2, 3, 6)
    plt.imshow(scale_list[5][0][0])

    plt.show()
    print('ok')

if __name__=="__main__":

    main3()

    pass
