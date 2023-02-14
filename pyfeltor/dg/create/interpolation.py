import numpy as np
import itertools
import scipy.sparse
from . import operators as ops
from ..enums import bc, direction


def shift(grid, x, bcs):
    """ Shift a point into the grid according to boundary conditions
        (used internally by interpolation)
    """
    negative = False
    for i in range( 0, grid.ndim):
        if( bcs[i] == bc.PER):
            N = np.floor((x[i]-grid.x0[i])/(grid.x1[i]-grid.x0[i])) # ... -2[ -1[ 0[ 1[ 2[ ...
            x[i] = x[i] - N*(grid.x1[i]-grid.x0[i]) # shift
        # mirror along boundary as often as necessary
        while( (x[i]<grid.x0[i]) or (x[i]>grid.x1[i]) ):
            if( x[i] < grid.x0[i]):
                x[i] = 2.*grid.x0[i] - x[i];
                # every mirror swaps the sign if Dirichlet
                if( (bcs[i] == bc.DIR) or (bcs[i] == bc.DIR_NEU)):
                    negative = not negative # swap sign
            if( x[i] > grid.x1[i]):
                x[i] = 2.*grid.x1[i] - x[i]
                if( (bcs[i] == bc.DIR) or (bcs[i] == bc.NEU_DIR)):
                    # notice the different boundary NEU_DIR to the above DIR_NEU !
                    negative = not negative # swap sign
    return negative, x


def interpolation( xs, grid, bcs):
    """ interpolation matrix that evaluate points on given grid

        order is ... z y x
    """

    rows = []
    cols = []
    vals = []
    forward = [ops.forward( grid.n[dim]) for dim in range(0,grid.ndim)]

    for i in range(0, len( xs[0])):
        X = np.array([xs[k][i] for k in range(0,grid.ndim)])
        negative, X = shift( grid, X, bcs)
        xnn = (X - grid.x0)/grid.h()
        nn = np.floor( xnn)
        xn = 2.0*xnn - (2*nn+1)
        for k in range( 0, grid.ndim):
            if nn[k] == grid.N[k]:
                nn[k] -= 1
                xn[k] = 1

        # evaluate Legendre polynomials at (xn)...
        px = [(np.polynomial.legendre.legvander( xn[k], grid.n[k]-1) @ forward[k]).ravel() for k in range( 0, grid.ndim)]

        # generate the list of index permutations
        tuples = range(0,grid.n[0])
        if grid.ndim == 1:
            tuples = [(a,) for a in tuples]
        for k in range( 1, grid.ndim):
            tuples = itertools.product( tuples, range( 0, grid.n[k]))
            if k > 1:
                tuples = [(a,b,c) for (a,b),c in tuples]
            
        for it in tuples:
            I = 0 # the index to push back
            V = 1 # the value to push back
            for kk in range( 0, grid.ndim):
                I = ((I*grid.N[kk] + nn[kk])*grid.n[kk] + it[kk])
                V = V*px[kk][it[kk]]
            #print( i, I, V)
            rows.append(i)
            cols.append(round(I))
            if not negative :
                vals.append( V)
            else :
                vals.append(-V)
    # sort
    rows, cols, vals = zip(*sorted(zip(rows, cols, vals)))
    return scipy.sparse.coo_matrix((vals, (rows, cols)))
