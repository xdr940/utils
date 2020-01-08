import  torch
import matplotlib.pyplot as plt
from random import  *


img = torch.linspace(start=0,end=99,steps=100).reshape([10,10])
img2 = torch.randint(low=0,high=4,size=[10,10])
img3 = torch.randint(low=0,high=2,size=[10,10])
img_ls = [img,img2,img3]

row = 2
col=3
cnt =1
for img in img_ls:
    plt.subplot(row, col, cnt)
    img=img.cpu().numpy()

    plt.imshow(img,cmap='terrain')
    cnt+=1
print(plt.colormaps())



plt.show()


