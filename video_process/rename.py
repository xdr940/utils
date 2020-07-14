from path import Path
import os
from  tqdm import tqdm


#path = Path('/home/roit/datasets/MC/10001000/p3/normal')
#path = '/home/roit/datasets/Binjiang/00082'
path = '/media/roit/greenp2/output_dir/06021108_10001000p3'
path = Path(path)
files = path.files()
files.sort()
ext = files[0].ext
for idx,item in tqdm(enumerate(files)):
    cmd = 'mv '+ str(item)+' ' +item.parent/('{:04}'+ext).format(idx+1)
    os.system(cmd)
