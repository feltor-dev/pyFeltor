from . import dx
import scipy.sparse

def derivative( dim, grid, bc, direction):
    deriv = dx.normed( grid.n[dim], grid.N[dim], grid.h()[dim], bc, direction)
    if ( grid.ndim == 1):
        return deriv
    for d in range( 0, grid.ndim):
        if d != dim:
            identity = scipy.sparse.identity( grid.n[dim]*grid.N[dim])
            if d < dim :
                deriv = scipy.sparse.kron(identity, deriv)
            else :
                deriv = scipy.sparse.kron(deriv, identity)
    return deriv

def jump( dim, grid, bc):
    deriv = dx.jump_normed( grid.n[dim], grid.N[dim], grid.h()[dim], bc)
    if ( grid.ndim == 1):
        return deriv
    for d in range( 0, grid.ndim):
        if d != dim:
            identity = scipy.sparse.identity( grid.n[dim]*grid.N[dim])
            if d < dim :
                deriv = scipy.sparse.kron(identity, deriv)
            else :
                deriv = scipy.sparse.kron(deriv, identity)
    return deriv
