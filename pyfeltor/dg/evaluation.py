from . import create
import numpy as np

def evaluate( function, grid):
    """ Evaluate a function on the grid points of the given grid

    function: has to take numpy arrays as arguments, f(x), f(y,x), f(z,y,x)
    grid: instance of dg.Grid
    """
    xs = []
    dims = grid.dim()
    for dim in range( 0, dims):
        xs.append( create.abscissas(grid, dim))

    if dims == 1 :
        return np.array( function( xs[0]))
    if dims == 2 :
        return np.array( function( xs[0][:,None], xs[1][None,:]))
    if dims == 3 :
        return np.array( function( xs[0][:,None,None], xs[1][None,:,None]),xs[2][None,None,:])
    if dims == 4 :
        return np.array( function( xs[0][:,None,None,None], xs[1][None,:,None,None]),xs[2][None,None,:,None],xs[3][None,None,None,:])
    if dims > 4 :
        raise "Evaluate is not implemented for dim > 4"


