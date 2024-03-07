#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "dg/geometries/geometries.h"
namespace py = pybind11;
namespace poly = dg::geo::guenter;


PYBIND11_MODULE(guenter, m) { // name of the python module, not the C++ file
    m.doc() = "pybind11 binding guenter field"; // optional module docstring
    py::class_<poly::Psip>(m,"Psip")
        .def(py::init<double>( ))
        .def( "__call__", py::vectorize([]( poly::Psip& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipR>(m,"PsipR")
        .def(py::init<double>( ))
        .def( "__call__", py::vectorize([]( poly::PsipR& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipZ>(m,"PsipZ")
        .def(py::init<double>( ))
        .def( "__call__", py::vectorize([]( poly::PsipZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipRR>(m,"PsipRR")
        .def(py::init<double>( ))
        .def( "__call__", py::vectorize([]( poly::PsipRR& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipRZ>(m,"PsipRZ")
        .def(py::init<double>( ))
        .def( "__call__", py::vectorize([]( poly::PsipRZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipZZ>(m,"PsipZZ")
        .def(py::init<double>( ))
        .def( "__call__", py::vectorize([]( poly::PsipZZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::Ipol>(m,"Ipol")
        .def(py::init<double>( ))
        .def( "__call__", py::vectorize([]( poly::Ipol& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::IpolR>(m,"IpolR")
        .def(py::init<>( ))
        .def( "__call__", py::vectorize([]( poly::IpolR& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::IpolZ>(m,"IpolZ")
        .def(py::init<>( ))
        .def( "__call__", py::vectorize([]( poly::IpolZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    m.def( "createPsip", &dg::geo::guenter::createPsip);
    m.def( "createIpol", &dg::geo::guenter::createIpol);
}
