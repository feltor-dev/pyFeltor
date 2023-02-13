from evaluation import evaluate
from grid import Grid
from enums import bc

# from create.weights import abscissas, weights
import create
import numpy as np

grid = Grid(x0=(0, 0), x1=(np.pi, np.pi), n=(3, 3), N=(24, 24), bc=(bc.PER, bc.DIR))
weights = create.weights(grid)
sine = evaluate(lambda y, x: np.sin(y) * np.sin(x), grid)
