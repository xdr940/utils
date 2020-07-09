import json
from path import Path
import argparse
parser =argparse.ArgumentParser('None')
parser.add_argument('--file',type=str,default='./10001000.json')
args= parser.parse_args()
#对原始的json文件处理时间,windows使用
def writelines(frames,path):
    titles = ['time','pitch','roll','yaw','x','y','z']
    with open(path,'w') as f:
        #f.writelines('#'+str(list(frames[0].keys()))[1:-1])
        f.writelines('#'+str(titles)[1:-1]+' \n')
        for item in frames:
            line =[]
            for  sub_title in titles:
                line.append(item[sub_title])
            f.writelines(str(line)[1:-1]+' \n')#dic 2 list 2 str



def readjson(path):
    f = open(path, encoding='utf-8')
    content = f.read()
    dict = json.loads(content)
    return  dict

def read_path(path_name):
    #path_name is a list
    num_frames = len(path_name[0]['keyframes'])
    ret_list=[]
    frame={}
    for i in range(num_frames):
        #frame['no'] = '{:07d}'.format(i)
        #frame['no'] = i

        frame['time'] = path_name[1]['keyframes'][i]['time']
        frame['pitch'] = path_name[1]['keyframes'][i]['properties']['camera:rotation'][1]
        frame['yaw'] = path_name[1]['keyframes'][i]['properties']['camera:rotation'][0]
        frame['roll']  = path_name[1]['keyframes'][i]['properties']['camera:rotation'][2]

        frame['x'] = path_name[1]['keyframes'][i]['properties']['camera:position'][0]
        frame['y'] = path_name[1]['keyframes'][i]['properties']['camera:position'][1]
        frame['z'] = path_name[1]['keyframes'][i]['properties']['camera:position'][2]

        ret_list.append(frame.copy())

    return ret_list


    #frames={}


    pass


def format_js(p):
    dict = readjson(p)
    print('format timelines')
    for key in dict.keys():
#        dict.pop('')
        if key!='':
            i =0
            slices =  dict[key][0]['keyframes']
            for slice in slices:#
                slice['time'] = i*5000
                slice['properties']['timestamp'] = i*5000
                i+=1
                pass
            slices = dict[key][1]['keyframes']
            i=0
            for slice in slices:  #
                slice['time'] = i * 5000
                slice['properties']['timestamp'] = i*5000
                i += 1
                pass
    dict.pop('')
    f =Path('format.json')

    with open('format.json','w') as fp:
        json.dump(dict,fp)
    pass




if  __name__ == '__main__':

    timelines = Path(args.file)
    format_js(timelines)
    print('ok')
    #json2txt(timelines)


