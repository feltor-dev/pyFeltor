# pyFeltor
An implementation of feltor's dg library in python

[![LICENSE : MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Rationale

In order to analyse Feltor simulations python has turned out to be an invaluable tool.
However, it is currently not possible to compute a dG derivative inside python once a
field is loaded from a netCDF file. All diagnostics therefore have to be
written by the simulation code and an extension involves writing the new
diagnostics, re-compilation of code and a re-simulation of the result. This is
a too costly interruption of the workflow for a simple task. The initial goal for this package is
to provide the dG derivatives as they are used inside the dg library as well
as other quality of life functions like weights, grids and the evaluate
functions. In fact, since many numerical packages are available
through python this enables many applications beyond simple simulations
diagnostics. The only downside is of course that all functions are
unparallelized in python.

## Installation
> You need python3 to install this module

The simplest way is to install from the python package index [pypi](https://pypi.org/) via the package manager [pip](https://pip.pypa.io/en/stable/):
```bash
python3 -m pip install pyfeltor
```

To install from github you have to clone the repository and then use the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
git clone https://github.com/feltor-dev/pyfeltor
cd pyfeltor
python3 -m pip install -e . # editable installation of the module
# ... if asked, cancel all password prompts ...
cd tests
pytest-3 -s . # run all the unittests with output
```

## Usage

Generally, pyfeltor is built to mimic the `dg` library in feltor.
There are a few things to consider
- pyfeltor uses 1d numpy arrays as its vector class
- there is only one grid class `dg.Grid` that generalises `dg::Grid1d`,
  `dg::Grid2d` and `dg::Grid3d`
- the evaluate function generates 1d (flat) numpy arrays that can be **reshaped**
    to 1d, 2d, 3d structure using `reshape(grid.shape)`
- the x dimension is the **last/rightmost** dimension (row-major/C-style layout)
- the equivalent of the `dg::blas1` vector functions are just plain math
  operators with numpy arrays
- the equivalent of `dg::blas1::dot` and `dg::blas2::dot` is `np.sum`
- the derivative matrices are generated as `scipy.sparse` matrices
- the equivalent of `dg::blas::symv` is the `dot` method of scipy.sparse matrices

Here is how the grid generation, evaluation and integration works
```python
import numpy as np
# import dg library
from pyfeltor import dg

n, Nx = 3, 12
grid = dg.Grid( [1],[2],[n], [Nx], [dg.bc.PER])
weights = dg.create.weights( grid)
func = dg.evaluate( lambda x : np.exp(x), grid)

sol = np.exp(2)-np.exp(1)
# the equivalent of dg::blas1::dot
num = np.sum( weights*func)
print( f"Correct integral is {sol} while numerical is {num}")

```
Here is an example of how to generate and use a derivative
```python
import numpy as np
from pyfeltor import dg

# !! The x dimension is the second one !!
g2d = dg.Grid([0.1, 0], [2 * np.pi + 0.1, np.pi], [n, n], [Ny, Nx], [bcy, bcx])
w2d = dg.create.weights(g2d)
f2d = dg.evaluate(sine, g2d)
x2d = dg.evaluate(cosx, g2d)

# the x dimension is the rightmost (index 1)
dx = dg.create.dx(1, g2d, g2d.bc[1], dg.direction.forward)
# and the y dimension is the leftmost (index 0)
dy = dg.create.dx(0, g2d, g2d.bc[0], dg.direction.centered)
error = dx.dot(f2d) - x2d
norm = np.sqrt(np.sum(w2d * error**2)) / np.sqrt(w2d * x2d ** 2)
print(f"Relative error to true solution: {norm}")

```


