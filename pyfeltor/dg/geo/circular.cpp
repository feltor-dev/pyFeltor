#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "dg/geometries/geometries.h"
namespace py = pybind11;
namespace poly = dg::geo::circular;


PYBIND11_MODULE(circular, m) { // name of the python module, not the C++ file
    m.doc() = "pybind11 binding guenter field"; // optional module docstring
    py::class_<poly::Psip>(m,"Psip")
        .def(py::init<double,double,double>( ))
        .def( "__call__", py::vectorize([]( poly::Psip& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipR>(m,"PsipR")
        .def(py::init<double,double>( ))
        .def( "__call__", py::vectorize([]( poly::PsipR& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipZ>(m,"PsipZ")
        .def(py::init<double>( ))
        .def( "__call__", py::vectorize([]( poly::PsipZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    m.def( "createPsip", &dg::geo::circular::createPsip);
    m.def( "createIpol", &dg::geo::circular::createIpol);
}
