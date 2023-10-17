import pytest
import numpy as np
import magneticfielddb as magdb
from pyfeltor import dg

# Run with pytest-3 -s . to see stdout output

def test_polynomial():
    print( "hello world")
    c = np.array( [1,2,3,4])
    params = {"R_0" : 400, "inverseaspectratio" : 20, "elongation" : 1, "triangularity" : 1,
              "PP" : 1, "PI" : 1, "description" : "standardX", "M" : 2, "N" : 2, "c" : c.tolist()}
    pp = dg.geo.polynomial.Parameters(params)
    psip = dg.geo.polynomial.Psip( pp)
    Rs = np.full( 100, 200)
    Zs = np.full( 100, 3)
    print( psip( Rs,Zs))


def test_make_field():
    print( "hello world")
    magparams = magdb.select( "COMPASS/compass_1X.json")
    print(magparams)
    magpara = dg.geo.createMagneticField( magparams)
    Rs = np.full( 100, 0.500)
    Zs = np.full( 100, 0)
    print( magpara.R0())
    print( magpara.psip()( Rs,Zs))


def test_q_profile():
    #magparams = magdb.select( "COMPASS/compass_1X.json")
    magparams = magdb.select( "TCV/eq_TCV_76186.json")
    mag = dg.geo.createMagneticField(magparams)
    qfunctor = dg.geo.SafetyFactor(mag)
    RO  = mag.R0()
    ZO = 0
    (point, RO, ZO) = dg.geo.findOpoint(mag.get_psip(), RO, ZO)
    psipO = mag.psip()(RO,ZO)
    psi_values = np.linspace( psipO, 0, 20, endpoint = False)
    print(psipO)
    #print(qfunctor(psipO+1e-09))
    print(qfunctor(psi_values))


