import numpy as np

from . import create
from .create import operators as ops
from .enums import direction


def evaluate(function, grid):
    """Evaluate a function on the grid points of the given grid

    function: has to take numpy arrays as arguments, f(x), f(y,x), f(z,y,x)
    grid: instance of dg.Grid
    return: flat np.array with x the fastest varying dimension. Can be reshaped
    with reshape(grid.shape)
    """
    ndim = grid.ndim
    xs = [create.abscissas(grid, dim) for dim in range(0, ndim)]

    if ndim == 1:
        return np.array([function(x) for x in xs[0]])
    if ndim == 2:
        return np.array([function(y, x) for y in xs[0] for x in xs[1]])
    if ndim == 3:
        return np.array(
            [function(z, y, x) for z in xs[0] for y in xs[1] for x in xs[2]]
        )
    if ndim == 4:
        return np.array(
            [
                function(xx, z, y, x)
                for xx in xs[0]
                for z in xs[1]
                for y in xs[2]
                for x in xs[3]
            ]
        )
    if ndim > 4:
        raise Exception("dg.evaluate is not implemented for ndim > 4")


def integrate(to_integrate, grid, direction=direction.forward):
    # python passes parameters "by assignment"
    if grid.ndim > 1:
        raise Exception("dg.integrate not implemented for ndim > 1")
    h = grid.h()[0]
    n = grid.n[0]
    to_in = to_integrate
    if direction == direction.backward:  # reverse input vector
        # https://stackoverflow.com/questions/6771428/most-efficient-way-to-reverse-a-numpy-array
        to_in = to_integrate[::-1]  # create a reversed view

    forward = ops.forward(n)
    backward = ops.backward(n)
    ninj = ops.ninj(n)
    t = ops.pipj_inv(n) * h / 2.0
    ninj = backward @ t @ ninj @ forward
    constant = 0.0

    out = np.zeros(grid.size())
    for i in range(0, grid.N[0]):
        for k in range(0, grid.n[0]):
            for ll in range(0, grid.n[0]):
                out[i * n + k] += ninj[k, ll] * to_in[i * n + ll]
            out[i * n + k] += constant
        for k in range(0, grid.n[0]):
            constant += h * forward[0, k] * to_in[i * n + k]
    if direction == direction.backward:  # reverse output
        out = -out[::-1]
    return out
