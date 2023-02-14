import pytest
import numpy as np
from pyfeltor import dg

# Run with pytest-3 -s . to see stdout output


def function2d(y, x):
    rho = 0.20943951023931953  # pi/15
    delta = 0.050000000000000003
    # return np.where(

    if y <= np.pi:
        return delta * np.cos(x) - 1.0 / rho / np.cosh(
            (y - np.pi / 2.0) / rho
        ) / np.cosh((y - np.pi / 2.0) / rho)
    else:
        return delta * np.cos(x) + 1.0 / rho / np.cosh(
            (3.0 * np.pi / 2.0 - y) / rho
        ) / np.cosh((3.0 * np.pi / 2.0 - y) / rho)


def test_evaluation():
    n, Nx, Ny, Nz = 3, 9, 5, 4
    equi = dg.Grid([-7, -5, -10], [-3, 5, 10], [1, 1, 1], [n * Nz, n * Ny, n * Nx])
    z = dg.evaluate(lambda z, y, x: z * x, equi)
    y = dg.evaluate(lambda z, y, x: y, equi)
    x = dg.evaluate(lambda z, y, x: x, equi)
    print("Length of arrays", len(z), len(y), len(x))
    assert (len(z) == grid.size())
    assert (len(y) == grid.size())
    assert (len(x) == grid.size())


def test_integration():
    n = 3
    Nx = 12
    Ny = 28
    Nz = 100
    g1d = dg.Grid([1], [2], [n], [Nx])
    g2d = dg.Grid((0, 0), (2 * np.pi, 2 * np.pi), (n, n), (Ny, Nx))
    w1d = dg.create.weights(g1d)
    w2d = dg.create.weights(g2d)
    func1d = dg.evaluate(lambda x: np.exp(x), g1d)
    func2d = dg.evaluate(function2d, g2d)

    sol1d = np.exp(2) - np.exp(1)
    num1d = np.sum(w1d * func1d)
    print(f"Correct integral is {sol1d} while numerical is {num1d}")
    assert np.abs(sol1d - num1d) / sol1d < 1e-10

    sol2d = 0.0
    num2d = np.sum(w2d * func2d)
    print(f"Correct integral is {sol2d} while numerical is {num2d}")
    assert np.abs(sol2d - num2d) < 1e-10
