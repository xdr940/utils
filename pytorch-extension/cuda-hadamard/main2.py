import torch

from hadamard2 import Hadamard as mylayer
from time import time


class Network(torch.nn.Module):
	def __init__(self):
		super(Network, self).__init__()
	# end

	def forward(self, input1, input2):

		return mylayer()(input1, input2)



def main():

    net = Network().cuda()
    for i in range(3):
        input1 =3* torch.ones([ 1,1,3, 4]).cuda()
        input2 =4*torch.ones([1,1, 3, 4]).cuda()

        input1 = input1.requires_grad_()
        input2 = input2.requires_grad_()
        end = time()
        output = net(input1, input2)
        time1 = time()
        expected = torch.mul(input1, input2)
        time2 = time()

        print('\ntime1:{:.2f} us \n time2:{:.2f}\n'.format(1000000 * (time1 - end), 1000000 * (time2 - time1)))

        print((output.data - expected.data).abs().sum(), '<-- should be 0.0')
        print(torch.autograd.gradcheck(net, tuple([input1, input2]), 0.001), '<-- should be true')
        print(output)
    # end

def main2():
    print('switching to DataParallel mode')

    net = torch.nn.DataParallel(Network()).cuda()
    for i in range(3):
        input1 = torch.rand(2, 3, 8, 8).cuda()
        input2 = torch.rand(2, 3, 8, 8).cuda()

        input1 = input1.requires_grad_()
        input2 = input2.requires_grad_()

        output = net(input1, input2)
        expected = torch.mul(input1, input2)

        print((output.data - expected.data).abs().sum(), '<-- should be 0.0')
        print(torch.autograd.gradcheck(net, tuple([input1, input2]), 0.001), '<-- should be true')

if __name__ =="__main__":
    assert (int(str('').join(torch.__version__.split('.')[0:3])) >= 41)  # requires at least pytorch version 0.4.1
    main()