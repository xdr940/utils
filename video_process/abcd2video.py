import cv2
from path import Path
import matplotlib.pyplot as plt
import numpy as np
#concate 田字格演示
import argparse
from tqdm import tqdm
parser = argparse.ArgumentParser(description='KITTI evaluation')
parser.add_argument("--scale",
                    help="四个图像文件夹统一尺寸",
                    default=[600,800],
                    )

parser.add_argument("--out_dir",default='0807')
parser.add_argument('--interval_6dof',default=3)

args = parser.parse_args()

def main(args):
    fps = 10   #视频帧率
    dump_root = Path('./0807.avi')
    out_dir = Path(args.out_dir)
    out_dir.mkdir_p()
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    folderName1 = '/home/roit/datasets/MC/0807/p1/color'  # 269
    folderName2 = '/home/roit/datasets/MC/0807/p1/depth'  # 181
    folderName3 = '/home/roit/datasets/MC/0807/p1/normal'  # 300
    folderName4 = '/home/roit/aws/utils/video_process/0807_poses_p1_'  # 361



    videoWriter = cv2.VideoWriter(dump_root, fourcc, fps, (1200,1600))   #(1360,480)为视频大小


    frames=[]

    folderName1 = Path(folderName1)
    folderName2 = Path(folderName2)
    folderName3 = Path(folderName3)
    folderName4 = Path(folderName4)

    if folderName1.exists()==False :
        print('folder a no exist')
        return
    if folderName2.exists()==False :
        print('folder b no exist')
        return
    if folderName3.exists()==False:
        print('folder c no exist')
        return
    if folderName4.exists()==False:
        print('folder d no exist')
        return

    files1 = folderName1.files('*.{}'.format('png'))
    files1.sort()
    files2 = folderName2.files('*.{}'.format('png'))
    files2.sort()
    files3 = folderName3.files('*.{}'.format('png'))
    files3.sort()
    files4 = folderName4.files()
    files4.sort()
    cnt=0
    for img_p1,img_p2,img_p3,img_p4 in tqdm(zip( files1,files2,files3,files4)):

        img1 = plt.imread(img_p1)#
        img2 = plt.imread(img_p2)
        img3 = plt.imread(img_p3)
        img4 = plt.imread(img_p4)/255.



        img4 = cv2.resize(img4,(800,600))
        ones = np.ones([600,800,1]).astype(np.float)
        img4 = np.concatenate([img4,ones],axis=2)

        img_u = np.concatenate([img1,img2],axis=1)
        img_d = np.concatenate([img3,img4],axis=1)
        img = np.concatenate([img_u,img_d],axis=0)

    #    cv2.imshow('img', img12)
    #    cv2.waitKey(1000/int(fps))
        plt.imsave(out_dir/"{:04d}.png".format(cnt),img)
        cnt+=1
        #videoWriter.write(out_dir)
    videoWriter.release()
if __name__=='__main__':
    main(args)
    print('over')
