import cv2
from path import Path
from tqdm import tqdm
import argparse




parser =argparse.ArgumentParser(description="generate histogram ")
parser.add_argument('--path',default='/home/roit/aws/utils/video_process/0807/')
parser.add_argument('--out_path',default=None)
parser.add_argument('--out_h',default=256,type=int)
parser.add_argument('--out_w',default=384,type=int)
parser.add_argument('--ext',default='jpg')

parser.add_argument('--type',default='rgb',choices=['rgb','gray'])
parser.add_argument('--scales',default=255,choices=[1,255])
parser.add_argument('--near',default='big_value',choices=['small_value','big_value'])

args = parser.parse_args()

def main(args):
    fps = 10   #视频帧率
    dump_root = './0807.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWriter = cv2.VideoWriter(dump_root, fourcc, fps, (1600,1200))   #和输入一样大小wh


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
