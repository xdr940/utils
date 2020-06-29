
import numpy as np
from utils import load_poses_from_txt,matrix2dof

import matplotlib as mpl
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation  # 动图的核心函数
from  matplotlib.colors import  BoundaryNorm
from  random import random
import matplotlib.pyplot as plt
from math import pi,cos,sin
import argparse
parser = argparse.ArgumentParser(description='KITTI evaluation')
parser.add_argument("--input_json",
                    default="./timelines.json"
                    )
parser.add_argument("--out_dir",default='out_dir')
parser.add_argument('--interval_dynamic_draw',default=5)

args = parser.parse_args()


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
#def pm18021(roll): #-180~180 --> 0~1
#    return roll/360 +0.5

def draw_6dof(poses_6dof):#poses_6dof
    poses_np = np.array(poses_6dof)#200,6
    roll = poses_np[:,2]
    roll =roll/360 +0.5 #[-180,180]-->[0,1] for colormap 处理

    position = poses_np[:,2:]#xyz
    orient_vec=[]
    for item in poses_6dof:
        orient_vec.append(deg2vec(item[0], item[1]))
    orient_vec = np.array(orient_vec)


    fig = plt.figure(figsize=[8, 5])
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal', adjustable='box')
    # ax.yaxis.set_ticks_position('top')
    ax.invert_xaxis()  # x 反方向
    ax.set_xlabel('X')  # X不变
    ax.set_ylabel('z')  # yz交换
    ax.set_zlabel('y')  #
    plt.axis('equal')
    # plt.title('trajectory 80_00_1')
    mycmap = plt.get_cmap('hsv', 100)
    mynorm = mpl.colors.Normalize(vmin=-180, vmax=180)

    # 绘制起点,终点,其他点
    ax.scatter(position[0, 0], position[0, 2], position[0, 1], c='r')  # 起点绿色
    ax.scatter(position[-1, 0], position[-1, 2], position[-1, 1], c='g')  # 终点黄色
    # ax.plot(position[:, 0], position[:, 2], position[:, 1], 'k-')

    i = 0
    # 绘制箭头
    while i < position.shape[0]:
        if i % 5 == 0:
            # 划黑线
            ax.plot(position[:i, 0], position[:i, 2], position[:i, 1], 'k-')

            ax.quiver(position[i, 0], position[i, 2], position[i, 1],
                      orient_vec[i, 0], orient_vec[i, 2], orient_vec[i, 1],
                      color=mycmap(roll[i]), norm=mynorm, length=3)
        i += 1

    fig, ax2 = plt.subplots(figsize=(1.5, 4))
    fig.subplots_adjust(right=0.4)

    # color bar
    cb = mpl.colorbar.ColorbarBase(ax2,
                                   cmap=mycmap,
                                   norm=mynorm,
                                   orientation='vertical')

    cb.set_label('roll angle (degree)')

    plt.show()
def draw_3dof(poses_6dof):#poses_6dof
    poses_np = np.array(poses_6dof)#200,6
    position = poses_np[:,3:]#xyz

    fig = plt.figure(figsize=[8, 5])
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal', adjustable='box')
    ax.invert_xaxis()  # x 反方向
    ax.set_xlabel('X')  # X不变
    ax.set_ylabel('z')  # yz交换
    ax.set_zlabel('y')  #
    plt.axis('equal')

    i = 0

    #while i < position.shape[0]:
    ax.plot(position[:, 0], position[:, 2], position[:, 1], 'k-')
    #    i+=1

    # 绘制起点,终点,其他点
    ax.scatter(position[0, 0], position[0, 2], position[0, 1], c='r')  # 起点绿色
    ax.scatter(position[-1, 0], position[-1, 2], position[-1, 1], c='g')  # 终点黄色



    plt.show()
def draw_2dof(poses_6dof):#poses_6dof
    poses_np = np.array(poses_6dof)#200,6
    position = poses_np[:,3:]#xyz

    fig = plt.figure(figsize=[8, 5])
    ax = fig.gca()
    ax.set_aspect('equal', adjustable='box')
    ax.invert_xaxis()  # x 反方向
    ax.set_xlabel('x')  # X不变
    ax.set_ylabel('z')  # yz交换
    plt.axis('equal')

    i = 0

    #while i < position.shape[0]:
    ax.plot(position[:, 0], position[:, 2], 'k-')
    #    i+=1

    # 绘制起点,终点,其他点
    ax.scatter(position[0, 0], position[0, 2], position[0, 1], c='r')  # 起点绿色
    ax.scatter(position[-1, 0], position[-1, 2], position[-1, 1], c='g')  # 终点黄色



    plt.show()


def dynamic_draw_6dof(poses_6dof):
    def update(i):
        label = 'timestep {0}'.format(i)
        #print(label)
        # 更新直线和x轴（用一个新的x轴的标签）。
        # 用元组（Tuple）的形式返回在这一帧要被重新绘图的物体
        ax.plot(position[:i, 0], position[:i, 2], position[:i, 1], 'k-')

        ax.quiver(position[i, 0], position[i, 2], position[i, 1],
                  orient_vec[i, 0], orient_vec[i, 2], orient_vec[i, 1],
                  color=mycmap(roll[i]), norm=mynorm)

        return fig, ax


    interval = args.interval_dynamic_draw
    #减少点数
    poses_6dof_sub = []
    cnt=0
    for pose in poses_6dof:
        if cnt%interval==0:
            poses_6dof_sub.append(pose)
        cnt+=1
    poses_6dof = poses_6dof_sub
    poses_6dof_np = np.array(poses_6dof)

    orient_vec = []
    roll = []
    for item in poses_6dof:
        orient_vec.append(deg2vec(item[0], item[1]))
        roll.append(item[2])
    # draw

    position = poses_6dof_np[:,2:]
    orient_vec = np.array(orient_vec)
    roll = np.array(roll)
    # roll =(roll - roll.min())/(roll.max() - roll.min())
    roll = roll / 360 + 0.5  # [-180,180]-->[0,1] for colormap 处理


    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal', adjustable='box')
    # ax.yaxis.set_ticks_position('top')
    ax.invert_xaxis()  # x 反方向
    ax.set_xlabel('X')  # X不变
    ax.set_ylabel('z')  # yz交换
    ax.set_zlabel('y')  #
    plt.axis('equal')

    ax.scatter(position[0, 0], position[0, 2], position[0, 1], c='r')  # 起点绿色
    ax.scatter(position[-1, 0], position[-1, 2], position[-1, 1], c='g')  # 终点黄色
    plt.title('Aircraft Ego-motion')
    mycmap = plt.get_cmap('hsv', 100)
    mynorm = mpl.colors.Normalize(vmin=-180, vmax=180)



    #save
    anim = FuncAnimation(fig, update, frames=range(0, position.shape[0]), interval=175)
    anim.save('./line.gif', dpi=80, writer='imagemagick')


    pass

def add_draw(fliename):
    """
    根据文件内容变化绘制点
    :param fliename:
    :return:
    """

    pass


if __name__ == '__main__':
    poses = load_poses_from_txt('./out_dir/p1_.txt')
    poses_6dof = matrix2dof(poses)
    #draw
    draw_2dof(poses_6dof)
    #draw_6dof(poses_6dof)
    #dynamic_draw_6dof(poses_6dof)
