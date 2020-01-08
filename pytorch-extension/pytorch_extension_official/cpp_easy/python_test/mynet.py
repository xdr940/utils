from torch.autograd import Function

import mynet_cpp# name of .so

class MyNetFunction(Function):

    @staticmethod
    def forward(ctx, x, y):
        return mynet_cpp.forward(x, y)

    @staticmethod
    def backward(ctx, gradOutput):
        gradX, gradY = mynet_cpp.backward(gradOutput)
        return gradX, gradY

	
import torch
class MyNet(torch.nn.Module):

    def __init__(self):
        super(MyNet, self).__init__()

    def forward(self, inputA, inputB):
        return MyNetFunction.apply(inputA, inputB)

