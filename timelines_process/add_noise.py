
from utils import load_poses_from_txt
import argparse
import numpy as np
parser = argparse.ArgumentParser(description='KITTI evaluation')
parser.add_argument("--input",
                    help="as kitti formate that 12 dof",
                    default="./10001000_poses/p1_.txt"
                    #default="./custom_vo/03_gt.txt"

                    )
parser.add_argument("--out_name",default='p1_noise.txt')
if __name__ == '__main__':

    args = parser.parse_args()

    poses = load_poses_from_txt(args.input)

    length = len(poses)
    dof = len(poses[0])

    poses_np  = np.concatenate(poses)

    poses_np.resize([length,dof])
    rand1 = np.random.rand(length)*2
    rand2 = np.random.rand(length)*2
    rand3 = np.random.rand(length)*2


    poses_np[:,3]+=rand1
    poses_np[:,7]+=rand2
    poses_np[:,11]+=rand3

    #poses_np[3]+=np.random.rand()#*50
    #poses_np[11]+=np.random.rand()#*50



    np.savetxt(args.out_name,poses_np, delimiter=' ', fmt='%1.8e')
    print('pok')
