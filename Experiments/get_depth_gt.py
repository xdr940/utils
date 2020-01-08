import os
from path import Path
def writelines(list,path):
    with open(path,'w') as f:
        for item in list:
            f.writelines(item+'\n')

def readlines(filename):
    """Read all the lines in a text file and return as a list
    """
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    return lines

def main():
    dataset_path = Path('/home/roit/datasets/MC')
    lines = readlines('MC_out.txt')#must same with xdr94_mono
    out_dir = Path('./mc_gt')
    out_dir.mkdir_p()
    i = 0
    for item in lines:
        item = item.split(' ')
        gt_path = dataset_path/item[0]/'depth'/item[1]+'.png'
        out_path=out_dir/'{:03d}.png'.format(i)
        os.system('cp '+gt_path+ ' '+out_path)
        i+=1

    pass

if __name__ == '__main__':
    main()