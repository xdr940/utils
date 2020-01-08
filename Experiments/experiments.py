from SoftHistogram2D.soft_hist import SoftHistogram2D_H,SoftHistogram2D_W
import matplotlib.pyplot as plt
import torch
from path import Path
import os
from utils import *
import torch.nn as nn
import torch.nn.functional as f
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
import cv2
from opts import parse_args_main as parse_args

def main():
    path = Path('../data/0000057.png')
    img = plt.imread(path)  # 600,800
    if len(img.shape)==3:
        img = img[:, :, 0]#gray

    img = torch.tensor(img, dtype=torch.float).to(device)
    img = img.unsqueeze(0)
    img = img.unsqueeze(0) * 255
    b, c, h, w = img.shape

    # hist_soft
    hist_soft_h = SoftHistogram2D_H(device=device, bins=255, min=0, max=255, sigma=3, b=b, c=c, h=h, w=w)
    hist_soft_v = SoftHistogram2D_W(device=device, bins=255, min=0, max=255, sigma=3, b=b, c=c, h=h, w=w)


    out_h = hist_soft_h(img)
    out_v = hist_soft_v(img)
    img_h = tensor2array(out_h[0][0],colormap=None,out_shape='HWC')
    img_v = tensor2array(out_v[0][0],colormap=None,out_shape='HWC')

    hdx,hdy = gradient(out_h)
    vdx,vdy = gradient(out_v)
    hdxdy = hdx[:,:,:-1,:]*hdy[:,:,:,:-1]
    #print(hdxdy[hdxdy.abs()>0.1].abs().mean())
    #print((hdx>0.1).mean()+(hdy>0.1).mean())
    #print((vdx>0.1).mean()+(vdy>0.1).mean())


    hdx_img = tensor2array(hdx,colormap=None)
    hdy_img = tensor2array(hdy,colormap=None)

    hdx_h,hdx_w = hdx_img.shape
    hdy_h,hdy_w = hdy_img.shape

    hdxdy_img = tensor2array(hdxdy,colormap=None)

    vdx_img = tensor2array(vdx,colormap=None)
    vdy_img = tensor2array(vdy,colormap=None)
    vdx_h,vdx_w = vdx_img.shape
    vdy_h,vdy_w = vdy_img.shape


    vdxdy = vdx[:,:,:-1,:]*vdy[:,:,:,:-1]
    #print(vdxdy[vdxdy.abs()>0.1].abs().mean())

    vdxdy_img = tensor2array(vdxdy,colormap=None)


    plt.subplot(2,4,1)
    plt.imshow(img_h)
    plt.subplot(2,4,2)
    plt.imshow(hdx_img)
    plt.subplot(2,4,3)
    plt.imshow(hdy_img)
    plt.subplot(2,4,4)
    plt.imshow(hdxdy_img)

    #希望顺利


    plt.subplot(2,4,5)
    plt.imshow(img_v)
    plt.subplot(2,4,6)
    plt.imshow(vdx_img)
    plt.subplot(2,4,7)
    plt.imshow(vdy_img)
    plt.subplot(2,4,8)
    plt.imshow(vdxdy_img)

    print('hdx, hdy, vdx, vdy\n')
    print(float((hdx.abs()>0).sum())/hdx_h/hdx_w,
          float((hdy.abs() > 0).sum()) / hdy_h / hdy_w,
          float((vdx.abs() > 0).sum()) / vdx_h / vdx_w,
          float((vdy.abs() > 0).sum()) / vdy_h / vdy_w
          )
    plt.show()
    pass








def test():
    path = Path('../data/cyc.png')
    img = plt.imread(path)  # 600,800
    if len(img.shape) == 3:
        img = img[:, :, 0]  # gray

    img = torch.tensor(img, dtype=torch.float).to(device)
    img = img.unsqueeze(0)
    img = img.unsqueeze(0) * 255
    b, c, h, w = img.shape

    # hist_soft
    hist_soft_h = SoftHistogram2D_H(device=device, bins=255, min=0, max=255, sigma=3, b=b, c=c, h=h, w=w)
    hist_soft_v = SoftHistogram2D_W(device=device, bins=255, min=0, max=255, sigma=3, b=b, c=c, h=h, w=w)

    out_h = hist_soft_h(img)
    out_v = hist_soft_v(img)

    rober_h = rober(out_h)
    rober_v = rober(out_v)


    a = float((rober_h>0).sum())/h/255
    b = float((rober_v>0).sum())/w/255

    print(a,b)

    plt.subplot(1,2,1)
    plt.imshow(rober_h.cpu().numpy()[0][0])
    plt.subplot(1, 2, 2)
    plt.imshow(rober_v.cpu().numpy()[0][0])
    plt.show()

def test_rober():
    path = Path('../data/eigen_mono.png')
    img = plt.imread(path)  # 600,800
    if len(img.shape) == 3:
        img = img[:, :, 0]  # gray

    img = torch.tensor(img, dtype=torch.float).to(device)
    img = img.unsqueeze(0)
    img = img.unsqueeze(0)
    b, c, h, w = img.shape

    out = rober(img)#xiebian
   # out = rober2(img)

    plt.imshow(out.cpu().numpy()[0][0])
    plt.show()



def caculate_from_txt():
    args = parse_args()

    #txt_path = Path()
    txt_path = Path(os.path.dirname(__file__))/args.txt_path
    dirs= readlines(txt_path)

    files_ls =[ Path(dr).files() for dr in dirs]
    lines=[]
    line=[]
    batch=[]
    for files in files_ls:
        for img_p in files:
            img = cv2.imread(img_p)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img=torch.tensor(img).cuda()
            img = normalize_image(img)
            img = img.reshape(1, 1, img.shape[0], img.shape[1])
            line.append(stat(img))

        line = torch.tensor(line)
        line_hist = line.histc(bins=50,min=0,max=1)
        lines.append( line_hist.numpy())
        line=[]
    print('ok')

    plt.subplot(2,2,1)
    plt.plot(lines[0],'r')
    plt.subplot(2,2,2)
    plt.plot(lines[1],'g')
    plt.subplot(2,2,3)
    plt.plot(lines[2],'b')

    #plt.subplot(2,2,4)
    #plt.plot(lines[3],'y')
    plt.show()

def stat(img):#bchw
    #method 1
    #return float((img>img.min()).sum())/img.shape[-1]/img.shape[-2]
    #method2
    #temp = xber(img.cuda())
    temp=img
    mean = temp.mean()
    max = temp.max()
    median = temp.median()
    min = temp.min()
    #return float((temp>temp.mean()).sum())/temp.shape[-1]/temp.shape[-2]
    zeros = torch.zeros_like(img)
    zeros[(img<mean) *( img> min)] = 1.

    #pin = temp[0][0]
    #pin2 = (((pin<mean)*(pin>min)).type(torch.float))
    #cnt = pin2.sum()/pin.shape[-1]/pin.shape[-2]
    cnt = zeros.sum()/zeros.shape[-1]/zeros.shape[-2]

    return cnt

def stat_mean(img):#mean
    return img.mean()

def stat_median(img):
    return img.median()
def stat_min(img):
    return img.min()

if __name__ == '__main__':
    #main()
    #test_rober()
#
    caculate_from_txt()