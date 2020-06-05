
from path import Path
from random import shuffle
import argparse
from tqdm import  tqdm


def parse_args():
    parser = argparse.ArgumentParser(
        description='Simple testing funtion for Monodepthv2 models.')

    parser.add_argument('--dataset_path', type=str,default='/home/roit/datasets/VisDrone2',help='path to a test image or folder of images')
    parser.add_argument("--splits",default='visdrone_lite_full',help='output_dir')
    parser.add_argument('--out_path', type=str,default=None,help='path to a test image or folder of images')
    parser.add_argument("--num",default=None,type=str)
    parser.add_argument("--proportion",default=[0.16,0.016,0.004],help="train, val, test")
    parser.add_argument("--frame_ids",default=[-3,0,3],help="frame interval settings")

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
def generate_vsd(args):
    '''

    :param args:
    :return:none , output is  a dir includes 3 .txt files
    '''
    [train_,val_,test_] = args.proportion

    if train_+val_+test_-1.>0.01:#delta
        print('erro')
        return


    dataset_path = Path(args.dataset_path)
    out_dir = Path(".")/args.splits
    out_dir.mkdir_p()
    train_txt_p = out_dir/'train_files.txt'
    val_txt_p = out_dir/'val_files.txt'
    test_txt_p = out_dir/'test_files.txt'

    sequences = dataset_path.dirs()
    sequences.sort()#
    real_list=[]#

    if args.frame_ids[0] +args.frame_ids[-1]==0:
        start_end = int(abs(args.frame_ids[0]))
    for item in tqdm(sequences):
        files = item.files()
        files.sort()
        real_list+=files#[start_end:-start_end]

    rel_list = []
    for item in tqdm(real_list):
        rel_list.append(item.relpath(dataset_path).strip('.jpg'))

    del(real_list)




    shuffle(rel_list)

    num = len(rel_list)

    train_bound = int(num *args.proportion[0])
    val_bound = int(num *args.proportion[1])+train_bound
    test_bound = int(num *args.proportion[2])+val_bound

    writelines(rel_list[:train_bound],train_txt_p)
    writelines(rel_list[train_bound:val_bound],val_txt_p)
    writelines(rel_list[val_bound:test_bound],test_txt_p)

    print('ok')











if  __name__ == '__main__':
    options = parse_args()
    generate_vsd(options)