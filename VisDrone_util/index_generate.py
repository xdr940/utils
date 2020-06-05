from path import Path

import os
import argparse
parser = argparse.ArgumentParser(description='Simple testing funtion for Monodepthv2 models.')

parser.add_argument('--data_path', type=str,
                             default='/home/roit/datasets/VisDrone2',
                            help='path to a test image or folder of images')




def main(opt):
    data_path = Path(opt.data_path)
    dirs = data_path.dirs()
    dirs.sort()

    cnt=0
    print('|id|seq|img|notes|\n|--|--|--|--|')
    for dir in dirs:
        id='{:02d}'.format(cnt)
        seq_name = dir.stem
        path = '[img](./{}/0000001.jpg)'.format(seq_name)
        full = '|'+id+'|'+seq_name+'|'+path+'|-| '
        print(full)
        cnt+=1


if __name__ == '__main__':
    opt = parser.parse_args()
    main(opt)
