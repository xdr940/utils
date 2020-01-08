import torch

#torch.histc()
a = torch.tensor([[1,2,3,4,5,6],[1,2,3,4,5,5]]).cuda()
b = a.histc(bins=-6)
c = torch.histc(a,bins=6)
print(b)
print(c)