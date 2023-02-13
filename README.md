# pyfeltor
An implementation of feltor in python


There are a few things to watch out for
- there is only one grid class `dg.Grid` that generalises `dg::Grid1d`, `dg::Grid2d` and `dg::Grid3d`
- the x dimension is the **last/rightmost** dimension

Here is how the grid generation, evaluation and integration works
```python
import numpy as np
from pyfeltor import dg

def function2d( y, x): # x comes last
    rho = 0.20943951023931953 # pi/15
    delta = 0.050000000000000003
    return np.where( y <= np.pi,
        delta*np.cos(x) - 1./rho/np.cosh( (y-np.pi/2.)/rho)/np.cosh( (y-np.pi/2.)/rho),
        delta*np.cos(x) + 1./rho/np.cosh( (3.*np.pi/2.-y)/rho)/np.cosh( (3.*np.pi/2.-y)/rho))

n = 3
Nx = 12
Ny = 28
Nz = 100
g1d = dg.Grid( [1],[2],[n], [Nx], [dg.bc.PER])
g2d = dg.Grid( (0,0),(2*np.pi, 2*np.pi),(n,n), (Ny,Nx), (dg.bc.PER,dg.bc.PER)) # first y then x!!
w1d = dg.create.weights( g1d)
w2d = dg.create.weights( g2d)
func1d = dg.evaluate( lambda x : np.exp(x), g1d)
func2d = dg.evaluate( function2d, g2d)

sol1d = np.exp(2)-np.exp(1)
num1d = np.sum( w1d*func1d)
print( f"Correct integral is {sol1d} while numerical is {num1d}")
assert np.abs(sol1d - num1d)/sol1d < 1e-10

sol2d = 0.
num2d = np.sum( w2d*func2d)
print( f"Correct integral is {sol2d} while numerical is {num2d}")
assert np.abs(sol2d - num2d) < 1e-10

```

In order to compute derivatives we use the `scipy.sparse` package
```python
import numpy as np
from pyfeltor import dg

g2d = dg.Grid([0.1, 0], [2 * np.pi + 0.1, np.pi], [n, n], [Ny, Nx], [bcy, bcx])
w2d = dg.create.weights(g2d)
f2d = dg.evaluate(sine, g2d)
x2d = dg.evaluate(cosx, g2d)

# Remember that the x dimension is the rightmost
dx = dg.create.dx(1, g2d, g2d.bc[1], dg.direction.forward)
# and the y dimension is the leftmost
dy = dg.create.dx(0, g2d, g2d.bc[0], dg.direction.centered)
error = dx.dot(f2d) - x2d
norm = np.sqrt(np.sum(w2d * error**2)) / np.sqrt(w2d * x2d ** 2)
print(f"Relative error to true solution: {norm}")

```


