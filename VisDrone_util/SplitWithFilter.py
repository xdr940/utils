
from path import Path
from random import shuffle
import numpy as np
from options import SplitWithFilter_opts
from utils import PhotometricErr,list_remove
import matplotlib.pyplot as plt
from multiprocessing import Pool




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
    seqs_p = dataset_path.dirs()
    seqs_p.sort()#



    photometric_errs=[]
    p=Pool(processes=opt.num_workers)
    num_imgs=0
    for seq_p in seqs_p:
        num_imgs+=len(seq_p.files())
    num_seqs = len(seqs_p)
    print('-> total {} sequences, {}imgs '.format(num_seqs,num_imgs))
    step = max(opt.frame_idxs)
    for seq_p in seqs_p:
        print(seq_p)
        files = seq_p.files()
        files.sort()

        photometric_err = PhotometricErr(paths=files,pool=p,batch_size=opt.batch_size,step=step)
        photometric_err = np.concatenate([photometric_err,-np.ones(step)])
        print(photometric_err.shape)
        print(photometric_err)
        photometric_errs.append(photometric_err)
        photometric_err = np.array(photometric_err)

        np.save(photometric_err_dir/str(seq_p.stem)+'.npy',photometric_err)
    p.close()






def VsdSeqSelect(opt):
    '''
    根据npy的大小选择合适的frame, 过小的就认为相机基本静止, 放弃选择.
    :param opt:
    :return:
    '''
    shows=False
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
    select_vec =[]
    mean_npy=[]
    for npy_p in npys_p:
        npy = np.load(npy_p)
        npys.append(npy)
        print(npy_p.stem)
        mean_npy.append(npy.mean())

        npy_bool  = ((npy > opt.photometric_threshold[0])*( npy < opt.photometric_threshold[1]))

        #npy_bool = list(npy_bool)
        select_vec.append(npy_bool)
    print("---\n")
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


    for real_seq_p ,select_idx in zip(real_seqs_p,select_vec):
        full_files_real_paths = real_seq_p.files()
        full_files_real_paths.sort()
        full_len = len(full_files_real_paths)

        print(real_seq_p.stem)
        if real_seq_p.stem =='uav0000240_00001_s':
            pass
        #real_paths = StartEnd_remove(select_idx,full_len,frame_interval=opt.frame_idxs)#掐头去尾
        real_paths = list_remove(full_files_real_paths,select_idx,frame_interval=opt.frame_idxs)#photometric filtering

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

    plt.plot(mean_npy,"r-o")
    plt.show()







if  __name__ == '__main__':
    options = SplitWithFilter_opts().args()
    VSD_PhotometricErrNpy_Output(options)
    #VsdSeqSelect(options)



