import pytest
import numpy as np
import magneticfielddb as mag
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
    magparams = mag.select( "COMPASS/compass_1X.json")
    print(magparams)
    magpara = dg.geo.createMagneticField( magparams)
    Rs = np.full( 100, 0.500)
    Zs = np.full( 100, 0)
    print( magpara.R0())
    print( magpara.psip()( Rs,Zs))

