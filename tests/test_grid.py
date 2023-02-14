import pytest
import numpy as np
from pyfeltor import dg

# Run with pytest-3 -s . to see stdout output


def test_grid():
    print("TEST GRID")
    g1d = dg.Grid([1], [2], [3], [24], [dg.bc.PER])
    print(g1d.x0, g1d.x1, g1d.n, g1d.N, g1d.bc)
    assert g1d.ndim == 1
    g2d = dg.Grid(x0=(0, 0), x1=(1, 1), n=(3, 3), N=(24, 24), bc=(dg.bc.PER, dg.bc.DIR))
    print(g2d.x0, g2d.x1, g2d.n, g2d.N, g2d.bc)
    assert g2d.ndim == 2
    assert g2d.size() == 5184


def test_creation():
    print("TEST CREATION")
    grid = dg.Grid(
        x0=(0, 0), x1=(1, 1), n=(3, 3), N=(24, 24), bc=(dg.bc.PER, dg.bc.DIR)
    )
    weights = dg.create.weights(grid)
    print(weights)


def test_evaluation():
    print("TEST EVALUATION")
    grid = dg.Grid(
        x0=(0, 0), x1=(np.pi, np.pi), n=(3, 3), N=(24, 24), bc=(dg.bc.PER, dg.bc.DIR)
    )
    weights = dg.create.weights(grid)
    sine = dg.evaluate(lambda y, x: np.sin(y) * np.sin(x), grid)
    print(f"Integral is {np.sum( sine*weights)}")
