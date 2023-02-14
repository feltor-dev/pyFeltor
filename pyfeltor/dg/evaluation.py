from . import create
import numpy as np


def evaluate(function, grid):
    """Evaluate a function on the grid points of the given grid

    function: has to take numpy arrays as arguments, f(x), f(y,x), f(z,y,x)
    grid: instance of dg.Grid
    return: flat np.array with x the fastest varying dimension. Can be reshaped with reshape(grid.shape)
    """
    xs = []
    ndim = grid.ndim
    for dim in range(0, ndim):
        xs.append(create.abscissas(grid, dim))

    if ndim == 1:
        return np.array( [ function(x) for x in xs[0]])
    if ndim == 2:
        return np.array( [ function(y, x) for y in xs[0] for x in xs[1] ])
    if ndim == 3:
        return np.array( [function( z,y,x) for z in xs[0] for y in xs[1] for x in xs[2]])
    if ndim == 4:
        return np.array( [function( xx, z,y,x) for xx in xs[0] for z in xs[1] for y in xs[2] for x in xs[3]])
    if ndim > 4:
        raise "Evaluate is not implemented for dim > 4"
