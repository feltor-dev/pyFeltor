import numpy as np

from pyfeltor import dg

# Run with pytest-3 -s . to see stdout output


def test_grid():
    print("TEST GRID")
    g1d = dg.Grid(x0=1, x1=2, n=3, N=24)
    print(g1d.x0, g1d.x1, g1d.n, g1d.N)
    assert g1d.ndim == 1
    g2d = dg.Grid(x0=(0, 0), x1=(1, 1), n=(3, 3), N=(24, 24))
    print(g2d.x0, g2d.x1, g2d.n, g2d.N)
    assert g2d.ndim == 2
    assert g2d.size() == 5184


def test_creation():
    print("TEST CREATION")
    grid = dg.Grid(x0=(0, 0), x1=(1, 1), n=(3, 3), N=(24, 24))
    weights = dg.create.weights(grid)
    print(weights)


def test_evaluation():
    print("TEST EVALUATION")
    grid = dg.Grid(x0=(0, 0), x1=(np.pi, np.pi), n=(3, 3), N=(24, 24))
    weights = dg.create.weights(grid)
    sine = dg.evaluate(lambda y, x: np.sin(y) * np.sin(x), grid)
    print(f"Integral is {np.sum(sine * weights)}")


def test_grid_from_abscissas():
    print("TEST REVERSE GRID ENGINEER")
    grid = dg.Grid(x0=(-10, 0, 20, -10, 0, 20), x1=(2 * np.pi, np.pi, 10 * np.pi,
        2 * np.pi, np.pi, 10 * np.pi), n=(1, 2, 3, 4, 5, 6), N=(20, 24, 12, 13, 15, 16))
    xs = [dg.create.abscissas(grid, i) for i in range(0, grid.ndim)]
    test_grid = dg.create.grid_from_abscissas(xs)

    print(grid.x0, grid.x1, grid.n, grid.N)
    print(test_grid.x0, test_grid.x1, test_grid.n, test_grid.N)
    assert np.allclose(grid.x0, test_grid.x0)
    assert np.allclose(grid.x1, test_grid.x1)
    assert np.allclose(grid.n, test_grid.n)
    assert np.allclose(grid.N, test_grid.N)
