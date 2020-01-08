
import torch
import sys
class Sampler():
    def __init__(self,batch,channels,height,width,scales=6,down_type = 'down_resolution'):
        '''

        :param scales:尺度数量，包括原图
        :param down_type:
        '''

        self.multiscale_masks=[]
        self.scalse = scales
        self.batch,self.channels , self.height, self.width  = batch,channels,height,width

        if down_type =='down_resolution':# 计算量最低的下采样，多分辨率采样mask

            for i in range(1, scales):
                tem = torch.zeros(self.height, self.width, dtype=torch.uint8)#没有bool以最小位数量为

                for j in range(tem.shape[0]):
                    for k in range(tem.shape[1]):
                        if j % pow(2,i) ==0 and k % pow(2,i) == 0:
                            tem[j][k] = 1

                tem = tem.unsqueeze(dim=0)#channel
                tem = tem.unsqueeze(dim=0)#batch
                batch=[]
                for i in range(self.batch):
                    batch.append(tem)
                self.multiscale_masks.append(torch.cat(batch,dim=0))



            print('ok')
            pass
    def down_resolution_sampling(self,scales_list):
        img = scales_list[0]
        assert (img.shape == (self.batch,self.channels,self.height,self.width))
        i = 2
        for item in self.multiscale_masks:
            tem = img[item]
            tem = tem.reshape(self.batch,self.channels,int(self.height/i), int(self.width/i))
            scales_list.append(tem)
            i*=2
        return scales_list