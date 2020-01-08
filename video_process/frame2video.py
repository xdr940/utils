import cv2
from path import Path
from tqdm import tqdm
import argparse

folderName1 = '/home/roit/aws/aprojects/monodepth2_pt/uav0000013_00000_v_out'  # 269
folderName2 = '/home/roit/aws/aprojects/monodepth2_pt/uav0000144_01980_s_out'  # 181
folderName3 = '/home/roit/aws/aprojects/monodepth2_pt/uav0000023_00870_s_out'  # 300
folderName4 = '/home/roit/aws/aprojects/monodepth2_pt/uav0000079_00480_v_out'  # 361

a = '/home/roit/datasets/VisDrone/VisDrone2018-SOT-test/sequences/uav0000023_00870_s'
b = '/home/roit/datasets/VisDrone/VisDrone2018-SOT-train/sequences/uav0000144_01980_s'
c = '/home/roit/datasets/VisDrone/VisDrone2019-VID-train/sequences/uav0000013_00000_v'
d = '/home/roit/aws/utils/video_process/out_frames/2019_11_24_16_42_d'


parser =argparse.ArgumentParser(description="generate histogram ")
parser.add_argument('--path',default='/home/roit/datasets/MC/2019_11_24_16_42/normal')
parser.add_argument('--out_path',default=None)
parser.add_argument('--out_h',default=256,type=int)
parser.add_argument('--out_w',default=384,type=int)
parser.add_argument('--ext',default='jpg')

parser.add_argument('--type',default='rgb',choices=['rgb','gray'])
parser.add_argument('--scales',default=255,choices=[1,255])
parser.add_argument('--near',default='big_value',choices=['small_value','big_value'])

args = parser.parse_args()

def main():
    fps = 10   #视频帧率
    dump_root = './2019_11_24_16_42_d.avi'
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    folderName = d#269
    videoWriter = cv2.VideoWriter(dump_root, fourcc, fps, (1920,1080))   #和输入一样大小wh


    folderName = Path(folderName)
    if folderName.exists()==False:
        print('folder no exist')
        return
    files = folderName.files('*.{}'.format('png'))
    files.sort()
    for img_p in tqdm(files):


        img = cv2.imread(img_p)
        videoWriter.write(img)
    videoWriter.release()
if __name__=='__main__':
    main()
    print('ok')
