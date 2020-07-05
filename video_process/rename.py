from path import Path
import os


path = Path('/home/roit/datasets/Binjiang/0001')
files = path.files()
files.sort()
for idx,item in enumerate(files):
    cmd = 'mv '+ str(item)+' ' +item.parent/'{:04}.jpg'.format(idx+1)
    os.system(cmd)
