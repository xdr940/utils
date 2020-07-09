
import torch
import torch.nn.functional as F
from path import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import pltshow,zoom
kernel_ver = torch.tensor([0,1,0,
                        0, 1, 0,
                        0, 1, 0]).type(torch.float).reshape([1,1, 3, 3]).cuda()
kernel_hor = torch.tensor([0,0,0,
                        1, 1, 1,
                        0, 0, 0]).type(torch.float).reshape([1,1, 3, 3]).cuda()
weight75 = torch.tensor([0, 0, 0,0,0,
                           1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           1,1,1,1,1,
                           1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1,
                           0,0,0,0,0]).type(torch.float).reshape([1,1,7,5])


left = torch.tensor([1, 0, -1,
                     2, 0, -2,
                     1, 0, -1]).type(torch.float).reshape([1,1, 3, 3]).cuda()
right = torch.tensor([-1, 0, 1,
                      -2, 0, 2,
                      -1, 0, 1]).type(torch.float).reshape([1,1, 3, 3]).cuda()  # 向右卷积， src中暗处(小)点在src‘中值较大

def dilation(batch,kernel=kernel_hor,iteration=1):

    w_sum = kernel.sum()
    batch =batch.type_as(kernel)
    #batch = batch.unsqueeze(dim=1)
    #batch = torch.tensor(batch).type_as(kernel)

    i =0
    ret=0
    while i<iteration:

        ret = F.conv2d(input=batch, weight=kernel, padding=1)
        ret[ret < w_sum] = 0
        ret /= w_sum
        i+=1

    return ret#.squeeze(dim=1)


def erosion(batch,kernel=kernel_ver,iteration=1):


    w_sum = kernel.sum()
    batch =batch.type_as(kernel)
    #batch = batch.unsqueeze(dim=1)
    i = 0
    ret = 0
    while i < iteration:

        ret = F.conv2d(input=batch, weight=kernel, padding=1)
        ret[ret > 0] = 1
        i+=1
    return ret#.squeeze(dim=1)

def rectify(batch):
    batch = batch.unsqueeze(dim=1)

    batch_ed = dilation(erosion(batch,iteration=1),iteration=1)
    #batch = batch.unsqueeze(dim=1)
    batch_l = F.conv2d(input=batch_ed,weight=left,padding=1)
    batch_l[batch_l>1]=1
    batch_l[batch_l<0]=0


    batch_r = F.conv2d(input=batch_ed, weight=right, padding=1)
    batch_r[batch_r > 1] = 1
    batch_r[batch_r < 0] = 0



    final =(batch_l+batch_r)

    final[final>1]=1
    final[final<0]=0
    final = dilation(erosion(final))
    return final.squeeze(dim=1),batch_r,batch_l,batch_ed
    #return batch2.squeeze(dim=1)

def test():
    file = Path('./poles/18.png')
    img = cv2.imread(file)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    batch = torch.tensor(img).unsqueeze(0)#.unsqueeze(1)
    batch[batch>1]=1
    batch = batch.type(torch.float).cuda()
    batch = batch.unsqueeze(dim=1)#bchw

    batch_ed = dilation(erosion(batch, kernel_ver,iteration=3), kernel_ver,iteration=3)
    # batch = batch.unsqueeze(dim=1)
    batch_l = F.conv2d(input=batch_ed, weight=left, padding=1)
    batch_l[batch_l > 1] = 1
    batch_l[batch_l < 0] = 0

    batch_r = F.conv2d(input=batch_ed, weight=right, padding=1)
    batch_r[batch_r > 1] = 1
    batch_r[batch_r < 0] = 0

    batch_lr = (batch_l + batch_r)

    batch_lr[batch_lr > 1] = 1
    batch_lr[batch_lr < 0] = 0
    final = dilation(erosion(batch_lr,kernel_hor),kernel_ver)
    final[final>0]=1
    combined=final+batch
    combined[combined>1]=1
    shows=[
        batch,#[0].cpu().numpy(),
        batch_ed,
        batch_l,
        batch_r,
        batch_lr,
        final,
        combined
    ]
    shows = tonumpy(shows)
    #shows = zoom(shows)
    pltshow(shows)

def tonumpy(shows):

    ret_list=[]

    for item in shows:
        ret_list.append(item[0,0].cpu().numpy())

    return ret_list
def main():
    pass

if __name__ == '__main__':

    test()
