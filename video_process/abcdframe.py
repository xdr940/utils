#
#把2,3,4张图像合并成一张
#
#

import cv2
from path import Path
import matplotlib.pyplot as plt
import numpy as np
#concate 田字格演示
import argparse
from tqdm import tqdm
parser = argparse.ArgumentParser(description='imgs concat')
parser.add_argument("--resize",
                    help="四个图像文件夹统一尺寸",
                    #default=[192,640],
                    default=True,

                    )

parser.add_argument("--out_dir",default='./ab')
parser.add_argument('--folders',default=[
   # "/home/roit/datasets/MC/0000/p1/color",
   # "/home/roit/datasets/MC/0000/p1/depth",
   # "/home/roit/test_out/mc/ours_06020659_0000p1",
    #"/home/roit/test_out/mc/ours_06020659_0000p1_abc",
    #"/home/roit/test_out/mc/ours_06020659_0001p1_abc",
    #"/home/roit/test_out/mc/ours_06020659_0003p1_abc",
    "/home/roit/aws/aprojects/som-TSP/src/chains",
    "/home/roit/aws/aprojects/som-TSP/src/routes",
    "/home/roit/test_out/vsd/uav0000317_00000_s_atb",
    "/home/roit/test_out/vsd/uav0000240_00001_s_atb",
    "/home/roit/datasets/VSD/uav0000238_00001_s",
    "/home/roit/test_out/vsd/video_08171031w9_uav0000238_00001_s",
    "/home/roit/test_out/vsd/02_uav0000240_00001_s_masks/mean_mask",
    "/home/roit/test_out/vsd/02_uav0000240_00001_s_masks/var_mask",
    "/home/roit/test_out/vsd/02_uav0000240_00001_s_masks/final_mask"

])
parser.add_argument("--mode",
                    default='abcd',
                    choices=['abcd',
                             'abcdef',
                             'ab'])

args = parser.parse_args()

def main_abc(args):
    out_dir = Path(args.out_dir)
    out_dir.mkdir_p()

    folderName1 = args.folders[0]  # 269
    folderName1 = Path(folderName1)
    folderName2 = args.folders[1]  # 269
    folderName2 = Path(folderName2)

    folderName3 = args.folders[2]  # 300
    folderName3 = Path(folderName3)

    if folderName1.exists() == False:
        print('folder a no exist')
        return
    if folderName2.exists() == False:
        print('folder b no exist')
        return
    if folderName3.exists() == False:
        print('folder c no exist')

        return

    files1 = folderName1.files()
    files1.sort()
    files2 = folderName2.files()
    files2.sort()
    files3 = folderName3.files()
    files3.sort()


    cnt = 0
    print('--> files num:{}'.format(len(files1)))
    for img_p1,img_p2,img_p3 in tqdm(zip(files1, files2,files3)):
        img1 = plt.imread(img_p1)  #
        img2 = plt.imread(img_p2)
        img3 = plt.imread(img_p3)

        if img1.max() > 1:
            img1 = img1 / 255
        if img2.max() > 1:
            img2 = img2 / 255
        if img3.max() > 1:
            img3 = img3 / 255
        if args.resize:
            img1 = cv2.resize(img1, (2400, 600))[:, :, :3]
            img2 = cv2.resize(img2, (2400, 600))[:, :, :3]
            img3 = cv2.resize(img3, (2400, 600))[:, :, :3]

        img = np.concatenate([img1, img2,img3], axis=1)

        plt.imsave(out_dir / "{:04d}.png".format(cnt), img)
        cnt += 1
def main_ab(args):
    out_dir = Path(args.out_dir)
    out_dir.mkdir_p()

    folderName1 = args.folders[0]  # 269
    folderName1 = Path(folderName1)
    folderName2 = args.folders[1]  # 269
    folderName2 = Path(folderName2)


    if folderName1.exists() == False:
        print('folder a no exist')
        return
    if folderName2.exists() == False:
        print('folder b no exist')
        return


    files1 = folderName1.files()
    files1.sort()
    files2 = folderName2.files()
    files2.sort()



    cnt = 0
    print('--> files num:{}'.format(len(files1)))
    for img_p1,img_p2 in tqdm(zip(files1, files2)):
        img1 = plt.imread(img_p1)  #
        img2 = plt.imread(img_p2)

        if img1.max() > 1:
            img1 = img1 / 255
        if img2.max() > 1:
            img2 = img2 / 255

        if args.resize:
            img1 = cv2.resize(img1, (1000, 800))#[:, :, :3]
            img2 = cv2.resize(img2, (1000, 800))#[:, :, :3]


        img = np.concatenate([img1, img2], axis=1)#0 竖着， 1横着

        plt.imsave(out_dir / "{:04d}.png".format(cnt), img)
        cnt += 1



if __name__=='__main__':
    #main_abc(args)
    main_ab(args)

    print('over')
