import scipy.sparse

from .dx import jump_normed, normed


def dx(dim, grid, bc, direction):
    deriv = normed(grid.n[dim], grid.N[dim], grid.h()[dim], bc, direction)
    if grid.ndim == 1:
        return deriv
    for d in range(0, grid.ndim):
        if d != dim:
            identity = scipy.sparse.identity(grid.n[d] * grid.N[d])
            if d < dim:
                deriv = scipy.sparse.kron(identity, deriv)
            else:
                deriv = scipy.sparse.kron(deriv, identity)
    return deriv


def jump(dim, grid, bc):
    deriv = jump_normed(grid.n[dim], grid.N[dim], grid.h()[dim], bc)
    if grid.ndim == 1:
        return deriv
    for d in range(0, grid.ndim):
        if d != dim:
            identity = scipy.sparse.identity(grid.n[d] * grid.N[d])
            if d < dim:
                deriv = scipy.sparse.kron(identity, deriv)
            else:
                deriv = scipy.sparse.kron(deriv, identity)
    return deriv
