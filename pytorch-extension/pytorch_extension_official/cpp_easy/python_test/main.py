import torch

from mynet import MyNet

x = torch.tensor([1,2,3],dtype=torch.float32)
y = torch.tensor([4,5,6],dtype=torch.float32)
x.requires_grad=True
y.requires_grad=True

net = MyNet()
z = net(x, y)
#对向量不能直接求到，需要传入参数
z.backward(torch.tensor([1,1.2,1],dtype=torch.float32))
#z[0].backward()
# debug
print('x: ', x)
print('y: ', y)
print('z: ', z)
print('x.grad: ', x.grad)
print('y.grad: ', y.grad)
