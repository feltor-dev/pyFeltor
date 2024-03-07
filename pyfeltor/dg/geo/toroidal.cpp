#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "dg/geometries/geometries.h"
namespace py = pybind11;


PYBIND11_MODULE(toroidal, m) { // name of the python module, not the C++ file
    m.def( "createPsip", &dg::geo::toroidal::createPsip);
    m.def( "createIpol", &dg::geo::toroidal::createIpol);
}
