#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11_json/pybind11_json.hpp>

#include "dg/geometries/geometries.h"
namespace py = pybind11;
namespace poly = dg::geo::solovev;


PYBIND11_MODULE(solovev, m) { // name of the python module, not the C++ file
    py::class_<poly::Parameters>(m,"Parameters")
        .def(py::init<>())
        .def(py::init( [](const nlohmann::json& js){
                    return std::make_unique<poly::Parameters>(js);}))
        .def_readwrite("A", &poly::Parameters::a)
        .def_readwrite("R_0", &poly::Parameters::R_0)
        .def_readwrite("pp", &poly::Parameters::pp)
        .def_readwrite("pi", &poly::Parameters::pi)
        .def_readwrite("a", &poly::Parameters::a)
        .def_readwrite("elongation", &poly::Parameters::elongation)
        .def_readwrite("triangularity", &poly::Parameters::triangularity)
        .def_readwrite("c", &poly::Parameters::c)
        .def_readwrite("description", &poly::Parameters::description)
        .def("isToroidal", &poly::Parameters::isToroidal)
        .def("hasXpoint", &poly::Parameters::hasXpoint)
        .def("display", &poly::Parameters::display)
        ;
    py::class_<poly::Psip>(m,"Psip")
        .def(py::init<poly::Parameters>())
        .def( "__call__", py::vectorize([]( poly::Psip& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipR>(m,"PsipR")
        .def(py::init<poly::Parameters>())
        .def( "__call__", py::vectorize([]( poly::PsipR& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipZ>(m,"PsipZ")
        .def(py::init<poly::Parameters>())
        .def( "__call__", py::vectorize([]( poly::PsipZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipRR>(m,"PsipRR")
        .def(py::init<poly::Parameters>())
        .def( "__call__", py::vectorize([]( poly::PsipRR& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipRZ>(m,"PsipRZ")
        .def(py::init<poly::Parameters>())
        .def( "__call__", py::vectorize([]( poly::PsipRZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::PsipZZ>(m,"PsipZZ")
        .def(py::init<poly::Parameters>())
        .def( "__call__", py::vectorize([]( poly::PsipZZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::Ipol>(m,"Ipol")
        .def(py::init( []( poly::Parameters dict, std::function<double(double,double)> f ){
                return std::make_unique< poly::Ipol>( dict, f); }))
        .def( "__call__", py::vectorize([]( poly::Ipol& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::IpolR>(m,"IpolR")
        .def(py::init( []( poly::Parameters dict, std::function<double(double,double)> f, std::function<double(double,double)> g ){
                return std::make_unique< poly::IpolR>( dict, f, g); }))
        .def( "__call__", py::vectorize([]( poly::IpolR& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    py::class_<poly::IpolZ>(m,"IpolZ")
        .def(py::init( []( poly::Parameters dict, std::function<double(double,double)> f, std::function<double(double,double)> g ){
                return std::make_unique< poly::IpolZ>( dict, f, g); }))
        .def( "__call__", py::vectorize([]( poly::IpolZ& my,
                        double R, double Z){ return my(R,Z);}))
        ;
    m.def( "createPsip", &dg::geo::solovev::createPsip);
    m.def( "createIpol", [](poly::Parameters dict, const
                dg::geo::CylindricalFunctorsLvl1& psip){ return
            dg::geo::solovev::createIpol(dict, psip);});
}
