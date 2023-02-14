import numpy as np
from .derivative import dx, jump
from .. import enums
import scipy.sparse as sparse
from ..utility import dot


def elliptic(grid, bcs, directions, sigma, jumpfactor=1):
    left = [
        dx(i, grid, enums.inverse_bc(bcs[i]), enums.inverse_dir(directions[i]))
        for i in range(0, grid.ndim)
    ]
    right = [dx(i, grid, bcs[i], directions[i]) for i in range(0, grid.ndim)]
    jumps = [jump(i, grid, bcs[i]) for i in range(0, grid.ndim)]
    matrix = -left[0].dot(sparse.diags(sigma)).dot(right[0]) + jumpfactor * jumps[0]
    for i in range(1, grid.ndim):
        matrix += (
            -left[i].dot(sparse.diags(sigma)).dot(right[i]) + jumpfactor * jumps[i]
        )
    return matrix
