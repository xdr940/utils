
from  path import  Path
import os
from tqdm import  tqdm

def kitti_line2path(item):
    item = item.split(' ')
    if item[2] == 'l':
        camera = 'image_02'
    elif item[2] == 'r':
        camera = 'image_01'
    return item[0] +'/'+camera+  '/data/'+ item[1] + '.png'

def mc_line2path(str):
    pass
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
def extract_gt_mc():
    dataset =Path('/home/roit/datasets/MC')
    txt_in = './mc/test_files.txt'
    out_dir = Path('./') / 'mc_gt'

    imgs = readlines(txt_in)
    out_dir.mkdir_p()

    for p in tqdm(imgs):
        p=p.split(' ')
        path = dataset/p[0]/'depth'/p[1]+'.png'#home/roit/datasets/MC/sq/depth/
        cmd = 'cp '+path+' '+out_dir/(p[0]+'_'+p[1]+'.png')
        os.system(cmd)

def extract_img_mc():
    dataset = Path('/home/roit/datasets/MC')
    txt_in = './mc/test_files.txt'
    out_dir = Path('./') / 'mc_img'

    imgs = readlines(txt_in)
    out_dir.mkdir_p()

    for p in tqdm(imgs):
        p = p.split(' ')
        path = dataset / p[0] / 'img' / p[1] + '.png'  # home/roit/datasets/MC/sq/depth/
        cmd = 'cp ' + path + ' ' + out_dir / (p[0] + '_' + p[1] + '.png')
        os.system(cmd)

def extract_img_eigen():
    dataset = Path('/home/roit/datasets/kitti')
    txt_in = './eigen/test_files.txt'
    out_dir = Path('./') / 'eigen_img'

    imgs = readlines(txt_in)
    out_dir.mkdir_p()

    for line in tqdm(imgs):
        path = kitti_line2path(line)
        p = path.split('/')

        cmd = 'cp ' + dataset/path + ' ' + out_dir / (p[1] + '_' + p[4])
        os.system(cmd)

if  __name__ == '__main__':
   extract_img_eigen()