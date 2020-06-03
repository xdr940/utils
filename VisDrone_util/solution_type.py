#visdrone_lite 有多种分辨率的图像， 统计下
from tqdm import  tqdm
from options import VisDrone
import pandas as pd
from path import  Path
import  cv2
import  os
def main(opt):
    dataset_path = Path(opt.dataset_path)
    dirs = dataset_path.dirs()
    seqs = []
    for dir in dirs :
        temp= dir/'sequences'
        seqs+=temp.dirs()

    tab = []
    for seq in seqs:
        base = str(seq).replace(opt.dataset_path+'/','')
        up_name,_,seq_name = base.split('/')

        img_p = seq.files()[0]
        img = cv2.imread(img_p)
        h,w,c = img.shape
        solution = (h,w)
        num_frame = len(seq.files())
        item = [seq_name,up_name,solution,num_frame]
        tab.append(item)

    df = pd.DataFrame(tab,columns=['seq_name','parent_name','solution','num_frame'])
    df.to_csv('visdrone_desc.csv',index=None)

def op(csv):
    df = pd.read_csv(csv)
    df = df.sort_values(by='solution',ascending=True)



    df.to_csv('sort.csv',index=None)
def statistic(csv):
    df = pd.read_csv(csv)
    solution_frames = {}
    solution_seqs = {}
    for index,row in df.iterrows():
        if row['solution'] not in solution_seqs.keys():
            solution_seqs[row['solution']] = 1
        else:
            solution_seqs[row['solution']] += 1

        if row['solution'] not in solution_frames.keys():
            solution_frames[row['solution']] = row['num_frame']
        else:
            solution_frames[row['solution']] += row['num_frame']

    print(solution_seqs)
    print(solution_frames)

def re_struct():
    data_path = Path(opt.dataset_path)
    out_path = Path(opt.dataset_path)
    df = pd.read_csv('sort.csv')
    for index, row in tqdm(df.iterrows()):
        if row['solution']=='(1071, 1904)':
            cmd = 'mv '+ str(data_path/row['parent_name']/'sequences'/row['seq_name'])+ '  '+ str(out_path)
            os.system(cmd)
    print('ok')


if __name__ == '__main__':
    parser = VisDrone()
    opt = parser.parse()
    #main(opt)
    #op('visdrone_desc.csv')
    #static('sort.csv')
    re_struct()
