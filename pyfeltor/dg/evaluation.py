from . import create
import numpy as np

def evaluate( function, grid):
    """ Evaluate a function on the grid points of the given grid

    function: has to take numpy arrays as arguments, f(x), f(y,x), f(z,y,x)
    grid: instance of dg.Grid
    """
    xs = []
    ndim = grid.ndim
    for dim in range( 0, ndim):
        xs.append( create.abscissas(grid, dim))

    if ndim == 1 :
        return np.array( function( xs[0]))
    if ndim == 2 :
        return np.array( function( xs[0][:,None], xs[1][None,:]))
    if ndim == 3 :
        return np.array( function( xs[0][:,None,None], xs[1][None,:,None]),xs[2][None,None,:])
    if ndim == 4 :
        return np.array( function( xs[0][:,None,None,None], xs[1][None,:,None,None]),xs[2][None,None,:,None],xs[3][None,None,None,:])
    if ndim > 4 :
        raise "Evaluate is not implemented for dim > 4"


