
import time
import linecache
file_p = "pipline.txt"


cnt=1
while True:
    linecache.checkcache(file_p)
    s = linecache.getline(file_p,cnt)
    print(s)
    time.sleep(0.8)
    cnt+=1
