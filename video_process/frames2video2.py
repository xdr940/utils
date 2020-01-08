import cv2
from path import Path
import matplotlib.pyplot as plt
import numpy as np
#concate 田字格演示
def main():
    fps = 10   #视频帧率
    dump_root = Path('./dump2.avi')
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    folderName1 = './out_frames/2019_11_24_16_42_o'
    folderName2 = './out_frames/2019_11_24_16_42_s'
    folderName3 = './out_frames/2019_11_24_16_42_d'
    folderName4 = './out_frames/2019_11_24_16_42_n'

    videoWriter = cv2.VideoWriter(dump_root, fourcc, fps, (1920,1080))   #(1360,480)为视频大小


    frames=[]

    folderName1 = Path(folderName1)
    folderName2 = Path(folderName2)
    folderName3 = Path(folderName3)
    folderName4 = Path(folderName4)

    if folderName1.exists()==False :
        print('folder no exist')
        return
    if folderName2.exists()==False :
        print('folder no exist')
        return
    if folderName3.exists()==False:
        print('folder no exist')
        return
    if folderName4.exists()==False:
        print('folder no exist')
        return

    files1 = folderName1.files('*.{}'.format('png'))
    files1.sort()
    files2 = folderName2.files('*.{}'.format('png'))
    files2.sort()
    files3 = folderName3.files('*.{}'.format('png'))
    files3.sort()
    files4 = folderName4.files('*.{}'.format('png'))
    files4.sort()
    for img_p1,img_p2,img_p3,img_p4 in zip( files1,files2,files3,files4):

        img1 = cv2.imread(img_p1)#
        img2 = cv2.imread(img_p2)
        img3 = cv2.imread(img_p3)
        img4 = cv2.imread(img_p4)

        img_u = np.concatenate([img1,img2],axis=1)
        img_d = np.concatenate([img3,img4],axis=1)
        img = np.concatenate([img_u,img_d],axis=0)
        img = cv2.resize(img,(0,0),fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)

    #    cv2.imshow('img', img12)
    #    cv2.waitKey(1000/int(fps))
        videoWriter.write(img)
    videoWriter.release()
if __name__=='__main__':
    main()
    print('ok')
