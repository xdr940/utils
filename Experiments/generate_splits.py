
#generate texte.file
from opts import parse_args_generate_splits as parse_args
from path import Path
from random import random
import os
def writelines(list,path):
    lenth = len(list)
    with open(path,'w') as f:
        for i in range(lenth):
            if i == lenth-1:
                f.writelines(list[i])
            else:
                f.writelines(list[i]+'\n')

def readlines(filename):
    """Read all the lines in a text file and return as a list
    """
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    return lines
def generate_mc(args):
    '''

    :param args:
    :return:none , output is  a dir includes 3 .txt files
    '''
    [train_,val_,test_] = args.proportion

    if train_+val_+test_-1.>0.01:#delta
        print('erro')
        return


    file_path = Path(args.dataset_path)

    out_dir = Path(args.txt_style + "_splits")
    out_dir.mkdir_p()
    train_txt_p = out_dir/'train_files.txt'
    val_txt_p = out_dir/'val_files.txt'
    test_txt_p = out_dir/'test_files.txt'




    return_list=[]
    i = 0
    if args.txt_style =='mc':
        dirs = file_path.dirs()
        dirs.sort()
    elif args.txt_style == 'visdrone':
        dirs = (file_path / 'sequences').dirs()

    while(i<args.num):

        sq_idx = int(random()*len(dirs))

        s = dirs[sq_idx].stem+' '
        if args.txt_style=='mc':
            frames = (dirs[sq_idx]/'img').files()
        elif args.txt_style == 'visdrone':
            frames = dirs[sq_idx].files()
        frames.sort()
        frame_idx = int(random()*len(frames))
        # 为了前一阵后一阵都能取到
        if frame_idx<2:
            frame_idx=2
        if frame_idx >len(frames)-2:
            frame_idx = len(frames)-2


        s+=frames[frame_idx].stem
        if frames[frame_idx].stem =='0000001':
            print('cao!')
        if not s in return_list:
            return_list.append(s)
            i+=1
    lenth = len(return_list)


    train_ = int(train_*lenth)
    val_ = int(val_*lenth) +train_
    test_ = int(test_*lenth)+val_


    writelines(return_list[:train_],train_txt_p)
    writelines(return_list[train_:val_],val_txt_p)
    writelines(return_list[val_:],test_txt_p)



if  __name__ == '__main__':
    options = parse_args()
    generate_mc(options)