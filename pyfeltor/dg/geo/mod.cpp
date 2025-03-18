#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "dg/geometries/geometries.h"
namespace py = pybind11;
namespace poly = dg::geo::mod;


PYBIND11_MODULE(mod, m) { // name of the python module, not the C++ file
    py::class_<poly::Psip>(m,"Psip")
        .def( "__call__", py::vectorize([]( poly::Psip& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipR>(m,"PsipR")
        .def( "__call__", py::vectorize([]( poly::PsipR& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipZ>(m,"PsipZ")
        .def( "__call__", py::vectorize([]( poly::PsipZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipRR>(m,"PsipRR")
        .def( "__call__", py::vectorize([]( poly::PsipRR& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipRZ>(m,"PsipRZ")
        .def( "__call__", py::vectorize([]( poly::PsipRZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipZZ>(m,"PsipZZ")
        .def( "__call__", py::vectorize([]( poly::PsipZZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    m.def( "createPsip", &dg::geo::mod::createPsip);
    py::class_<poly::SetCompose>(m,"SetCompose")
        .def( "__call__", py::vectorize([]( poly::SetCompose& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::SetUnion>(m,"SetUnion")
        .def( "__call__", py::vectorize([]( poly::SetUnion& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::SetIntersection>(m,"SetIntersection")
        .def( "__call__", py::vectorize([]( poly::SetIntersection& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::SetNot>(m,"SetNot")
        .def( "__call__", py::vectorize([]( poly::SetNot& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::ClosedFieldlineRegion>(m,"ClosedFieldlineRegion")
        .def( py::init<const dg::geo::TokamakMagneticField&,bool>(), py::arg( "mag"), py::arg("closed") = true)
        .def( "__call__", py::vectorize([]( poly::ClosedFieldlineRegion& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::SOLRegion>(m,"SOLRegion")
        .def( py::init<const dg::geo::TokamakMagneticField&,dg::geo::CylindricalFunctor>())
        .def( "__call__", py::vectorize([]( poly::SOLRegion& my,
                        double R, double Z){ return my(R,Z);}))
        ;
}
