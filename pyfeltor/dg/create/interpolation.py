import itertools

import numpy as np
import scipy.sparse

from ..enums import bc
from ..evaluation import evaluate
from . import operators as ops
from .weights import weights


def shift(grid, x, bcs):
    """ Shift a point into the grid according to boundary conditions
        (used internally by interpolation)
    """
    negative = False
    for i in range(0, grid.ndim):
        if bcs[i] == bc.PER:
            N = np.floor(
                (x[i] - grid.x0[i]) / (grid.x1[i] - grid.x0[i])
            )  # ... -2[ -1[ 0[ 1[ 2[ ...
            x[i] = x[i] - N * (grid.x1[i] - grid.x0[i])  # shift
        # mirror along boundary as often as necessary
        while (x[i] < grid.x0[i]) or (x[i] > grid.x1[i]):
            if x[i] < grid.x0[i]:
                x[i] = 2.0 * grid.x0[i] - x[i]
                # every mirror swaps the sign if Dirichlet
                if (bcs[i] == bc.DIR) or (bcs[i] == bc.DIR_NEU):
                    negative = not negative  # swap sign
            if x[i] > grid.x1[i]:
                x[i] = 2.0 * grid.x1[i] - x[i]
                if (bcs[i] == bc.DIR) or (bcs[i] == bc.NEU_DIR):
                    # notice the different boundary NEU_DIR to the above DIR_NEU !
                    negative = not negative  # swap sign
    return negative, x


def interpolation(xs, grid, bcs):
    """ interpolation matrix that evaluate points on given grid

        order is xs = [... z, y, x]
    """

    rows = []
    cols = []
    vals = []
    forward = [ops.forward(grid.n[dim]) for dim in range(0, grid.ndim)]

    for i in range(0, len(xs[0])):
        X = np.array([xs[k][i] for k in range(0, grid.ndim)])
        negative, X = shift(grid, X, bcs)
        xnn = (X - grid.x0) / grid.h()
        nn = np.floor(xnn)
        xn = 2.0 * xnn - (2 * nn + 1)
        for k in range(0, grid.ndim):
            if nn[k] == grid.N[k]:
                nn[k] -= 1
                xn[k] = 1

        # evaluate Legendre polynomials at (xn)...
        px = [
            (
                np.polynomial.legendre.legvander(xn[k], grid.n[k] - 1) @ forward[k]
            ).ravel()
            for k in range(0, grid.ndim)
        ]

        # generate the list of index permutations
        tuples = []
        if grid.ndim == 1:
            tuples = [(a,) for a in range(0, grid.n[0])]
        elif grid.ndim == 2:
            tuples = itertools.product(range(0, grid.n[0]), range(0, grid.n[1]))
        elif grid.ndim == 3:
            tuples = itertools.product(
                range(0, grid.n[0]), range(0, grid.n[1]), range(0, grid.n[2])
            )
        else:
            raise Exception("interpolation not implemented for ndim > 3")
        for it in tuples:
            II = 0  # the index to push back
            VV = 1  # the value to push back
            for kk in range(0, grid.ndim):
                II = (II * grid.N[kk] + nn[kk]) * grid.n[kk] + it[kk]
                VV = VV * px[kk][it[kk]]
            # print( i, I, V)
            rows.append(i)
            cols.append(round(II))
            if not negative:
                vals.append(VV)
            else:
                vals.append(-VV)
    # sort
    rows, cols, vals = zip(*sorted(zip(rows, cols, vals, strict=False)), strict=False)
    return scipy.sparse.coo_matrix((vals, (rows, cols)), shape=(len(xs[0]),
        grid.size()))


def projection(grid_new, grid_old):
    """ Create a projection between two grids

    This matrix can be applied to vectors defined on the old (fine) grid to obtain
    its values projected on the new (coarse) grid. (Projection means that the
    projection integrals over the base polynomials are computed).
    The projection matrix is the adjoint of the interpolation matrix
    params:
    g_new : The new (coarse) grid
    g_old : The old (fine) grid
    """
    ndim = grid_old.ndim
    if grid_new.ndim != ndim:
        raise Exception("Cannot project between grids with different dimensions")
    for i in range(0, ndim):
        if grid_old.N[i] % grid_new.N[i] != 0:
            print(f"WARNING you project between incompatible grids!! old N: \
{grid_old.N[i]} new N {grid_new.N[i]}")
        if grid_old.n[i] < grid_new.n[i]:
            print(f"WARNING you project between incompatible grids!! old n: \
{grid_old.n[i]} new n {grid_new.n[i]}")
    wf = scipy.sparse.diags(weights(grid_old))
    points = []
    bcs = [bc.PER for i in range(0, ndim)]
    if ndim == 1:
        points.append(evaluate(lambda x: x, grid_old))
    elif ndim == 2:
        points.append(evaluate(lambda y, x: y, grid_old))
        points.append(evaluate(lambda y, x: x, grid_old))
    elif ndim == 3:
        points.append(evaluate(lambda z, y, x: z, grid_old))
        points.append(evaluate(lambda z, y, x: y, grid_old))
        points.append(evaluate(lambda z, y, x: x, grid_old))
    else:
        raise Exception("Projection not implemented for ndim > 3")
    A = interpolation(points, grid_new, bcs)
    vc = scipy.sparse.diags(1. / weights(grid_new))
    return vc @ A.transpose() @ wf
