from  utils import  readlines,write_as_lines
from CatmulRom.catmul import CatmulRom
from  path import  Path
import numpy as np

import matplotlib.pyplot as plt
from math import *
from read_timelines import  json2txt
from  matplotlib.colors import  BoundaryNorm
from  random import random
import matplotlib as mpl
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import Axes3D

def deg2vec(pitch,yaw):
    '''
        x = rsin(phi)cos(theta)
        y = rsin(phi)sin(theta)
        z = rcos(phi)


        phi -- pi/2 --pitch
        theta --> pi/2 --yaw
        z --> y
        x --> x
        y --> z

        x = r *sin(pi/2+pitch)*cos(pi/2+yaw)
        z = r* sin(pi/2+pitch)*sin(pi/2+yaw)

        y = r*cos(pi/2+pitch)

    :param pitch:
    :param yaw:
    :return:
    '''
    #degra 2 rad
    #pitch%=360
    #yaw%=360
    pitch_r = pitch/360 *2*pi
    yaw_r = yaw/360 *2*pi
    r = 10
    x = r * sin(pi / 2 + pitch_r) * cos(pi / 2 + yaw_r)
    z = r * sin(pi / 2 + pitch_r) * sin(pi / 2 + yaw_r)

    y = r * cos(pi / 2 + pitch_r)

    ret = [x,y,z]
    '''
    i=0
    while i< len(ret):
        if ret[i]>0.99:
            ret[i] =1
        elif ret[i]<-0.99:
            ret[i]=-1
        elif ret[i]<0.001 and ret[i]> -0.001:
            ret[i]=0
        i+=1
    '''
    return ret
def pm18021(roll): #-180~180 --> 0~1
    return roll/360 +0.5


def draw(position,rotation):
    '''
        2 list with same shape
    :param position:
    :param rotation:
    :return:
    '''
    orient_vec = []
    roll = []
    for item in rotation:
        orient_vec.append(deg2vec(item[0], item[1]))
        roll.append(item[2])
    # draw

    position = np.array(position)
    orient_vec = np.array(orient_vec)
    roll = np.array(roll)
    #roll =(roll - roll.min())/(roll.max() - roll.min())
    roll =roll/360 +0.5 #[-180,180]-->[0,1] for colormap 处理

    c = np.array([1.,0,0,1]).reshape([1,4])
    roll4= np.expand_dims(roll,axis=1)@c

    c = np.ones([200,4])

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal', adjustable='box')
    # ax.yaxis.set_ticks_position('top')
    ax.invert_xaxis()  # x 反方向
    ax.set_xlabel('X')  # X不变
    ax.set_ylabel('z')  # yz交换
    ax.set_zlabel('y')  #
    plt.axis('equal')

    ax.scatter(position[0, 0], position[0, 2], position[0, 1],c='r')#起点绿色
    ax.scatter(position[-1, 0], position[-1, 2], position[-1, 1],c='g')#终点黄色
    ax.plot(position[:, 0], position[:, 2], position[:, 1], 'k-')
    plt.title('trajectory 80_00_1')
    mycmap = plt.get_cmap('hsv',100)
    mynorm = mpl.colors.Normalize(vmin = -180,vmax=180)

    i =0
    while i< position.shape[0]:
        if i%5==0:
            ax.quiver(position[i, 0], position[i, 2], position[i, 1],
                  orient_vec[i, 0], orient_vec[i, 2], orient_vec[i, 1],
                  color = mycmap(roll[i]),norm = mynorm)
        i+=1


    fig,ax2 = plt.subplots(figsize=(1.5,4))
    fig.subplots_adjust(right=0.4)
    cb = mpl.colorbar.ColorbarBase(ax2,
                                   cmap=mycmap,
                                   norm=mynorm,
                                   orientation='vertical')
    cb.set_label('roll angle (degree)')

    plt.show()
    print('ok')

def interpolaration(path):
    '''
        读取txt 然后进行插值， 并返回list
    :param path:
    :return:
    '''
    timelines = readlines(path)
    out_p = path.stem+'_.txt'
    time = []
    x = []
    y = []
    z = []

    pitch = []
    roll = []
    yaw = []
    no = []
    for item in timelines:

        time.append(item[0] )# time
        pitch.append(item[1])
        yaw.append(item[2])
        roll.append(item[3])

        x.append(item[4])
        y.append(item[5])
        z.append(item[6])

    position = []
    rotation = []
    for item in zip(x, y, z):
        position.append(item)
    for item in zip(pitch, yaw, roll):
        rotation.append(item)

    ac = CatmulRom(alpha=0.5, n_step=50)

    position = ac.run3d(position)
    rotation = ac.run3d(rotation)
    cnt=0
    with open(out_p,'w') as f:
        f.writelines('#time,pitch,yaw,roll,x,y,z')
        for pos,rot in zip(position,rotation):
            string = '\n' + str(cnt*100) + ',' \
                     + str(rot[0])+','+str(rot[1])+','+ str(rot[2])+','\
                     +str(pos[0])+','+str(pos[1])+','+str(pos[2])
            f.writelines(string)
            cnt+=1

    #return position,rotation
    return out_p

def main():
    IsDraw = True
    p = Path('./02_00.json')
    f0s = json2txt(p)
    cnt =1
    trajectories = []
    for f in f0s:
        if cnt >3:
            break
        f = Path(f)
        f2 = interpolaration(f)# T1.txt 2 T1_.txt
        trajectories.append(readlines(f2))
        cnt+=1
    if IsDraw:#光画第一个 trajectory
        position = []
        rotation = []
        for item in trajectories[0]:
            rotation.append([item[1], item[2], item[3]])
            position.append([item[4], item[5], item[6]])
        draw(position, rotation)

def main2():
    pass


if __name__ == '__main__':
    main()

    #a= plt.cm.seismic

    #print('ok')

