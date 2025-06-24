import scipy.sparse as sparse

from .. import enums
from .derivative import dx, jump


def elliptic(grid, bcs, directions, sigma, jumpfactor=1):
    left = [
        dx(i, grid, enums.inverse_bc(bcs[i]), enums.inverse_dir(directions[i]))
        for i in range(0, grid.ndim)
    ]
    right = [dx(i, grid, bcs[i], directions[i]) for i in range(0, grid.ndim)]
    jumps = [jump(i, grid, bcs[i]) for i in range(0, grid.ndim)]
    matrix = -left[0] @ sparse.diags(sigma) @ right[0] + jumpfactor * jumps[0]
    for i in range(1, grid.ndim):
        matrix += -left[i] @ sparse.diags(sigma) @ right[i] + jumpfactor * jumps[i]
    return matrix
