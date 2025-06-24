import json

import numpy as np

from pyfeltor import dg


def test_polynomial():
    c = np.array([1, 2, 3, 4])
    params = {"R_0": 400, "inverseaspectratio": 20, "elongation": 1, "triangularity": 1,
              "PP": 1, "PI": 1, "description": "standardX", "M": 2, "N": 2,
              "c": c.tolist()}
    pp = dg.geo.polynomial.Parameters(params)
    psip = dg.geo.polynomial.Psip(pp)
    grid = dg.Grid(x0=(pp.R_0 - pp.a, -pp.a), x1=(pp.R_0 + pp.a, pp.a),
        n=(3, 3), N=(24, 24))
    psi = dg.evaluate(psip, grid)
    R = dg.evaluate(lambda R, Z: R, grid)
    Z = dg.evaluate(lambda R, Z: Z, grid)
    psi_ = psip(R, Z)
    print(psi)
    print(psi_)


def test_make_field(datadir):
    with open(datadir / "geometry_params_Xpoint.json") as f:
        magparams = json.load(f)
    mag = dg.geo.createMagneticField(magparams)
    a = mag.params().a()
    R0 = mag.R0()
    grid = dg.Grid(x0=(R0 - a, -a), x1=(R0 + a, +a), n=(3, 3), N=(24, 24))
    psi = dg.evaluate(mag.psip(), grid)
    BR = dg.evaluate(dg.geo.BFieldR(mag), grid)
    print(mag.R0())
    print(mag.params().a())
    print(mag.params().elongation())
    print(mag.params().getDescription())
    print(mag.params().getEquilibrium())
    print(psi, BR)


def test_q_profile(datadir):
    with open(datadir / "enrx_tcv.json") as f:
        magparams = json.load(f)
    mag = dg.geo.createMagneticField(magparams)
    qfunctor = dg.geo.SafetyFactor(mag)
    RO, ZO = mag.R0(), 0
    (point, RO, ZO) = dg.geo.findOpoint(mag.get_psip(), RO, ZO)
    print("O-point found at ", RO, ZO)
    psipO = mag.psip()(RO, ZO)
    psi_values = np.linspace(psipO, 0, 20, endpoint=False)
    print(qfunctor(psi_values))


def test_sheath(datadir):
    with open(datadir / "enrx_tcv.json") as f:
        magparams = json.load(f)
    mag = dg.geo.createMagneticField(magparams)
    wall = {"type": "sol_pfr", "alpha": [0.05, 0.05], "boundary": [1.09, 0.97]}
    sheath = {"boundary": 3 / 32, "alpha": 2 / 32}
    wall_f = dg.geo.CylindricalFunctor()
    transition_f = dg.geo.CylindricalFunctor()
    sheath_f = dg.geo.CylindricalFunctor()
    dg.geo.createModifiedField(magparams, wall, wall_f, transition_f)
    a = mag.params().a()
    R0 = mag.R0()
    print(R0 - a, -a, R0 + a, +a)
    grid = dg.Grid(x0=(R0 - a, -a), x1=(R0 + a, +a), n=(3, 3), N=(24, 24))
    dg.geo.createSheathRegion(sheath, mag, wall_f, grid, sheath_f)

    point, RO, ZO = dg.geo.findOpoint(mag.get_psip(), R0, 0)
    assert (point == 1)
    assert (abs(RO - 0.9022324795511738) < 1e-10)
    assert (abs(ZO - (-0.005684720497897021)) < 1e-10)

    closed = dg.geo.mod.ClosedFieldlineRegion(mag)
    assert (closed(0, R0))
    opened = dg.geo.mod.ClosedFieldlineRegion(mag, False)
    assert (not opened(0, R0))
    sol = dg.geo.mod.SOLRegion(mag, wall_f)
    assert (not sol(0, R0))

    cutter = dg.geo.ZCutter(10)
    assert (cutter(1, 11))
    assert (not cutter(1, 8))
