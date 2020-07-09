
import math
import json
import numpy as np
from  math import cos,acos,sin,asin,pi

def readlines(filename):
    """Read all the lines in a text file and return as a list
    """
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    i=0
    while(i<len(lines)):
        if lines[i][0]=='#':
            lines.pop(i)
            i-=1
        i+=1
    i=0
    ret =[]
    while(i<len(lines)):
        ret.append(lines[i].split(','))
        if len(ret[i])==1:
            ret[i] = float(ret[i][0])
        else:

            for j in range(len(ret[i])):
                ret[i][j] = float(ret[i][j])
        i+=1


    return ret


def readjson(path):
    f = open(path, encoding='utf-8')
    content = f.read()
    dict = json.loads(content)
    return  dict



    pass



def save_as_txt(filename,poses,shape='matrix'):
    #poses (n,3,4)
    with open(filename,'w') as f:
        for pose in poses:
            if shape=='matrix':
                #pose = pose.reshape([12])
                pose = str(pose).replace('\n',' ')
                f.writelines(pose[1:-1]+'\n')
            if shape =='6dof':
                pose = str(pose)
                f.writelines(pose[1:-1]+'\n')
def load_poses_from_txt(filename):
    poses=[]
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            pose = line.split()
            pose = [float(item) for item in pose]
            poses.append(pose)
        print('ok')

    return poses
def dof2matrix(poses):

        '''
        pitch, yaw, roll, x, y, z --> T11 T12 T13 T14 T21 T22 T23 T24 T31 T32 T33 T34
        :param poses:
        :return:
        '''

        def deg2raid(x):
            return x / 360 * math.pi

        poses_format =[]
        for pose in poses:
            pitch,yaw, roll, x, y, z = pose


            roll = deg2raid(roll)
            yaw = deg2raid(yaw)
            pitch = deg2raid(pitch)

            R_roll = [cos(roll),-sin(roll),0,
                    sin(roll),cos(roll),0,
                    0,             0,       1]
            R_pitch = [1,0,0,
                       0,cos(pitch),sin(pitch),
                       0,-sin(pitch),cos(pitch)]

            R_yaw = [cos(yaw),0,-sin(yaw),
                     0,1,0,
                     sin(yaw),0,cos(yaw)]

            R_roll = np.array(R_roll).reshape([3,3])
            R_yaw = np.array(R_yaw).reshape([3,3])
            R_pitch = np.array(R_pitch).reshape([3,3])

            R= R_roll@R_yaw@R_pitch
            t = np.array([x,y,z]).reshape([3,1])
            Rt = np.concatenate([R,t],axis=1)
            Rt = Rt.reshape(12)
            poses_format.append(Rt)

        return  poses_format

def matrix2dof(poses):
    poses_6dof =[]
    for item in poses:
        T11,T12,T13,T14,T21,T22,T23,T24,T31,T32,T33,T34 = item


        yaw = asin(T31)

        pitch = -asin(T32/(cos(yaw)))

        roll = asin(T21/cos(yaw))

        pitch =pitch/pi *360
        roll =roll/pi *360
        yaw =yaw/pi *360

        x = T14
        y=T24
        z=T34
        poses_6dof.append([pitch,yaw,roll,x,y,z])

    return poses_6dof