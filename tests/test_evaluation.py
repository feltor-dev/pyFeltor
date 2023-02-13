import pytest
import numpy as np
from pyfeltor import dg

def function2d( y, x):
    rho = 0.20943951023931953 # pi/15
    delta = 0.050000000000000003
    return np.where( y <= np.pi,
        delta*np.cos(x) - 1./rho/np.cosh( (y-np.pi/2.)/rho)/np.cosh( (y-np.pi/2.)/rho),
        delta*np.cos(x) + 1./rho/np.cosh( (3.*np.pi/2.-y)/rho)/np.cosh( (3.*np.pi/2.-y)/rho))

def test_evalution():
    n = 3
    Nx = 12
    Ny = 28
    Nz = 100
    g1d = dg.Grid( [1],[2],[n], [Nx], [dg.bc.PER])
    g2d = dg.Grid( (0,0),(2*np.pi, 2*np.pi),(n,n), (Ny,Nx), (dg.bc.PER,dg.bc.PER))
    w1d = dg.create.weights( g1d)
    w2d = dg.create.weights( g2d)
    func1d = dg.evaluate( lambda x : np.exp(x), g1d)
    func2d = dg.evaluate( function2d, g2d)

    sol1d = np.exp(2)-np.exp(1)
    num1d = np.sum( w1d*func1d)
    print( f"Correct integral is {sol1d} while numerical is {num1d}")
    assert np.abs(sol1d - num1d)/sol1d < 1e-10

    sol2d = 0.
    num2d = np.sum( w2d*func2d)
    print( f"Correct integral is {sol2d} while numerical is {num2d}")
    assert np.abs(sol2d - num2d) < 1e-10


