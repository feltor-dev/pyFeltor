import numpy as np
import scipy.linalg
import scipy.sparse.linalg

from pyfeltor import dg


def test_elliptic():
    amp = 0.9
    def pol(y, x):
        return 1 + amp * np.sin(x) * np.sin(y)
    def rhs(y, x):
        return 2.0 * np.sin(x) * np.sin(y) * (amp * np.sin(x) * np.sin(y) + 1)\
            - amp * np.sin(x) * np.sin(x) * np.cos(y) * np.cos(y)\
            - amp * np.cos(x) * np.cos(x) * np.sin(y) * np.sin(y)
    def sol(y,x):
        return np.sin(x) * np.sin(y)
    lx, ly = np.pi, 2 * np.pi
    bcx, bcy = dg.bc.DIR, dg.bc.PER
    n, Nx, Ny = 3, 64, 64
    jfactor = 1
    grid = dg.Grid([0, 0], [ly, lx], [n, n], [Ny, Nx])
    w2d = dg.create.weights(grid)
    x = np.zeros(grid.size())
    b = dg.evaluate(rhs, grid)
    chi = dg.evaluate(pol, grid)
    solution = dg.evaluate(sol, grid)
    print("Forward elliptic ")
    pol_forward = dg.create.elliptic(
        grid,
        [bcy, bcx],
        [dg.direction.forward, dg.direction.forward],
        sigma=chi,
        jumpfactor=jfactor,
    )
    error = pol_forward.dot(solution) - b
    print(
        "Direct application of laplace to solution is",
        np.sqrt(np.sum(w2d * error ** 2)),
    )
    assert np.isclose(np.sqrt(np.sum(w2d * error ** 2)), 0.07475654581481737)
    x = scipy.sparse.linalg.spsolve(pol_forward, b)

    print("Distance to true solution is ", np.sqrt(np.sum(w2d * (x - solution) ** 2)))


def test_elliptic1d():
    print("TEST 1d ELLIPTIC")
    grid1d = dg.Grid([0], [np.pi], [3], [4])
    w1d = dg.create.weights(grid1d)
    x = np.zeros(grid1d.size())
    b = dg.evaluate(lambda x: np.sin(x), grid1d)
    chi = np.ones(grid1d.size())
    solution1d = dg.evaluate(lambda x: np.sin(x), grid1d)
    pol_backward = dg.create.elliptic(
        grid1d, [dg.bc.DIR], [dg.direction.backward], sigma=chi, jumpfactor=1
    )
    x = pol_backward.dot(solution1d) - b
    assert np.isclose(np.sqrt(np.sum(w1d * x ** 2)), 0.28502509566157097)
