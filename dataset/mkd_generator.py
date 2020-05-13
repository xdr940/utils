from path import Path
import argparse
parser = argparse.ArgumentParser(description="Monodepthv2 options")

parser.add_argument("--dirs",
                    help="sub dirs processed",
                    default="/home/roit/datasets/kitti/2011_09_30")
opt = parser.parse_args()



def main():
    root = Path(opt.dirs)
    dirs = root.dirs()
    dirs.sort()
    idxs=[]
    names=[]
    fig_paths=[]
    others=[]

    for (idx,dir) in zip( range(len(dirs)),dirs):
        idxs.append(idx)
        names.append(dir.stem)
        fig_paths.append("[img](./{}/{}/image_02/data/0000000000.png)".format(root.stem,dir.stem))
        others.append('--')
    lines = []
    for idx,name,fig_path,other in zip(idxs,names,fig_paths,others):
        lines.append("|"+"{:02d}".format(idx)+"|"+name+"|"+fig_path+"|"+other+"|")
    for line in lines:
        print(line)
if __name__ =="__main__":
    main()

