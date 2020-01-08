import torch
import torch.nn.functional as f
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np

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


def high_res_colormap(low_res_cmap, resolution=1000, max_value=1):
    # Construct the list colormap, with interpolated values for higer resolution
    # For a linear segmented colormap, you can just specify the number of point in
    # cm.get_cmap(name, lutsize) with the parameter lutsize
    x = np.linspace(0,1,low_res_cmap.N)
    low_res = low_res_cmap(x)
    new_x = np.linspace(0,max_value,resolution)
    high_res = np.stack([np.interp(new_x, x, low_res[:,i]) for i in range(low_res.shape[1])], axis=1)
    return ListedColormap(high_res)


def gradient(pred):
    D_dy = pred[:, :, 1:] - pred[:, :, :-1]
    D_dx = pred[:, :, :, 1:] - pred[:, :, :, :-1]
    return D_dx, D_dy


def opencv_rainbow(resolution=1000):
    # Construct the opencv equivalent of Rainbow
    opencv_rainbow_data = (
        (0.000, (1.00, 0.00, 0.00)),
        (0.400, (1.00, 1.00, 0.00)),
        (0.600, (0.00, 1.00, 0.00)),
        (0.800, (0.00, 0.00, 1.00)),
        (1.000, (0.60, 0.00, 1.00))
    )

    return LinearSegmentedColormap.from_list('opencv_rainbow', opencv_rainbow_data, resolution)


COLORMAPS = {'rainbow': opencv_rainbow(),
             'magma': high_res_colormap(cm.get_cmap('magma')),
             'bone': cm.get_cmap('bone', 10000)}


def tensor2array(tensor, max_value=None, colormap='magma',out_shape = 'CHW'):



    tensor = tensor.detach().cpu()
    if max_value is None:
        max_value = tensor.max().item()
    if tensor.ndimension() == 2 or tensor.size(0) == 1:
        norm_array = tensor.squeeze().numpy()/max_value
        if colormap!=None:
            array = COLORMAPS[colormap](norm_array).astype(np.float32)
            array = array[:,:,:3]
            array = array.transpose(2, 0, 1)
            if out_shape == 'HWC' :
                array = array.transpose(1,2,0)
        else:
            return  norm_array
    elif tensor.ndimension() == 3:
        if (tensor.size(0) == 3):
            array = 0.5 + tensor.numpy()*0.5
        elif (tensor.size(0) == 2):
            array = tensor.numpy()

        if out_shape == 'HWC' :
            array = array.transpose(1,2,0)

    return array

def writelines(list,path):
    with open(path,'w') as f:
        for item in list:
            f.writelines(item+'\n')

def readlines(filename):
    """Read all the lines in a text file and return as a list
    """
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    i = 0
    while i < len(lines):# i
        if lines[i][0]=='#':
            lines.pop(i)
        i+=1
    return lines
def normalize_image(x):
    """Rescale image pixels to span range [0, 1]
    """
    max = float(x.max().cpu().data)
    min = float(x.min().cpu().data)
    d = max - min if max != min else 1e5
    return (x.type(torch.float) - min) / d