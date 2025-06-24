import numpy as np

from pyfeltor import dg


def test_interpolation1d():
    print("1D INTERPOLATION TEST")
    passed = True
    n, Nx = 3, 9
    g1d = dg.Grid(-np.pi, 0, n, Nx)
    field = dg.evaluate(lambda x: x, g1d)
    x = [(i + 0.5) * g1d.h()[0] / g1d.n[0] for i in range(0, g1d.size())]

    interp = dg.create.interpolation([x], g1d, [dg.bc.DIR])
    x_inter = interp.dot(field)
    for i in range(g1d.size()):
        if x[i] - x_inter[i] > 1e-14:
            print(f"X NOT EQUAL {i}\t{x[i]}  \t{x_inter[i]}")
            passed = False
    assert passed


def test_interpolation2d():
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
    assert np.isclose(np.sqrt(error), 0, atol=1e-5)


def test_interpolation3d():
    print("3D INTERPOLATION TEST")
    n, Nx, Ny, Nz = 3, 9, 5, 4

    g = dg.Grid([-7, -5, -10], [-3, 5, 10], [1, n, n], [Nz, Ny, Nx])
    equi = dg.Grid([-7, -5, -10], [-3, 5, 10], [1, 1, 1], [1 * Nz, n * Ny, n * Nx])
    z = dg.evaluate(lambda z, y, x: z, equi)
    y = dg.evaluate(lambda z, y, x: y, equi)
    x = dg.evaluate(lambda z, y, x: x, equi)

    interp = dg.create.interpolation([z, y, x], g, [dg.bc.DIR, dg.bc.DIR, dg.bc.PER])
    vec = dg.evaluate(lambda z, y, x: np.sin(x) * np.sin(y) * np.sin(z), g)
    inter = interp.dot(vec)
    # These values are from interpolation_t.cu
    solution = np.array(
        [
            -0.0388107,
            0.108781,
            0.200279,
            0.188096,
            0.07971,
            -0.0697783,
            -0.189282,
            -0.20544,
            -0.115663,
            0.0414357,
        ]
    )
    print("Pointwise error ", inter[0:10] - solution)
    assert np.allclose(inter[0:10], solution)


def test_projection():
    print("2D PROJECTION TEST")

    n, Nx, Ny = 3, 8, 8
    g = dg.Grid(x0=[-5 * np.pi, -np.pi], x1=[-4 * np.pi, 0], n=[n, n], N=[Ny, Nx])
    g_fine = dg.Grid(x0=g.x0, x1=g.x1, n=g.n, N=[n * Ny, n * Nx])

    project = dg.create.projection(g, g_fine)
    vec = dg.evaluate(lambda y, x: np.sin(x) * np.sin(y), g_fine)
    project = project.dot(vec)
    projectE = dg.evaluate(lambda y, x: np.sin(x) * np.sin(y), g)
    error = np.sum((project - projectE) ** 2) / np.sum(project ** 2)
    print(f"Error is {np.sqrt(error)} (should be small)!")
    assert np.isclose(np.sqrt(error), 0, atol=1e-5)
