from path import Path
import matplotlib.pyplot as plt
import cv2
root = Path('/home/roit/datasets/mctest/screenshots')
ext ='png'


def main():
    dirs = root.dirs()
    len = dirs.__len__()
    name_dis_gray=[]
    fmt=['r','g','b','y','m','c','k']

    for i in range(len):
        name_dis_gray.append(read_dir(dirs[i]))


    for i in range(len):
        plt.plot(name_dis_gray[i][1],name_dis_gray[i][2],fmt[i],label=name_dis_gray[i][0])

    plt.ylabel('gray(1)')
    plt.xlabel('distances(m)')
    plt.legend()
    plt.show()

    print('ok')

def read_dir(path):
    name = path.stem
    files = path.files('*.{}'.format(ext))
    files.sort()
    img=cv2.imread(files[0])
    h,w=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY).shape
    gray=[]
    dis=[]
    for img_p in files:
        img = cv2.imread(img_p)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        #img = plt.imread(img_p)
        gray.append(img[int(h/2)+1,int(w/2)+1])
        dis.append(float(img_p.stem))

    return (name,dis,gray)
if __name__ == '__main__':
    main()