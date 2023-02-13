import numpy as np

def weights( grid):
    """ Create dG weights on given grid """
    weights = np.array([1])
    for dim in range(0, grid.ndim):
        (x,w) = np.polynomial.legendre.leggauss(grid.n[dim])
        wdim = np.tile( w, grid.N[dim])*grid.h()[dim]/2.0
        weights = np.kron( weights, wdim)
        weights = np.reshape( weights, grid.size()[0:dim+1])
    return weights

def abscissas(grid, dimension = 0):
    """ Create 1d dG abscissas on given grid for given dimension """
    dim = dimension
    (x,w) = np.polynomial.legendre.leggauss(grid.n[dim])
    abscissas = np.zeros( grid.size()[dim])
    h  = grid.h()[dim]
    x0 = grid.x0[dim]
    for i in range(0,grid.N[dim]):
        for k in range(0,grid.n[dim]):
            abscissas[i*grid.n[dim]+k] = i*h+x0 + h/2.0*(1.0+x[k])
    return abscissas


