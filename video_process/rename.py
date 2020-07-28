from path import Path
import os
from  tqdm import tqdm
import cv2

#path = Path('/home/roit/datasets/MC/10001000/p3/normal')
#path = '/home/roit/datasets/Binjiang/00082'

def rename():
    path = '/home/roit/testouts/vsd/ours'
    path = Path(path)
    files = path.files()
    files.sort()
    ext = files[0].ext
    for idx, item in tqdm(enumerate(files)):
        cmd = 'mv ' + str(item) + ' ' + item.parent / ('{:04}' + ext).format(idx + 1)
        os.system(cmd)


def resize():
    path = '/home/roit/testouts/vsd/zhou'
    path = Path(path)
    files = path.files()
    files.sort()
    ext = files[0].ext
    for item in tqdm(files):
        img = cv2.imread(item)
        img = cv2.resize(img,(480,270))

        cv2.imwrite(item,img)


if __name__ == '__main__':
    #rename()
    resize()