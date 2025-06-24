# pyFeltor
An implementation of [feltor](https://github.com/feltor-dev/feltor)'s discontinuous Galerkin 'dg' library in python.

[![LICENSE : MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


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

As a second addition, Feltor's geometries extension is available in python.
However, the geometries functions and classes are not re-implemented in python, but
they are bound to python via the [pybind11](https://github.com/pybind/pybind11)
library. As such the corresponding C++ binding code must be compiled in order
to generate the module `dg.geo`.
## Installation
> The `pyfeltor.dg.geo` part of the module contains python bindings for the underlying C++ [feltor](https://github.com/feltor-dev/feltor) code using [pybind11](https://github.com/pybind/pybind11). During installation the C++ code will be compiled using cmake, which may take a minute or two. 

The simplest way is to install from the python package index [pypi](https://pypi.org/) via the package manager [pip](https://pip.pypa.io/en/stable/) v23.0
```bash
python3 -m pip install pyfeltor
```

To install from github you have to clone the repository and then use the package manager [pip](https://pip.pypa.io/en/stable/) v23.0

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
Consider

- pyfeltor uses 1d numpy arrays as its vector class
- there is only one grid class `dg.Grid` that generalises `dg::Grid1d`,
  `dg::Grid2d` and `dg::Grid3d`
- Grids don't hold boundary conditions, these need to be provided in each
  function
- the evaluate function generates 1d (flat) numpy arrays that can be
  **reshaped** to 1d, 2d, 3d structure using `reshape(grid.shape)`
- the Grids do not name dimensions, only number them; the **last/rightmost**
  dimension is the one that varies fastest in memory (contrary to the C++
  library where the first dimension (x) varies fastest).
- the equivalent of the `dg::blas1` vector functions are just plain math
  operators with numpy arrays
- the equivalent of `dg::blas1::dot` and `dg::blas2::dot` is `np.sum`
- the derivative matrices are generated as `scipy.sparse` matrices
- the equivalent of `dg::blas::symv` is the `dot` method of scipy.sparse matrices
- The elliptic operator is a sparse matrix in pyfeltor (in contrast to a class) and is created by a function

### Grid generation, evaluation and integration

```python
import numpy as np

# import dg library
from pyfeltor import dg

n, Nx = 3, 12
grid = dg.Grid(x0=1, x1=2, n=n, N=Nx)
weights = dg.create.weights(grid)
func = dg.evaluate(lambda x: np.exp(x), grid)

sol = np.exp(2) - np.exp(1)
# the equivalent of dg::blas1::dot
num = np.sum(weights * func)
print(f"Correct integral is {sol} while numerical is {num}")
```

### Generate and use a derivative

```python
import numpy as np
from pyfeltor import dg

# We choose x as the second dimension here to make it vary in memory fastest
n, Nx, Ny = 3, 12, 24
g2d = dg.Grid(x0=[0.1, 0], x1=[2 * np.pi + 0.1, np.pi], n=[n, n], N=[Ny, Nx])
w2d = dg.create.weights(g2d)
f2d = dg.evaluate(lambda y, x: np.sin(x) * np.sin(y), g2d)
x2d = dg.evaluate(lambda y, x: np.cos(x) * np.sin(y), g2d)

# the x dimension is the rightmost (index 1)
dx = dg.create.dx(1, g2d, dg.bc.DIR, dg.direction.forward)
# and the y dimension is the leftmost (index 0)
dy = dg.create.dx(0, g2d, dg.bc.PER, dg.direction.centered)
error = dx.dot(f2d) - x2d
norm = np.sqrt(np.sum(w2d * error ** 2)) / np.sqrt(w2d * x2d ** 2)
print(f"Relative error to true solution: {norm}")
```

You can equally name x as the first dimension, then the y dimension
varies fastest in memory. Just keep it consistent.

### The elliptic operator

```python
from pyfeltor import dg
import numpy as np
import scipy.sparse.linalg
import scipy.linalg

amp = 0.9
pol = lambda y, x: 1 + amp * np.sin(x) * np.sin(y)
rhs = (
    lambda y, x: 2.0 * np.sin(x) * np.sin(y) * (amp * np.sin(x) * np.sin(y) + 1)
    - amp * np.sin(x) * np.sin(x) * np.cos(y) * np.cos(y)
    - amp * np.cos(x) * np.cos(x) * np.sin(y) * np.sin(y)
)
sol = lambda y, x: np.sin(x) * np.sin(y)
lx, ly = np.pi, 2 * np.pi
bcx, bcy = dg.bc.DIR, dg.bc.PER
n, Nx, Ny = 3, 64, 64
grid = dg.Grid([0, 0], [ly, lx], [n, n], [Ny, Nx])
x = np.zeros(grid.size())
b = dg.evaluate(rhs, grid)
chi = dg.evaluate(pol, grid)
solution = dg.evaluate(sol, grid)
# here we assemble the dg elliptic operator as a sparse matrix
pol_forward = dg.create.elliptic(
    grid,
    [bcy, bcx],
    [dg.direction.forward, dg.direction.forward],
    sigma=chi,
    jumpfactor=1,
)
# use a direct solver to solve linear equation
x = scipy.sparse.linalg.spsolve(pol_forward, b)

w2d = dg.create.weights(grid)
print("Distance to true solution is ", np.sqrt(np.sum(w2d * (x - solution) ** 2)))
```
### Interpolation

```python
from pyfeltor import dg
import numpy as np

print("2D INTERPOLATION TEST")

n, Nx, Ny = 3, 32, 32
g = dg.Grid(x0=[-5 * np.pi, -np.pi], x1=[-4 * np.pi, 0], n=[n, n], N=[Ny, Nx])
equi = dg.Grid(
    x0=[-5 * np.pi, -np.pi], x1=[-4 * np.pi, 0], n=[1, 1], N=[n * Ny, n * Nx]
)
y = dg.evaluate(lambda y, x: y, equi)
x = dg.evaluate(lambda y, x: x, equi)

interp = dg.create.interpolation([y, x], g, [dg.bc.DIR, dg.bc.DIR])
vec = dg.evaluate(lambda y, x: np.sin(x) * np.sin(y), g)
inter = interp.dot(vec)
interE = dg.evaluate(lambda y, x: np.sin(x) * np.sin(y), equi)
error = np.sum((inter - interE) ** 2) / np.sum(inter ** 2)
print(f"Error is {np.sqrt(error)} (should be small)!")
```

## The dg.geo module
Currently the `dg.geo` module binds all classes and functions available
in Modules 3 and 5 in [the documentation](https://mwiesenberger.github.io/feltor/geometries/html/modules.html).
Since the interface is now the same, the C++ documentation applies exactly to the python module as well.
Only a few caveats need to be considered:

- in all derivatives of `dg::geo::aCylindricalFunctor` only the 2 dimensional
  version of `operator()` is currently bound
- in all derivatives of `dg::geo::aCylindricalFunctor` the
  `operator()` is vectorized, i.e. can be called on a numpy array
- function or member parameters that are of type `dg::file::WrappedJsonValue`
  on the C++ code are simple python dictionaries on the python side (arrays
  need to be lists though)
- functions or members with parameters from the original `dg` library (e.g.
  `dg::Grid2d`) are currently not bound (except `dg::geo::createSheathRegion`).
- python does not support non-const double reference arguments (e.g. `double& R`)
  [see this FAQ entry on pybind11](https://pybind11.readthedocs.io/en/stable/faq.html#limitations-involving-reference-arguments)
  In the cases when it occurs we append these variables as a tuple to the
  return value of the function (for example in `dg.geo.findOpoint`, see the
  examples below)

### Generating simple flux functions
A first application is to generate a flux function and evaluating it like so
```python
from pyfeltor import dg
params = {c = np.array( [1,2,3,4])
params = {"R_0" : 400, "inverseaspectratio" : 20, "elongation" : 1, "triangularity" : 1,
          "PP" : 1, "PI" : 1, "description" : "standardX", "M" : 2, "N" : 2, "c" : c.tolist()}
pp = dg.geo.polynomial.Parameters(params)
psip = dg.geo.polynomial.Psip(pp)
grid = dg.Grid( x0 = (pp.R_0-pp.a, -pp.a), x1 = (pp.R_0+pp.a, pp.a), n=(3,3), N=(24, 24))
psi = dg.evaluate( psip, grid)
```
As an application in
[magneticfieldb](https://github.com/feltor-dev/magneticfielddb)
you can see a polynomial flux function being fitted to an experimental field.

### Generating the magnetic field and magnetic field functions
In this second example we look how we can use a json magnetic field
file to generate the magnetic field for us:

```python
from pyfeltor import dg
with open ("geometry_params_Xpoint.json", "r") as f:
    magparams = json.load(f)
mag = dg.geo.createMagneticField( magparams)
RO,ZO  = mag.R0(), 0
(point, RO, ZO) = dg.geo.findOpoint(mag.get_psip(), RO, ZO)
print( "O-point found at ", RO, ZO)
a = mag.params().a()
R0 = mag.R0()
grid = dg.Grid(x0=(R0-a, -a), x1=(R0+a, +a), n=(3, 3), N=(24, 24))
psi = dg.evaluate( mag.psip(), grid)
BR  = dg.evaluate( dg.geo.BFieldR(mag), grid)
BZ  = dg.evaluate( dg.geo.BFieldZ(mag), grid)
# ... the list of possible functions is large ...
# Since the functions can be evaluated using numpy arrays this also works
R = dg.evaluate( lambda R, Z: R, grid)
Z = dg.evaluate( lambda R, Z: Z, grid)
BP = dg.geo.BFieldP(mag)(R,Z)
# go on to plot with matplotlib ...
```

### Generating q-profile
A common task is to generate a q-profile. This can be done like so:

```python
with open ("enrx_tcv.json", "r") as f:
    magparams = json.load(f)
mag = dg.geo.createMagneticField(magparams)
qfunctor = dg.geo.SafetyFactor(mag)
RO,ZO  = mag.R0(), 0
(point, RO, ZO) = dg.geo.findOpoint(mag.get_psip(), RO, ZO)
print( "O-point found at ", RO, ZO)
psipO = mag.psip()(RO,ZO)
grid = dg.Grid( psipO, 0, 3, 64)
qprof = dg.evaluate( qfunctor, grid)
print(qprof)
```

## Contributions

Contributions are welcome.

## Authors

Matthias Wiesenberger
