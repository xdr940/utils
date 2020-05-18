
#generate texte.file
'''
    MC# od0
        0000#blocks od1
            00#path od2
                color
                depth
        0001


'''
from opts import parse_args_generate_splits as parse_args
from path import Path
import path
from random import random
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
def generate_mc(args):
    '''

    :param args:
    :return:none , output is  a dir includes 3 .txt files
    '''
    [train_,val_,test_] = args.proportion

    if train_+val_+test_-1.>0.01:#delta
        print('erro')
        return


    dataset_path = Path(args.dataset_path)

    out_dir = Path("mc_splits")
    out_dir.mkdir_p()
    train_txt_p = out_dir/'train_files.txt'
    val_txt_p = out_dir/'val_files.txt'
    test_txt_p = out_dir/'test_files.txt'

    dirs_o1 = dataset_path
    blocks = dirs_o1.dirs()
    blocks.sort()#blocks
    item_list=[]#

    for dirs_o2 in blocks:
        trajectories = dirs_o2.dirs()
        for trajectory in trajectories:
            imgs = (trajectory/'color').files()

            for p in imgs:
                #p = p.relpath(dataset_path).strip('.png')
                item_list.append(p)

            #depths = (trajectory/'depth').files()
            #depths.sort()

    idx_list=[]
    #for i in range(args.num):
    while(len(idx_list)<args.num):
        rand = int(random()*len(item_list))
        #rand=55
        temp = item_list[rand]
        frame_num  =int(temp.stem)
        if rand not in idx_list and frame_num >3 and frame_num+1 <len(temp.parent.files()):
            idx_list.append(rand)

    total_list = []

    for i in idx_list:
        total_list.append(item_list[i].relpath(dataset_path).strip('.png'))

    train_bound = int(args.num *args.proportion[0])
    val_bound = int(args.num *args.proportion[1])+train_bound
    test_bound = int(args.num *args.proportion[2])+val_bound

    writelines(total_list[:train_bound],train_txt_p)
    writelines(total_list[train_bound:val_bound],val_txt_p)
    writelines(total_list[val_bound:test_bound],test_txt_p)


    print('ok')











if  __name__ == '__main__':
    options = parse_args()
    generate_mc(options)