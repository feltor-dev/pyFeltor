import pytest
from pyfeltor import dg
import numpy as np
def zero( y, x):
    return 0
def sine( y, x):
    return np.sin(x)*np.sin(y)
def cosx( y, x):
    return np.cos(x)*np.sin(y)
def cosy( y, x):
    return np.cos(y)*np.sin(x)

def test_derivative() :

    n, Nx, Ny, Nz = 3, 24, 28, 100
    print(f"On Grid {n} x {Nx} x {Ny} x {Nz}")
    bcx, bcy, bcz = dg.bc.DIR, dg.bc.PER, dg.bc.NEU_DIR
    g2d = dg.Grid( [0.1,0], [2*np.pi+0.1,np.pi], [n,n],[Ny,Nx], [bcy, bcx])
    w2d = dg.create.weights( g2d);

    dx2 = dg.create.derivative(1, g2d, g2d.bc[1], dg.direction.forward)
    dy2 = dg.create.derivative(0, g2d, g2d.bc[0], dg.direction.centered)
    jx2 = dg.create.jump( 1, g2d, g2d.bc[1])
    jy2 = dg.create.jump( 0, g2d, g2d.bc[0])
    m2 = [dx2, dy2, jx2, jy2]
    f2d = dg.evaluate( sine, g2d)
    dx2d = dg.evaluate( cosx, g2d)
    dy2d = dg.evaluate( cosy, g2d)
    null2 = dg.evaluate( zero, g2d)
    sol2 = [dx2d, dy2d, null2, null2]
    #binary2[4562611930300281864,4553674328256556132,4567083257206218817,4574111364446550002]

    print("TEST 2D: DX, DY, JX, JY")
    for i in range(0, 4):
        error = sol2[i].copy()
        print( m2[i].shape)
        print( f2d.flatten().shape)
        error = -m2[i].dot( f2d.flatten()) + error
        norm = np.sqrt(np.sum( w2d*error**2))/np.sqrt(w2d*sol2[i]**2)
        print( f"Relative error to true solution: {norm}")
