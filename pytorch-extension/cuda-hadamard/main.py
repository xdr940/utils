import torch

import hadamard
from time import time

assert(int(str('').join(torch.__version__.split('.')[0:3])) >= 41) # requires at least pytorch version 0.4.1

class Network(torch.nn.Module):
	def __init__(self):
		super(Network, self).__init__()
	# end

	def forward(self, input1, input2):
		return hadamard.Hadamard()(input1, input2)
	# end
# end

net = Network().cuda()

def test_time():
	for i in range(3):
		input1 = torch.rand(2, 3, 8, 8).cuda()
		input2 = torch.rand(2, 3, 8, 8).cuda()

		input1 = input1.requires_grad_()
		input2 = input2.requires_grad_()
		end = time()
		output = net(input1, input2)
		time1 = time()
		expected = torch.mul(input1, input2)
		time2 = time()

		print('\ntime1:{:.2f} us \n time2:{:.2f}\n'.format(1000000*(time1-end),1000000*(time2-time1)))

		print((output.data - expected.data).abs().sum(), '<-- should be 0.0')
		print(torch.autograd.gradcheck(net, tuple([ input1, input2 ]), 0.001), '<-- should be true')
	# end

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
		print(torch.autograd.gradcheck(net, tuple([ input1, input2 ]), 0.001), '<-- should be true')
	# end

def test_grad():
	in1 = in1_h = torch.tensor([1.,2,3,4,5,6,7,8],requires_grad=True).reshape(1,1,2,4).cuda()
	in2 = in2_h = torch.tensor([2.,3,4,5,6,7,8,9],requires_grad=True).reshape(1,1,2,4).cuda()

	out_h = net(in1_h,in2_h)
	out = in1*in2

	in1_h.retain_grad()
	in2_h.retain_grad()

	in1.retain_grad()
	in2.retain_grad()

	out_h[0][0][0][0].backward()

	out[0][0][0][0].backward()
	print(in1_h.grad)
	print(in1.grad)
	print(out_h)
	print(out)


if __name__ == '__main__':
	test_grad()