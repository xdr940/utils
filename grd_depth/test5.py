
import numpy as np
from numpy import sin,cos,pi,tan,sqrt
from numpy import  arctan as atan
np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt
#綜合測試三個計算yp(Zw;phi,yt)的白盒模型

def Rxyz(theta,psi,phi,x0,y0,z0):

    t = np.array([[x0, y0, z0]])  # 为了拼接, 这里是矩阵


    one = np.array([[1]])
    Rz = np.array([cos(theta), -sin(theta), 0.,
                   sin(theta), cos(theta), 0.,
                   0.,0.,1.]).reshape(3,3)

    Rx = np.array([1,0,0,
                   0,cos(psi),sin(psi),
                   0,-sin(psi),cos(psi)]).reshape(3,3)

    Ry = np.array([cos(phi),0,-sin(phi),
                   0,1,0,
                   sin(phi),0,cos(phi)]).reshape(3,3)
    R = Rx@Ry@Rz
    #R = np.ones([3,3])
    zero3= np.zeros([1,3])
    R = np.concatenate([R,zero3],axis=0)
    t = np.concatenate([t,one],axis=1)
    RT = np.concatenate([R,t.T],axis=1)
    #print(Rx)
    #print(RT)
    #

    return RT
def K_1(fov=70,u0=400,v0=300):
    '''
    属性图像求解内参
    input:fov, u0,v0
    output fx, fy
    return:K
    '''

    fov = fov#d
    belta = fov/2
    u0 = u0
    v0 = v0
    belta = belta*pi/360
    fx = u0/tan(belta)
    fy = v0/tan(belta)
    K = np.array([fx,0,u0,0,
                  0,fy,v0,0,
                  0,0,1,0]).reshape(3,4)
    return K

def K_2(f=30e-3,dx=26e-6,dy=26e-6):
    '''
    相机属性(SI单位)求解内参
    input    f =30e-3#35mm;
            dx,dy=0.00026#0.026m = /pixel

    :return:K
    '''

    dx =dx
    dy = dy
    u0 = 400
    v0 = 300

    h=2*u0*dx
    w=2*v0*dy
    fov = atan(0.5*h/f)
    K1 = np.array([1/dx,0,u0,
                   0, 1/dy,v0,
                   0,0,1]).reshape(3,3)
    K2 = np.array([f,0,0,0,
                   0,f,0,0,
                   0,0,1,0]).reshape(3,4)
    #print(h,w)
    K = K1@K2

    return K
    #print(K)
#RT =Rxyz(theta,psi,phi,t)

def yp(yt,psi,zw,v0=300,fy=428):
    temp = zw*(fy*sin(psi)+v0*cos(psi))+fy*yt
    return temp/(zw*cos(psi))
def main():
    # camera
    theta =0#-pi / 4
    psi =-pi / 4
    phi =0  #pi/4
    xt = 0
    yt = 40*sqrt(3)#世界往相机坐标系y方向移动50
    zt = 0
    # point
    Xw =0
    Yw = 0
    Zw = 80
    pW = np.array([[Xw, Yw, Zw, 1]]).T  # 齐次化

    # caculate
    pp1 =K_1()@ Rxyz(theta=theta, psi=psi, phi=phi, x0=xt, y0=yt, z0=zt) @ pW
    pp1 = pp1 / pp1[2, 0]
    print('pp1\n',pp1)

    pp2 = K_2() @ Rxyz(theta=theta, psi=psi, phi=phi, x0=xt, y0=yt, z0=zt) @ pW
    pp2 = pp2 / pp2[2, 0]
    print('pp2\n', pp2)



    pp3 = yp(yt,psi,Zw)
    print('pp3',pp3)
def test_K1(Zw,psi = -pi / 4,yt =40 * sqrt(3)):
    theta = 0  # -pi / 4
    #psi = -pi / 4
    phi = 0  # pi/4
    xt = 0
   # yt = 40 * sqrt(3)  # 世界往相机坐标系y方向移动50
    zt = 0
    # point
    Xw = 0
    Yw = 0
    #Zw = 80
    pW = np.array([[Xw, Yw, Zw, 1]]).T  # 齐次化

    # caculate
    pp1 = K_1() @ Rxyz(theta=theta, psi=psi, phi=phi, x0=xt, y0=yt, z0=zt) @ pW
    pp1 = pp1 / pp1[2, 0]
    return pp1[1][0]

def test_K2(Zw,psi=-pi / 4,yt=40 * sqrt(3)):
    theta = 0  # -pi / 4
    #psi = -pi / 4
    phi = 0  # pi/4
    xt = 0
   # yt = 40 * sqrt(3)  # 世界往相机坐标系y方向移动50
    zt = 0
    # point
    Xw = 0
    Yw = 0
    # Zw = 80
    pW = np.array([[Xw, Yw, Zw, 1]]).T  # 齐次化

    # caculate
    pp2 = K_2() @ Rxyz(theta=theta, psi=psi, phi=phi, x0=xt, y0=yt, z0=zt) @ pW
    pp2 = pp2 / pp2[2, 0]
    return pp2[1][0]

def test_yp(Zw,psi=-pi / 4,yt=40 * sqrt(3)):
    theta = 0  # -pi / 4
    #psi = -pi / 4
    phi = 0  # pi/4
    xt = 0
    #yt = 40 * sqrt(3)  # 世界往相机坐标系y方向移动50
    zt = 0
    # point
    Xw = 0
    Yw = 0
    #Zw = 80
    pW = np.array([[Xw, Yw, Zw, 1]]).T  # 齐次化
    pp3 = yp(yt, psi, Zw)
    return pp3
if __name__ =='__main__':
    pass
    #args
    psi = -pi / 6
    yt =  40 * sqrt(3)

    #vars
    xs=[]
    ys=[]
    start = 80
    end = 120
    for x in range(start,end):
        y=test_K1(x,psi,yt)
        xs.append(x)
        ys.append(y)
    plt.plot(xs,ys,'b',label='K1_test')

    xs.clear()
    ys.clear()
    for x in range(start,end):
        y=test_K2(x,psi,yt)
        xs.append(x)
        ys.append(y)
    plt.plot(xs,ys,'r',label='K2_test')

    xs.clear()
    ys.clear()
    for x in range(start,end):
        y = test_yp(x,psi,yt)
        xs.append(x)
        ys.append(y)
    plt.plot(xs, ys, 'g', label='yp_test')
    plt.axis('equal')
    plt.legend()
    plt.show()
    #main()
    #print(np.array([1,2,3,4,5,6,7,8,9]).reshape(3,3))