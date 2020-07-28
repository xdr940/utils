
from path import Path
from random import shuffle
import argparse
import numpy as np
from tqdm import  tqdm
from utils import PhotometricErr,list_remove,StartEnd_remove
import matplotlib.pyplot as plt
from multiprocessing import Pool

def parse_opt():
    parser = argparse.ArgumentParser(
        description='Simple testing funtion for Monodepthv2 models.')

    parser.add_argument('--dataset_path', type=str,default='/970evo/home/roit/datasets/VisDrone2',help='path to a test image or folder of images')
    parser.add_argument("--splits",default='visdrone',help='output_dir')
    parser.add_argument('--out_path', type=str,default=None,help='path to a test image or folder of images')
    parser.add_argument("--num",default=None,type=str)
    parser.add_argument("--proportion",default=[0.9,0.05,0.05],help="train, val, test")
    parser.add_argument("--num_workers",default=12)
    parser.add_argument("--batch_size",default=48)
    parser.add_argument("--photometric_threshold",default=0.12)
    parser.add_argument('--frame_idxs',default=[-3,0,3],help="frame interval settings")#由于有photometric err 控制了, 所以可以将frame interval 减小
    parser.add_argument("--photometric_err_dir",default='./photometric_err')
    parser.add_argument("--ext",default='.jpg')





    parser.add_argument("--out_name",default=None)

    return parser.parse_args()


def writelines(list,path):
    lenth = len(list)
    with open(path,'w') as f:
        for i in range(lenth):
            if i == lenth-1:
                f.writelines(str(list[i]))
            else:
                f.writelines(str(list[i])+'\n')

def readlines(filename):
    """Read all the lines in a text file and return as a list
    """
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    return lines
def VSD_PhotometricErrNpy_Output(opt):
    '''
     Output photometric diff(npy files) of img files in each seqs , like follows:

         dir
           seq1.npy# shape = [len (img_files) -1,]
           seq2.npy
           ...

    :param opt:
    :return:none
    '''


    #
    photometric_err_dir =Path(opt.photometric_err_dir)
    photometric_err_dir.mkdir_p()


    #
    dataset_path = Path(opt.dataset_path)
    real_sequences_p = dataset_path.dirs()
    real_sequences_p.sort()#



    photometric_errs=[]
    p=Pool(processes=opt.num_workers)
    print('-> total {} sequences '.format(len(real_sequences_p)))
    for real_seq in tqdm(real_sequences_p):
        real_files = real_seq.files()
        real_files.sort()

        photometric_err = PhotometricErr(paths=real_files,pool=p,batch_size=opt.batch_size)
        photometric_errs.append(photometric_err)
        photometric_err = np.array(photometric_err)

        np.save(photometric_err_dir/str(real_seq.stem)+'.npy',photometric_err)
    p.close()






def VsdSeqSelect(opt):
    '''
    根据npy的大小选择合适的frame, 过小的就认为相机基本静止, 放弃选择.
    :param opt:
    :return:
    '''
    shows=True
    [train_, val_, test_] = opt.proportion

    if train_ + val_ + test_ - 1. > 0.01:  # delta
        print('erro in split proportion')
        return

    out_dir = Path(".") / opt.splits
    out_dir.mkdir_p()
    train_txt_p = out_dir / 'train_files.txt'
    val_txt_p = out_dir / 'val_files.txt'
    test_txt_p = out_dir / 'test_files.txt'




    photometric_err_dir = Path(opt.photometric_err_dir)
    npys_p = photometric_err_dir.files()
    npys_p.sort()
    npys=[]
    photometric_errs =[]
    for npy_p in npys_p:
        npy = np.load(npy_p)
        npys.append(npy)
        npy_bool  = np.uint8(npy > opt.photometric_threshold)

        ls = list(npy_bool)
        photometric_errs.append(ls)

    if shows:
        ids = [0,20,40]
        legends = [npys_p[id].stem for id in ids]
        curvs = [npys[id] for id in ids]
        for curv in curvs:
            plt.plot(curv)
        plt.xlabel('frame_num',fontsize=10)
        plt.ylabel('photometric error/ rho',fontsize=10)
        plt.plot(0.15*np.ones([1000]),'r-.')
        plt.plot(0.3*np.ones([1000]),'b-.')
        plt.legend(legends, fontsize=10,loc = 'upper right')

    dataset_path = Path(opt.dataset_path)
    real_seqs_p = dataset_path.dirs()
    real_seqs_p.sort()  #


    rel_paths_seqs =[]


    for real_seq_p ,select_idx in zip(real_seqs_p,photometric_errs):
        full_files_real_paths = real_seq_p.files()
        full_files_real_paths.sort()
        full_len = len(full_files_real_paths)

        print(real_seq_p.stem)
        real_paths = list_remove(full_files_real_paths,select_idx)#photometric filtering
        real_paths = StartEnd_remove(real_paths,full_len,frame_interval=opt.frame_idxs[2])

        rel_paths_seq = [real_path.relpath(opt.dataset_path).strip(opt.ext) for real_path in real_paths]
        print('->full frames:{}, filtered frames:{}'.format(full_len,len(rel_paths_seq)))

        rel_paths_seqs+=rel_paths_seq

    print('->final files: {}'.format(len(rel_paths_seqs)))



    #rel_paths_seqs split as .txt files
    shuffle(rel_paths_seqs)
    num = len(rel_paths_seqs)
    train_bound = int(num *opt.proportion[0])
    val_bound = int(num *opt.proportion[1])+train_bound
    test_bound = int(num *opt.proportion[2])+val_bound

    writelines(rel_paths_seqs[:train_bound],train_txt_p)
    writelines(rel_paths_seqs[train_bound:val_bound],val_txt_p)
    writelines(rel_paths_seqs[val_bound:test_bound],test_txt_p)








if  __name__ == '__main__':
    options = parse_opt()
    #VSD_PhotometricErrNpy_Output(options)
    VsdSeqSelect(options)



