import matplotlib.pyplot as plt
import torch
from path import Path
import os
from utils import *
import torch.nn as nn
import torch.nn.functional as f
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
import cv2
from path import  Path
from  tqdm import  tqdm
from opts import parse_args_main as parse_args

def edge(tensor):
    filter_x = torch.tensor([-1, -1,-1,-1,
                             0,0,0,0,
                             0,0,0,0,
                            1, 1.,1,1]).reshape([1, 1, 4, 4]).cuda()  #

    filter_y = torch.tensor([-1, 0,0,1,
                            -1, 0,0,1.,
                             -1,0,0,1,
                             -1,0,0,1]).reshape([1, 1, 4, 4]).cuda()

    return (f.conv2d(tensor, filter_x) + f.conv2d(tensor, filter_y)).abs()

def rober(tensor):
    filter1 = torch.tensor([-1, 0,
                           0, 1.]).reshape([1, 1, 2, 2]).cuda()

    filter2 = torch.tensor([0,1,
                            -1,0.]).reshape([1, 1, 2, 2]).cuda()

    filter3 = torch.tensor([-1,-1,
                            1,1.]).reshape([1,1,2,2]).cuda()#

    filter4 = torch.tensor([-1,1,
                            -1,1.]).reshape([1,1,2,2]).cuda()
    out1 = f.conv2d(tensor, filter2)


    out3 = f.conv2d(tensor, filter3)
    out4 = f.conv2d(tensor,filter4)

    #out = torch.abs(out1.abs()-out2.abs())
    #out1[out1 <= out1.mean()] = 0
    ret3 = out3.abs()
    ret3[ret3<=ret3.mean()]=0

    ret4 = out4.abs()
    ret4[ret4 <= ret4.mean()] = 0

    ret = out1-ret3 -ret4
    ret[ret<=ret.mean()]=0
    return ret3
def xber(tensor):
    filter = torch.tensor([1,-1,1,
                           -1,1,-1,
                           1,-1,1.]).reshape([1,1,3,3]).cuda().type_as(tensor)

    out = f.conv2d(tensor,filter)
    return out



def t2arr(tensor):
    return tensor[0][0].detach().cpu().numpy()

def get_smooth_loss2(img,disp):
    edge_disp = torch.abs(disp[:, :, :, :-1] - disp[:, :, :, 1:])[:,:,:-1,:]+torch.abs(disp[:, :, :-1, :] - disp[:, :, 1:, :])[:,:,:,:-1]

    edge_img = torch.mean(torch.abs(img[:, :, :, :-1] - img[:, :, :, 1:]), 1, keepdim=True)[:,:,:-1,:]+torch.mean(torch.abs(img[:, :, :-1, :] - img[:, :, 1:, :]), 1, keepdim=True)[:,:,:,:-1]


    err = edge_disp*torch.exp(-edge_img)

    plt.subplot(2, 3, 1)
    plt.imshow(t2arr(edge_disp),cmap='Spectral')
    plt.subplot(2, 3, 2)
    plt.imshow(t2arr(edge_img),cmap='Spectral')
    plt.subplot(2, 3, 3)

    plt.imshow(t2arr(err),cmap='Spectral')

    return  err.mean()

def get_smooth_loss( img,disp):#bchw
    """Computes the smoothness loss for a disparity image
    The color image is used for edge-aware smoothness
    """
    grad_disp_x = torch.abs(disp[:, :, :, :-1] - disp[:, :, :, 1:])
    grad_disp_y = torch.abs(disp[:, :, :-1, :] - disp[:, :, 1:, :])

    grad_img_x = torch.mean(torch.abs(img[:, :, :, :-1] - img[:, :, :, 1:]), 1, keepdim=True)
    grad_img_y = torch.mean(torch.abs(img[:, :, :-1, :] - img[:, :, 1:, :]), 1, keepdim=True)

    grad_disp_x *= torch.exp(-grad_img_x)#err_x
    grad_disp_y *= torch.exp(-grad_img_y)#err_y

    ret = grad_disp_x[:,:,:-1,:]+grad_disp_y[:,:,:,:-1]

    plt.subplot(2,3,1)
    plt.imshow(t2arr(grad_disp_x))
    plt.subplot(2,3,2)
    plt.imshow(t2arr(grad_disp_y))
    plt.subplot(2,3,3)

    plt.imshow(t2arr(grad_img_x))

    plt.subplot(2,3,4)
    plt.imshow(t2arr(grad_img_y))

    plt.subplot(2,3,5)
    plt.imshow(t2arr(ret))

    return ret.mean()

def get_smooth_loss3(img,disp):
    edge_img = edge(img)
    edge_disp = edge(disp)

    err = edge_disp*torch.exp(-edge_img+1)

    plt.subplot(2, 3, 1)
    plt.imshow(t2arr(edge_disp))

    plt.subplot(2, 3, 2)
    plt.imshow(t2arr(edge_img))

    plt.subplot(2, 3, 3)
    plt.imshow(t2arr(err))

    plt.show()
    return err.mean()


def caculate_reg():

    img_p = Path('/home/roit/datasets/reg/eigen_img')
    depth_p = Path('/home/roit/datasets/reg/eigen_test_out')

    imgs = img_p.files()
    depths = depth_p.files()

    imgs.sort()
    depths.sort()

    reg_loss = []
    cnt =0
    for img,depth in tqdm(zip(imgs,depths)):

        img = cv2.imread(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = torch.tensor(img).cuda()
        img = normalize_image(img)
        img = img.unsqueeze(dim=0).unsqueeze(0)
        #img = img.reshape(1, 1, img.shape[0], img.shape[1])

        depth = cv2.imread(depth)
        depth = cv2.cvtColor(depth, cv2.COLOR_RGB2GRAY)
        depth = torch.tensor(depth).cuda()
        depth = normalize_image(depth)
        depth = depth.reshape(1, 1, depth.shape[0], depth.shape[1])


        reg_loss.append(get_smooth_loss3(img,depth))

    reg_loss = torch.tensor(reg_loss)
    Min = float(reg_loss.min())
    Max = float(reg_loss.max())
    bins=100
    histc = reg_loss.histc(bins=bins,min=Min,max=Max).detach().cpu().numpy()
    x = np.linspace(start=Min,stop=Max,num=bins)
    plt.plot(x,histc)
    plt.show()

def caculate_reg_mc_gt():
    img_p = Path('/home/roit/datasets/reg/mc_img')
    depth_p = Path('/home/roit/datasets/reg/mc_gt')

    imgs = img_p.files()
    depths = depth_p.files()

    imgs.sort()
    depths.sort()

    reg_loss = []
    cnt = 0
    for img, depth in tqdm(zip(imgs, depths)):
        #if cnt > 30:
        #    break
        #cnt += 1
        img = cv2.imread(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = torch.tensor(img).cuda()
        img = normalize_image(img)
        img = img.unsqueeze(dim=0).unsqueeze(0)
        # img = img.reshape(1, 1, img.shape[0], img.shape[1])

        depth = cv2.imread(depth)
        depth = cv2.cvtColor(depth, cv2.COLOR_RGB2GRAY)
        depth = torch.tensor(depth).cuda()
        depth = normalize_image(depth)
        depth = depth.reshape(1, 1, depth.shape[0], depth.shape[1])

        reg_loss.append(get_smooth_loss3(img, depth))

    reg_loss = torch.tensor(reg_loss)
    Min = float(reg_loss.min())
    Max = float(reg_loss.max())
    bins=100
    histc = reg_loss.histc(bins=bins, min=Min, max=Max).detach().cpu().numpy()
    x = np.linspace(start=Min,stop=Max,num=bins)
    #plt.xlim([Min,Max])
    plt.plot(x,histc)
    plt.show()

def caculate_reg_mc_test():
    img_p = Path('/home/roit/datasets/reg/mc_img')
    depth_p = Path('/home/roit/datasets/reg/mc_test_out')

    imgs = img_p.files()
    depths = depth_p.files()

    imgs.sort()
    depths.sort()

    reg_loss = []
    cnt = 0
    for img, depth in tqdm(zip(imgs, depths)):
        #if cnt > 30:
        #    break
        #cnt += 1
        img = cv2.imread(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = torch.tensor(img).cuda()
        img = normalize_image(img)
        img = img.unsqueeze(dim=0).unsqueeze(dim=0)
        # img = img.reshape(1, 1, img.shape[0], img.shape[1])

        depth = cv2.imread(depth)
        depth = cv2.cvtColor(depth, cv2.COLOR_RGB2GRAY)
        depth = torch.tensor(depth).cuda()
        depth = normalize_image(depth)
        depth = depth.reshape(1, 1, depth.shape[0], depth.shape[1])

        reg_loss.append(get_smooth_loss3(img, depth))

    reg_loss = torch.tensor(reg_loss)
    Min = float(reg_loss.min())
    Max = float(reg_loss.max())
    bins=100
    histc = reg_loss.histc(bins=bins, min=Min, max=Max).detach().cpu().numpy()
    x = np.linspace(start=Min,stop=Max,num=bins)
    #plt.xlim([Min,Max])
    plt.plot(x,histc)
    plt.show()



if __name__ == '__main__':
    #main()
    #test_rober()
#
    #caculate_reg_mc_test()
   caculate_reg_mc_gt()
   # caculate_reg_mc_test()