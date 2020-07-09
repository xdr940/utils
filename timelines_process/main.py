
from path import Path
import argparse
import numpy as np
import json
import math
from CatmulRom.catmul import CatmulRom
from  math import cos,acos,sin,asin,pi
parser = argparse.ArgumentParser(description='KITTI evaluation')
parser.add_argument("--input_json",
                    default="./data/10001000.json"
                    )
parser.add_argument("--out_dir",default=None)


args = parser.parse_args()

#json format: yaw pitch roll x, y, z
#_6dof formate pitch yaw roll x,y,z
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




class TimeLine():
    def __init__(self,options):
        self.input_json = Path(options.input_json)

        if args.out_dir:
            self.out_dir = Path(args.out_dir)
        else:
           self.out_dir = Path(self.input_json.stem + '_poses')
        self.out_dir.mkdir_p()


    def readjson(self,path):
        f = open(path, encoding='utf-8')
        content = f.read()
        dict = json.loads(content)
        return dict

    def interpolaration(self,key_frames_list):
        '''
            读取txt 然后进行插值， 并返回list
        :param path: "timelines_p1.txt"
        :return:
        '''
        #timelines = readlines(path)
        #out_p = path.stem+'_.txt'
        time = []
        x = []
        y = []
        z = []

        pitch = []
        roll = []
        yaw = []
        no = []
        cnt=0
        for item in key_frames_list:
            if cnt==len(key_frames_list)-1:
                pass
            time.append(item[0] )# time
            pitch.append(item[1])
            yaw.append(item[2])
            roll.append(item[3])

            x.append(item[4])
            y.append(item[5])
            z.append(item[6])
            cnt+=1

        position = []
        rotation = []
        for item in zip(x, y, z):
            position.append(item)
        for item in zip(pitch, yaw, roll):
            rotation.append(item)

        ac = CatmulRom(alpha=0.5, n_step=50)

        position = ac.run3d(position)
        rotation = ac.run3d(rotation)
        poses = [rot + pos for rot,pos in zip(rotation,position)]
        #np format
        #position = np.array(position)
        #rotation = np.array(rotation)
        #poses = np.concatenate([rotation,position],axis=1)

        return ['pitch','yaw','roll','x','y','z'], poses

    def json2trajs(self,json_path):
        pass
        print('ok')

    def format2list(self,path_name):
        # path_name is a list
        num_frames = len(path_name[0]['keyframes'])
        traj_formated_dict = []
        frame = {}
        for i in range(num_frames):
            # frame['no'] = '{:07d}'.format(i)
            # frame['no'] = i

            frame['time'] = path_name[1]['keyframes'][i]['time']
            frame['pitch'] = path_name[1]['keyframes'][i]['properties']['camera:rotation'][1]%90
            frame['yaw'] = path_name[1]['keyframes'][i]['properties']['camera:rotation'][0]%90
            frame['roll'] = path_name[1]['keyframes'][i]['properties']['camera:rotation'][2]%90

            frame['x'] = path_name[1]['keyframes'][i]['properties']['camera:position'][0]
            frame['y'] = path_name[1]['keyframes'][i]['properties']['camera:position'][1]
            frame['z'] = path_name[1]['keyframes'][i]['properties']['camera:position'][2]

            traj_formated_dict.append(frame.copy())

        key_frames = []
        for frame in traj_formated_dict:
            frame_ = list(frame.values())
            key_frames.append(frame_)


        return key_frames
    def dof2matrix(self,poses):
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
    def matrix2dof(self,poses):
        poses_6dof =[]
        for item in poses:
            T11,T12,T13,T14,T21,T22,T23,T24,T31,T32,T33,T34 = item
            pitch = acos(T33)
            roll = acos((-T23)/sin(pitch))
            yaw = acos(T32/sin(pitch))
            x = T14
            y=T24
            z=T34
            poses_6dof.append([pitch,yaw,roll,x,y,z])

        return poses_6dof






    def run(self):
        trajs = self.readjson(self.input_json)#读取原始json文件

        for traj_name in trajs:

            key_frames = self.format2list(trajs[traj_name])#第一次格式化


            names,poses_6dof = self.interpolaration(key_frames)
            poses_mat = self.dof2matrix(poses_6dof)#(n,3,4)


            save_as_txt(self.out_dir/traj_name+'_6dof.txt',poses_6dof,shape='6dof')
            save_as_txt(self.out_dir/traj_name+'_.txt',poses_mat)











if __name__ == '__main__':
    timeline = TimeLine(args)
    timeline.run()
