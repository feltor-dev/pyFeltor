import pytest
import json
import numpy as np
import magneticfielddb as magdb
from pyfeltor import dg

geo_loaded = True
try:
    from pyfeltor.dg import geo
except ImportError:
    geo_loaded = False


# Run with pytest-3 -s . to see stdout output
def geo_exists():
    if not geo_loaded:
        print( "dg.geo not compiled")
        return False
    return True


def test_polynomial():
    if not geo_exists(): return
    c = np.array( [1,2,3,4])
    params = {"R_0" : 400, "inverseaspectratio" : 20, "elongation" : 1, "triangularity" : 1,
              "PP" : 1, "PI" : 1, "description" : "standardX", "M" : 2, "N" : 2, "c" : c.tolist()}
    pp = dg.geo.polynomial.Parameters(params)
    psip = dg.geo.polynomial.Psip( pp)
    grid = dg.Grid( x0 = (pp.R_0-pp.a, -pp.a), x1 = (pp.R_0+pp.a, pp.a), n=(3,3), N=(24, 24))
    psi = dg.evaluate( psip, grid)
    R = dg.evaluate( lambda R, Z: R, grid)
    Z = dg.evaluate( lambda R, Z: Z, grid)
    psi_ = psip(R,Z)
    print( psi)
    print( psi_)


def test_make_field():
    if not geo_exists(): return
    with open ("geometry_params_Xpoint.json", "r") as f:
        magparams = json.load(f)
    mag = dg.geo.createMagneticField( magparams)
    a = mag.params().a()
    R0 = mag.R0()
    grid = dg.Grid(x0=(R0-a, -a), x1=(R0+a, +a), n=(3, 3), N=(24, 24))
    psi = dg.evaluate( mag.psip(), grid)
    BR  = dg.evaluate( dg.geo.BFieldR(mag), grid)
    print( mag.R0())
    print( mag.params().a())
    print( mag.params().elongation())
    print( mag.params().getDescription())
    print( mag.params().getEquilibrium())
    print (psi, BR)



def test_q_profile():
    if not geo_exists(): return
    #magparams = magdb.select( "COMPASS/compass_1X.json")
    with open ("enrx_tcv.json", "r") as f:
        magparams = json.load(f)
    mag = dg.geo.createMagneticField(magparams)
    qfunctor = dg.geo.SafetyFactor(mag)
    RO,ZO  = mag.R0(), 0
    (point, RO, ZO) = dg.geo.findOpoint(mag.get_psip(), RO, ZO)
    print( "O-point found at ", RO, ZO)
    psipO = mag.psip()(RO,ZO)
    psi_values = np.linspace( psipO, 0, 20, endpoint = False)
    print(qfunctor(psi_values))


