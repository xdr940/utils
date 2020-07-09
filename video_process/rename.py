from path import Path
import os
from  tqdm import tqdm


#path = Path('/home/roit/datasets/MC/10001000/p3/normal')
path = Path('/home/roit/datasets/Binjiang/0007')
files = path.files()
files.sort()
ext = files[0].ext
for idx,item in tqdm(enumerate(files)):
    cmd = 'mv '+ str(item)+' ' +item.parent/('{:04}'+ext).format(idx+1)
    os.system(cmd)
