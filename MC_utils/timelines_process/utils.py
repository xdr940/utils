


def readlines(filename):
    """Read all the lines in a text file and return as a list
    """
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    i=0
    while(i<len(lines)):
        if lines[i][0]=='#':
            lines.pop(i)
            i-=1
        i+=1
    i=0
    ret =[]
    while(i<len(lines)):
        ret.append(lines[i].split(','))
        if len(ret[i])==1:
            ret[i] = float(ret[i][0])
        else:

            for j in range(len(ret[i])):
                ret[i][j] = float(ret[i][j])
        i+=1


    return ret

def write_as_lines(rotation,position,path):
    with open(path,'w') as f:
        f.writelines(string)
