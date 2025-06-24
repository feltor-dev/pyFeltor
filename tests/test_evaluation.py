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
    assert len(z) == equi.size()
    assert len(y) == equi.size()
    assert len(x) == equi.size()


def test_integration():
    n = 3
    Nx = 12
    Ny = 28
    g1d = dg.Grid(x0=1, x1=2, n=n, N=Nx)
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


def test_integrate():
    print("TEST OF dg.integrate")
    g1d = dg.Grid([1], [2], [3], [12])
    w1d = dg.create.weights(g1d)
    integral_num = dg.integrate(
        dg.evaluate(lambda x: np.cos(x), g1d), g1d, dg.direction.forward
    )
    integral_ana = dg.evaluate(lambda x: np.sin(x), g1d) - np.sin(g1d.x0[0])
    error = integral_ana - integral_num
    norm = np.sum(w1d * error ** 2)
    print(" Error norm of  1d integral function (forward) ", norm)
    assert np.isclose(norm, 0)
    integral_num = dg.integrate(
        dg.evaluate(lambda x: np.cos(x), g1d), g1d, dg.direction.backward
    )
    integral_ana = dg.evaluate(lambda x: np.sin(x), g1d) - np.sin(g1d.x1[0])
    error = integral_ana - integral_num
    norm = np.sum(w1d * error ** 2)
    print(" Error norm of  1d integral function (backward) ", norm)
    assert np.isclose(norm, 0)
