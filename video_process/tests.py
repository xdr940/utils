import torch

a = torch.tensor([1.2,3.4,5.2])
c = torch.tensor([2,3])
b = a.type_as(c)
f = a.int()
g = a.type(torch.int8)
print(g)