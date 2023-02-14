from pyfeltor import dg
import numpy as np

n, Nx, Ny, Nz = 3,9,5,4
def test_interpolation1d():
    print( "1D INTERPOLATION TEST")
    passed = True
    g1d = dg.Grid( [-np.pi], [0], [n], [Nx])
    field = dg.evaluate( lambda x : x, g1d)
    x = [(i+0.5)*g1d.h()[0]/g1d.n[0] for i in range(0, g1d.size())]

    interp = dg.create.interpolation( [x], g1d, [dg.bc.DIR])
    x_inter = interp.dot( field)
    for i in range( g1d.size()):
        if( x[i] - x_inter[i] > 1e-14):
            print(f"X NOT EQUAL {i}\t{x[i]}  \t{x_inter[i]}")
            passed = False
    assert( passed)
    

def test_interpolation2d():
    print( "2D INTERPOLATION TEST")

    g = dg.Grid( [-5, -10], [5, 10], [n,n], [Ny, Nx]);
    equi = dg.Grid( [-5, -10], [5, 10], [1,1], [n*Ny, n*Nx]);
    y = dg.evaluate( lambda y,x : y , equi)
    x = dg.evaluate( lambda y,x : x , equi)

    print ( "Length of arrays", len(y), len(x))
    interp = dg.create.interpolation( [y,x], g, [dg.bc.DIR, dg.bc.PER])
    vec = dg.evaluate( lambda y,x: np.sin(x)*np.sin(y), g)
    inter = interp.dot( vec)
    interE = dg.evaluate( lambda y,x: np.sin(x)*np.sin(y), equi)
    print( inter[0:10])
    print( interE[0:10])
    error = np.sum ( (inter-interE)**2)/np.sum(inter**2)
    print(f"Error is {np.sqrt(error)} (should be small)!")
    assert np.isclose( np.sqrt(error), 0)


def test_interpolation3d():
    print( "3D INTERPOLATION TEST")

    g = dg.Grid( [-7, -5, -10], [-3, 5, 10], [n,n,n], [Nz, Ny, Nx]);
    equi = dg.Grid( [-7, -5, -10], [-3, 5, 10], [1,1,1], [n*Nz, n*Ny, n*Nx]);
    z = dg.evaluate( lambda z,y,x : z , equi)
    y = dg.evaluate( lambda z,y,x : y , equi)
    x = dg.evaluate( lambda z,y,x : x , equi)

    print ( "Length of arrays", len(z), len(y), len(x))
    interp = dg.create.interpolation( [z,y,x], g, [dg.bc.DIR, dg.bc.DIR, dg.bc.PER])
    vec = dg.evaluate( lambda z,y,x: np.sin(x)*np.sin(y)*np.sin(z), g)
    inter = interp.dot( vec)
    interE = dg.evaluate( lambda z,y,x: np.sin(x)*np.sin(y)*np.sin(z), equi)
    print( inter[0:10])
    print( interE[0:10])
    error = np.sum ( (inter-interE)**2)/np.sum(inter**2)
    print(f"Error is {np.sqrt(error)} (should be small)!")
    assert np.isclose( np.sqrt(error), 0)
