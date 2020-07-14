import cv2
from path import Path
from tqdm import tqdm
import argparse

import matplotlib.pyplot as plt


parser =argparse.ArgumentParser(description="generate histogram ")
parser.add_argument('--path',
                    #default='/home/roit/datasets/Binjiang/0008/',
                    #default='/media/roit/greenp2/output_dir/0020'
                    default='/media/roit/greenp2/output_dir/06021108_10001000p2'
                    #default='/home/roit/datasets/MC/10001000/p2/depth'

                    )
parser.add_argument('--out_path',default=None)
parser.add_argument('--input_size',default=(800,600))
parser.add_argument('--out_h',default=270,type=int)
parser.add_argument('--out_w',default=480,type=int)
parser.add_argument('--ext',default='png')

parser.add_argument('--type',default='rgb',choices=['rgb','gray'])
parser.add_argument('--scales',default=255,choices=[1,255])
parser.add_argument('--near',default='big_value',choices=['small_value','big_value'])
parser.add_argument('--fps',default=18)
args = parser.parse_args()

def main(args):
    fps = args.fps
    dump_root = './gt.avi'
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')


    videoWriter = cv2.VideoWriter(dump_root, fourcc, fps, args.input_size)   #和输入一样大小wh


    folderName = Path(args.path)
    if folderName.exists()==False:
        print('folder no exist')
        return
    files = folderName.files()
    files.sort()
    for img_p in tqdm(files):
        img = cv2.imread(img_p)
        videoWriter.write(img)
    videoWriter.release()
if __name__=='__main__':
    main(args)
    print('ok')
