import seaborn as sns
import matplotlib.pyplot as plt
from path import Path
root = Path("./VSD")
import numpy as np
import pandas as pd


def npy2csv():
    npys=[
        "uav0000115_00606_s",#0
        "uav0000232_00960_s",#1
        "uav0000226_05370_s",#2
        "uav0000235_00001_s",#3
        "uav0000235_01032_s",#4
        "uav0000236_00001_s",#5
        "uav0000237_00001_s",#6
        "uav0000238_00001_s",#7 good
        "uav0000238_01280_s",#8
        "uav0000239_11136_s",#9
        "uav0000240_00001_s",#10 good
        "uav0000245_00001_s",#11
        "uav0000303_01250_s",#12
        "uav0000317_00000_s",#13 good
        "uav0000317_02945_s",#14
        "uav0000325_01656_s"#15


    ]
    tab=np.array([1,2])
    for idx,p in enumerate(npys):
        npy_p = root/(p+'.npy')
        npy = np.load(npy_p)[:-10]
        npy = np.expand_dims(npy,axis=1)
        name = np.ones_like(npy)*idx

        if idx==0:
            tab = np.concatenate([npy, name], axis=1)
            continue
        else:
            temp = np.concatenate([npy, name], axis=1)
            tab = np.concatenate([tab,temp])

    print(tab.shape)
    np.savetxt("scences.csv", tab, delimiter=',',fmt='%.3f')

def main():
    sns.set(font_scale=1.8)
    frame = pd.read_csv("scences.csv",names=['Backward Photometric Error','Scenes'])


    sns.boxplot(x ='Scenes',y='Backward Photometric Error',data=frame)


    sns.despine(offset=10, trim=True)
    plt.show()



if __name__ == '__main__':
    #npy2csv()
    main()