
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from path import Path
from matplotlib import cm

class CatmulRom(object):

    def __init__(self,n_step,alpha):
        self.n_step = n_step
        self.alpha = alpha



    def spline(self,t, t0, t1, t2, t3, p0, p1, p2, p3):
        a1_x = (t1 - t) / (t1 - t0) * p0[0] + (t - t0) / (t1 - t0) * p1[0]
        a2_x = (t2 - t) / (t2 - t1) * p1[0] + (t - t1) / (t2 - t1) * p2[0]
        a3_x = (t3 - t) / (t3 - t2) * p2[0] + (t - t2) / (t3 - t2) * p3[0]

        b1_x = (t2 - t) / (t2 - t0) * a1_x + (t - t0) / (t2 - t0) * a2_x
        b2_x = (t3 - t) / (t3 - t1) * a2_x + (t - t1) / (t3 - t1) * a3_x

        c_x = (t2 - t) / (t2 - t1) * b1_x + (t - t1) / (t2 - t1) * b2_x

        a1_y = (t1 - t) / (t1 - t0) * p0[1] + (t - t0) / (t1 - t0) * p1[1]
        a2_y = (t2 - t) / (t2 - t1) * p1[1] + (t - t1) / (t2 - t1) * p2[1]
        a3_y = (t3 - t) / (t3 - t2) * p2[1] + (t - t2) / (t3 - t2) * p3[1]

        b1_y = (t2 - t) / (t2 - t0) * a1_y + (t - t0) / (t2 - t0) * a2_y
        b2_y = (t3 - t) / (t3 - t1) * a2_y + (t - t1) / (t3 - t1) * a3_y

        c_y = (t2 - t) / (t2 - t1) * b1_y + (t - t1) / (t2 - t1) * b2_y

        return c_x, c_y


    def spline3(self,t,t0,t1,t2,t3,p0,p1,p2,p3):
        '''

        :param t:
        :param t0:
        :param t1:
        :param t2:
        :param t3:
        :param p0:
        :param p1:
        :param p2:
        :param p3:
        :return:
        '''

        #x
        a1_x = (t1 - t) / (t1 - t0) * p0[0] + (t - t0) / (t1 - t0) * p1[0]
        a2_x = (t2 - t) / (t2 - t1) * p1[0] + (t - t1) / (t2 - t1) * p2[0]
        a3_x = (t3 - t) / (t3 - t2) * p2[0] + (t - t2) / (t3 - t2) * p3[0]

        b1_x = (t2 - t) / (t2 - t0) * a1_x + (t - t0) / (t2 - t0) * a2_x
        b2_x = (t3 - t) / (t3 - t1) * a2_x + (t - t1) / (t3 - t1) * a3_x

        c_x = (t2 - t) / (t2 - t1) * b1_x + (t - t1) / (t2 - t1) * b2_x

        #y
        a1_y = (t1 - t) / (t1 - t0) * p0[1] + (t - t0) / (t1 - t0) * p1[1]
        a2_y = (t2 - t) / (t2 - t1) * p1[1] + (t - t1) / (t2 - t1) * p2[1]
        a3_y = (t3 - t) / (t3 - t2) * p2[1] + (t - t2) / (t3 - t2) * p3[1]

        b1_y = (t2 - t) / (t2 - t0) * a1_y + (t - t0) / (t2 - t0) * a2_y
        b2_y = (t3 - t) / (t3 - t1) * a2_y + (t - t1) / (t3 - t1) * a3_y

        c_y = (t2 - t) / (t2 - t1) * b1_y + (t - t1) / (t2 - t1) * b2_y


        # z
        a1_z = (t1 - t) / (t1 - t0) * p0[2] + (t - t0) / (t1 - t0) * p1[2]
        a2_z = (t2 - t) / (t2 - t1) * p1[2] + (t - t1) / (t2 - t1) * p2[2]
        a3_z = (t3 - t) / (t3 - t2) * p2[2] + (t - t2) / (t3 - t2) * p3[2]

        b1_z = (t2 - t) / (t2 - t0) * a1_z + (t - t0) / (t2 - t0) * a2_z
        b2_z = (t3 - t) / (t3 - t1) * a2_z + (t - t1) / (t3 - t1) * a3_z

        c_z = (t2 - t) / (t2 - t1) * b1_z + (t - t1) / (t2 - t1) * b2_z

        return  c_x,c_y,c_z

    def run(self,p):
        '''

        :param p: 控制点(x,y)
        :param n_step: 控制点之间插入点数()
        :param alpha:
        :return:
        '''
        curve = list()

        # first curve
        t0 = 0
        t1 = (0.1) ** self.alpha + t0  # for numerical stability (divide-by-zero)
        t2 = ((p[1][0] - p[0][0]) ** 2 + (p[1][1] - p[0][1]) ** 2) ** self.alpha + t1
        t3 = ((p[2][0] - p[1][0]) ** 2 + (p[2][1] - p[1][1]) ** 2) ** self.alpha + t2
        step = (t2 - t1) / self.n_step

        for j in range(self.n_step):
            cx, cy = self.spline(t1 + j * step, t0, t1, t2, t3, p[0], p[0], p[1], p[2])
            curve.append([cx, cy])

        # middle curve
        for i in range(len(p) - 3):
            t0 = 0
            t1 = ((p[i + 1][0] - p[i][0]) ** 2 + (p[i + 1][1] - p[i][1]) ** 2) ** self.alpha + t0
            t2 = ((p[i + 2][0] - p[i + 1][0]) ** 2 + (p[i + 2][1] - p[i + 1][1]) ** 2) ** self.alpha + t1
            t3 = ((p[i + 3][0] - p[i + 2][0]) ** 2 + (p[i + 3][1] - p[i + 2][1]) ** 2) ** self.alpha + t2
            step = (t2 - t1) / self.n_step

            for j in range(self.n_step):
                cx, cy = self.spline(t1 + j * step, t0, t1, t2, t3, p[i], p[i + 1], p[i + 2], p[i + 3])
                curve.append([cx, cy])

        # last curve
        t0 = 0
        t1 = ((p[-2][0] - p[-3][0]) ** 2 + (p[-2][1] - p[-3][1]) ** 2) ** self.alpha + t0
        t2 = ((p[-1][0] - p[-2][0]) ** 2 + (p[-1][1] - p[-2][1]) ** 2) ** self.alpha + t1
        t3 = (0.1) ** self.alpha + t2  # for numerical stability (divide-by-zero)
        step = (t2 - t1) / self.n_step

        for j in range(self.n_step):
            cx, cy = self.spline(t1 + j * step, t0, t1, t2, t3, p[-3], p[-2], p[-1], p[-1])
            curve.append([cx, cy])

        return curve

    def run3d(self,p):

        curve = list()

        # first curve
        t0 = 0
        t1 = (0.1) ** self.alpha + t0  # for numerical stability (divide-by-zero)
        t2 = ((p[1][0] - p[0][0]) ** 2 + (p[1][1] - p[0][1]) ** 2 +(p[1][2] - p[0][2]) ** 2 ) ** self.alpha + t1
        t3 = ((p[2][0] - p[1][0]) ** 2 + (p[2][1] - p[1][1]) ** 2 +(p[2][2] - p[1][2]) ** 2) ** self.alpha + t2
        step = (t2 - t1) / self.n_step

        for j in range(self.n_step):
            cx, cy ,cz= self.spline3(t1 + j * step, t0, t1, t2, t3, p[0], p[0], p[1], p[2])
            curve.append([cx, cy, cz])

        # middle curve
        for i in range(len(p) - 3):
            t0 = 0
            t1 = ((p[i + 1][0] - p[i][0]) ** 2 + (p[i + 1][1] - p[i][1]) ** 2 + (p[i + 1][2] - p[i][2]) ** 2) ** self.alpha + t0
            t2 = ((p[i + 2][0] - p[i + 1][0]) ** 2 + (p[i + 2][1] - p[i + 1][1]) ** 2+ (p[i + 2][2] - p[i + 1][2]) ** 2) ** self.alpha + t1
            t3 = ((p[i + 3][0] - p[i + 2][0]) ** 2 + (p[i + 3][1] - p[i + 2][1]) ** 2+ (p[i + 3][2] - p[i + 2][2]) ** 2) ** self.alpha + t2
            step = (t2 - t1) / self.n_step

            for j in range(self.n_step):
                cx, cy,cz = self.spline3(t1 + j * step, t0, t1, t2, t3, p[i], p[i + 1], p[i + 2], p[i + 3])
                curve.append([cx, cy,cz])

        # last curve
        t0 = 0
        t1 = ((p[-2][0] - p[-3][0]) ** 2 + (p[-2][1] - p[-3][1]) ** 2+ (p[-2][2] - p[-3][2]) ** 2) ** self.alpha + t0
        t2 = ((p[-1][0] - p[-2][0]) ** 2 + (p[-1][1] - p[-2][1]) ** 2+ (p[-1][2] - p[-2][2]) ** 2) ** self.alpha + t1
        t3 = (0.1) ** self.alpha + t2  # for numerical stability (divide-by-zero)
        step = (t2 - t1) / self.n_step

        for j in range(self.n_step):
            cx, cy ,cz= self.spline3(t1 + j * step, t0, t1, t2, t3, p[-3], p[-2], p[-1], p[-1])
            curve.append([cx, cy,cz])

        return curve












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


def main2():
    data = Path('data2')
    time = readlines('timestamp2')
    frames = readlines(data)
    #插值参数
    alpha =0.5
    n_steps = 50

    assert (len(frames) == len(time), '文件不匹配长度不等')
    lenth = len(time)

    x = []
    y = []
    z = []
    yaw = []
    pitch = []
    roll = []

    for i in range(lenth):
        x.append(frames[i][0])
        y.append(frames[i][1])
        z.append(frames[i][2])
        yaw.append(frames[i][3])
        pitch.append(frames[i][4])
        roll.append(frames[i][5])

    ptsx = []
    ptsy = []
    ptsz = []
    ptsyaw = []
    ptspitch = []
    ptsroll = []
    for i in range(lenth):
        ptsx.append([time[i], x[i]])
        ptsy.append([time[i], y[i]])
        ptsz.append([time[i], z[i]])
        ptsyaw.append([time[i], yaw[i]])
        ptspitch.append([time[i], pitch[i]])
        ptsroll.append([time[i], roll[i]])


    cvx = plot_curve(p=ptsx, n_step=n_steps, alpha=alpha)
    t, x = zip(*cvx)#差值函数
    ptime, py = zip(*ptsx)#控制点
    #plt.plot(time, x, color="blue", markersize=3)

    cvy = plot_curve(p=ptsy, n_step=n_steps, alpha=alpha)
    t, y = zip(*cvy)
    ptime, py = zip(*ptsy)
    #plt.plot(time, y, color="blue", markersize=3)

    cvz = plot_curve(p=ptsz, n_step=n_steps, alpha=alpha)
    t, z = zip(*cvz)
    ptime, pz = zip(*ptsz)
    #plt.plot(time, y, color="blue", markersize=3)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    #ax.set_xlim([0,300])
    #ax.set_ylim([300,600])
    #ax.set_zlim([0,300])

    ax.plot(x,z,y)

    plt.show()


def main():
    pts = [[281, 944], [269, 1121], [285, 1291], [330, 1458], [398, 1566],
           [484, 1659], [583, 1737], [728, 1769], [873, 1737], [966, 1659],
           [1041, 1560], [1106, 1447], [1153, 1282], [1175, 1112], [1170, 936]]
    cv = plot_curve(pts, 3, alpha=0.5)

    x, y = zip(*cv)
    px, py = zip(*pts)

    plt.plot(x, y, color="blue", markersize=3)
    # plt.plot(x, y, "or", color="blue", markersize=3)
    plt.plot(px, py, "or", markersize=3)
    plt.show()

if __name__ == '__main__':
    #test()
    main2()



