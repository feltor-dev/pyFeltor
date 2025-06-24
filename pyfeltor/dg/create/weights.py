import numpy as np

from ..grid import Grid


def weights(grid):
    """Create dG weights on given grid"""
    weights = np.array([1])
    for dim in range(0, grid.ndim):
        (x, w) = np.polynomial.legendre.leggauss(grid.n[dim])
        wdim = np.tile(w, grid.N[dim]) * grid.h()[dim] / 2.0
        weights = np.kron(weights, wdim)
        # weights = np.reshape(weights, grid.shape[0 : dim + 1])
    return weights


def abscissas(grid, dimension=0):
    """Create 1d dG abscissas on given grid for given dimension"""
    dim = dimension
    (x, w) = np.polynomial.legendre.leggauss(grid.n[dim])
    abscissas = np.zeros(grid.shape[dim])
    h = grid.h()[dim]
    x0 = grid.x0[dim]
    for i in range(0, grid.N[dim]):
        for k in range(0, grid.n[dim]):
            abscissas[i * grid.n[dim] + k] = i * h + x0 + h / 2.0 * (1.0 + x[k])
    return abscissas


def _get_x0_x1_n_N(x):
    for n in range(1, 21):
        if len(x) % n != 0:
            continue
        N = len(x) / n
        (xx, w) = np.polynomial.legendre.leggauss(n)
        h = x[n] - x[0]
        x0 = x[0] - h / 2.0 * (1.0 + xx[0])
        first_absc = np.zeros(2 * n)
        last_value = x0 + h * N - h / 2.0 * (1.0 + xx[0])
        for i in range(0, 2):
            for k in range(0, n):
                first_absc[i * n + k] = i * h + x0 + h / 2.0 * (1.0 + xx[k])
        if abs(last_value - x[-1]) < 1e-10 * abs(x[-1]) + 1e-10:
            return (x0, x0 + h * N, int(n), int(N))
    raise Exception("Could not determine grid")
    return (0, 1, 1, 1)


def grid_from_abscissas(xs):
    """ This function reverse engineers a Grid that corresponds to the given
    abscissas. This is useful for example to get a Grid that corresponds to a
    given simulation output

    xs(list of 1d arrays): the length of the list is ndim. Last entry
        is the x-dimension. Each entry is a 1d array corresponding to the abscissas
        in that dimension. At least two cells need to be present.
    Return: Grid whose abscissas correspond to xs
    """
    ndim = len(xs)
    x0 = np.zeros(ndim)
    x1 = np.zeros(ndim)
    n = np.arange(ndim)
    N = np.arange(ndim)
    for dim in range(0, ndim):
        x0[dim], x1[dim], n[dim], N[dim] = _get_x0_x1_n_N(xs[dim])
    return Grid(x0, x1, n, N)
