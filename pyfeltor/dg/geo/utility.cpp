#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "dg/algorithm.h"
#include "dg/file/json_utilities.h"
#include "dg/geometries/geometries.h"

namespace py = pybind11;

PYBIND11_MODULE(utility, m) {
    py::class_<dg::geo::CylindricalFunctor>(m,"CylindricalFunctor")
        .def( py::init<>())
        .def(py::init<std::function<double(double,double)>>())
        .def( "__call__", py::vectorize([]( dg::geo::CylindricalFunctor& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<dg::geo::Constant>(m,"Constant")
        .def(py::init<double>())
        .def( "__call__", py::vectorize([]( dg::geo::Constant& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::ZCutter>(m,"ZCutter")
        .def(py::init<double,int>(), py::arg("ZX"), py::arg("sign") = +1)
        .def( "__call__", py::vectorize([]( dg::geo::ZCutter& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::CylindricalFunctorsLvl1>(m,"CylindricalFunctorsLvl1")
        .def( "f", &dg::geo::CylindricalFunctorsLvl1::f)
        .def( "dfx", &dg::geo::CylindricalFunctorsLvl1::dfx)
        .def( "dfy", &dg::geo::CylindricalFunctorsLvl1::dfy)
        ;
    py::class_<dg::geo::CylindricalFunctorsLvl2>(m,"CylindricalFunctorsLvl2")
        .def( "f", &dg::geo::CylindricalFunctorsLvl2::f)
        .def( "dfx", &dg::geo::CylindricalFunctorsLvl2::dfx)
        .def( "dfy", &dg::geo::CylindricalFunctorsLvl2::dfy)
        .def( "dfxx", &dg::geo::CylindricalFunctorsLvl2::dfxx)
        .def( "dfxy", &dg::geo::CylindricalFunctorsLvl2::dfxy)
        .def( "dfyy", &dg::geo::CylindricalFunctorsLvl2::dfyy)
        ;
    py::class_<dg::geo::CylindricalSymmTensorLvl1>(m,"CylindricalSymmTensorLvl1")
        .def( "xx", &dg::geo::CylindricalSymmTensorLvl1::xx)
        .def( "xy", &dg::geo::CylindricalSymmTensorLvl1::xy)
        .def( "yy", &dg::geo::CylindricalSymmTensorLvl1::yy)
        .def( "divX", &dg::geo::CylindricalSymmTensorLvl1::divX)
        .def( "divY", &dg::geo::CylindricalSymmTensorLvl1::divY)
        ;
    py::class_<dg::geo::CylindricalVectorLvl0>(m,"CylindricalVectorLvl0")
        .def( "x", &dg::geo::CylindricalVectorLvl0::x)
        .def( "y", &dg::geo::CylindricalVectorLvl0::y)
        .def( "z", &dg::geo::CylindricalVectorLvl0::z)
        ;
    py::class_<dg::geo::CylindricalVectorLvl1>(m,"CylindricalVectorLvl1")
        .def( "x", &dg::geo::CylindricalVectorLvl1::x)
        .def( "y", &dg::geo::CylindricalVectorLvl1::y)
        .def( "z", &dg::geo::CylindricalVectorLvl1::z)
        .def( "div", &dg::geo::CylindricalVectorLvl1::div)
        .def( "divvvz", &dg::geo::CylindricalVectorLvl1::divvvz)
        ;
    py::class_<dg::geo::ScalarProduct>(m,"ScalarProduct")
        .def(py::init<dg::geo::CylindricalVectorLvl0,dg::geo::CylindricalVectorLvl0>())
        .def( "__call__", py::vectorize([]( dg::geo::ScalarProduct& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::SquareNorm>(m,"SquareNorm")
        .def(py::init<dg::geo::CylindricalVectorLvl0,dg::geo::CylindricalVectorLvl0>())
        .def( "__call__", py::vectorize([]( dg::geo::SquareNorm& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::SafetyFactor>(m,"SafetyFactor")
        .def( py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__",  py::vectorize([]( dg::geo::SafetyFactor& my,
                        double psip0) { return my(psip0);}))
        ;
    // unfortunately floats are immutable in python (see pybind FAQ) we work-around with tuples:
    m.def( "findCriticalpoint", []( const dg::geo::CylindricalFunctorsLvl2& psi, double RC, double ZC)
            {
                int point = findCriticalPoint(psi, RC, ZC);
                return std::make_tuple(point, RC, ZC);
            });
    m.def( "findOpoint", []( const dg::geo::CylindricalFunctorsLvl2& psi, double RC, double ZC)
            {
                int point = findOpoint(psi, RC, ZC);
                return std::make_tuple(point, RC, ZC);
            });
    m.def( "findXpoint", []( const dg::geo::CylindricalFunctorsLvl2& psi, double RC, double ZC)
            {
                findXpoint(psi, RC, ZC);
                return std::make_pair( RC, ZC);
            });
}
