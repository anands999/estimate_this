# Rotation matrix library

import math as m
import numpy as np

def eye():
    R=np.matrix('1 0 0;0 1 0; 0 0 1')
    return R;

def c1(a):
    c=np.cos(a)
    s=np.sin(a)
    c1=np.matrix('{} {} {}; {} {} {}; {} {} {}'.format(1,0,0,0,c,s,0,-s,c))
    return c1

def c2(a):
    c=np.cos(a)
    s=np.sin(a)
    c2=np.matrix('{} {} {}; {} {} {}; {} {} {}'.format(c,0,-s,0,1,0,s,0,c))
    return c2

def c3(a):
    c=np.cos(a)
    s=np.sin(a)
    c3=np.matrix('{} {} {}; {} {} {}; {} {} {}'.format(c,s,0,-s,c,0,0,0,1))
    return c3

def skew(a):
    if type(a) is np.ndarray:
        a1=a[0]
        a2=a[1]
        a3=a[2]
    elif type(a) is np.matrix:
        a1=a.item(0)
        a2=a.item(1)
        a3=a.item(2)

    skew=np.matrix('{} {} {}; {} {} {}; {} {} {}'.format(0,-a3,a2,a3,0,-a1,-a2,a1,0))
    return skew

def rotRPY(r,p,y):
    cr=c1(r)
    cp=c2(p)
    cy=c3(y)
    return cy*cp*cr

def unit(x):
    if type(x) is np.ndarray:
        if np.dot(x,x) != 1:
            axis=x/np.linalg.norm(x,2)
        else:
            axis=x

    elif type(x) is np.matrix:
        xT=x.T
        if x.shape[0] is 3 and x.shape[1] is 1:
            dotP=float(np.dot(xT,x))
        else:
            dotP=float(np.dot(x,xT))

        if dotP != 1:
            axis=x/np.linalg.norm(x,2)
        else:
            axis=x

    return axis

def col(x):
    if type(x) is np.matrix:
        if x.shape[0] is 3 and x.shape[1] is 1:
            xout=x
        else:
            xout=x.T
    else:
        xout=np.matrix(x).T
    return xout

def rotEulAx(theta, ax_in):

    axis=unit(ax_in)

    c=np.cos(theta)
    s=np.sin(theta)

    C=eye()*c+(1.-c)*np.outer(axis,axis)-s*skew(axis)
    return C

def poisson(C,w):
    wX=skew(w)
    Cdot=-wX*C
    return Cdot

def triad(mag, accel):
    x1b=col(unit(mag))
    x2b=col(unit(accel))
    v1b=x1b
    v2b=skew(x1b)*x2b
    v2b=unit(v2b)
    v3b=skew(v1b)*v2b
    v3b=unit(v3b)


    x1a=np.matrix('1.;0.;0.')
    x2a=np.matrix('0.;0.;1.')

    v1a=x1a
    v2a=skew(x1a)*x2a
    v2a=unit(v2a)
    v3a=skew(v1a)*v2a
    v3a=unit(v3a)

    C1=np.column_stack((v1b,v2b,v3b))
    C2=np.column_stack((v1a,v2a,v3a))

    C=C1*C2.T
    return C

def RPYfromC(C):
    if C is not np.matrix and C.size is not 9:
        print 'Matrix not the right size'
        sys.exit()
    else:
        s1c2=-C.item(2,1)#-float(C[2][1])
        c1c2=C.item(2,2) #float(C[2][2])
        roll=np.arctan2(s1c2,c1c2)

        c1=np.cos(roll)
        print c1
        if abs(c1) > 0.0001:
            c2=c1c2/c1
            s2=C.item(2,0) #float(C[2][0])
            pitch=np.arctan2(s2,c2)
        else:
            pitch=np.arcsin(s2)

        c2c3=C.item(0,0)  #float(C[0][0])
        c2s3=-C.item(1,0) #float(C[1][0])
        yaw=np.arctan2(c2s3,c2c3)

    return [roll, pitch, yaw]

