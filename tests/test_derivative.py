import pytest
from pyfeltor import dg
import numpy as np

# Run with pytest-3 -s . to see stdout output


def zero(y, x):
    return 0


def sine(y, x):
    return np.sin(x) * np.sin(y)


def cosx(y, x):
    return np.cos(x) * np.sin(y)


def cosy(y, x):
    return np.cos(y) * np.sin(x)


def test_dx( ):
    n, N = 3, 20
    gPER = dg.Grid( [0.1], [2*np.pi+0.1], [n], [N], [dg.bc.PER]);
    gDIR = dg.Grid( [0], [np.pi], [n], [N], [dg.bc.DIR]);
    gNEU = dg.Grid( [np.pi/2.], [3*np.pi/2.], [n], [N], [dg.bc.NEU]);
    gDIR_NEU = dg.Grid( [0], [np.pi/2.], [n], [N], [dg.bc.DIR_NEU]);
    gNEU_DIR = dg.Grid( [np.pi/2.], [np.pi], [n], [N], [dg.bc.NEU_DIR]);
    g = [gPER, gDIR, gNEU, gDIR_NEU, gNEU_DIR]
    print("TEST NORMAL TOPOLOGY: YOU SHOULD SEE CONVERGENCE FOR ALL OUTPUTS!!!")
    print("COMPARE TO dx_t.cu")
    for i in range(0,5):
        print( "Boundary condition ", g[i].bc[0])
        hs = dg.create.dx( 0, g[i], g[i].bc[0], dg.direction.centered);
        hf = dg.create.dx( 0, g[i], g[i].bc[0], dg.direction.forward);
        hb = dg.create.dx( 0, g[i], g[i].bc[0], dg.direction.backward);
        js = dg.create.jump( 0, g[i], g[i].bc[0]);
        func = dg.evaluate( lambda x : np.sin(x), g[i]);
        error = func;
        w1d = dg.create.weights( g[i]);
        deri = dg.evaluate( lambda x : np.cos(x), g[i]);
        null = dg.evaluate( lambda x: 0, g[i]);
        error = deri - hs.dot(func)
        print( f"Distance to true solution (symmetric): {np.sqrt(np.sum( w1d*error**2) )}")
        error = deri - hf.dot(func)
        print( f"Distance to true solution (forward): {np.sqrt(np.sum( w1d*error**2) )}")
        error = deri - hb.dot(func)
        print( f"Distance to true solution (backward): {np.sqrt(np.sum( w1d*error**2) )}")
        error = null - js.dot(func)
        print( f"Distance to true solution (jump     ): {np.sqrt(np.sum( w1d*error**2) )}")


def test_derivative():
    n, Nx, Ny, Nz = 3, 24, 28, 100
    print(f"On Grid {n} x {Nx} x {Ny} x {Nz}")
    bcx, bcy, bcz = dg.bc.DIR, dg.bc.PER, dg.bc.NEU_DIR
    g2d = dg.Grid([0.1, 0], [2 * np.pi + 0.1, np.pi], [n, n], [Ny, Nx], [bcy, bcx])
    w2d = dg.create.weights(g2d)

    dx2 = dg.create.dx(1, g2d, g2d.bc[1], dg.direction.forward)
    dy2 = dg.create.dx(0, g2d, g2d.bc[0], dg.direction.centered)
    jx2 = dg.create.jump(1, g2d, g2d.bc[1])
    jy2 = dg.create.jump(0, g2d, g2d.bc[0])
    m2 = [dx2, dy2, jx2, jy2]
    f2d = dg.evaluate(sine, g2d)
    dx2d = dg.evaluate(cosx, g2d)
    dy2d = dg.evaluate(cosy, g2d)
    null2 = dg.evaluate(zero, g2d)
    sol2 = [dx2d, dy2d, null2, null2]
    # binary2[4562611930300281864,4553674328256556132,4567083257206218817,4574111364446550002]
    sol = [0.0010775034079703078,0.00027314872436790867,0.0021410107540649087,0.006471682818855125]

    print("TEST 2D: DX, DY, JX, JY")
    for i in range(0, 4):
        error = sol2[i].copy()
        error = -m2[i].dot(f2d) + error
        norm = np.sqrt(np.sum(w2d * error**2))
        print(f"Absolute error to true solution: {norm}")
        assert norm == sol[i]
