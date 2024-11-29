#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <pybind11_json/pybind11_json.hpp>

#include "dg/algorithm.h"
#include "dg/file/json_utilities.h"
#include "dg/geometries/geometries.h"

namespace py = pybind11;

PYBIND11_MODULE(geometries, m) { // name of the python module, not the C++ file
    py::enum_<dg::geo::description>( m, "description")
        .value("standardO", dg::geo::description::standardO)
        .value("standardX", dg::geo::description::standardX)
        .value("doubleX", dg::geo::description::doubleX)
        .value("none", dg::geo::description::none)
        .value("square", dg::geo::description::square)
        .value("centeredX", dg::geo::description::centeredX)
        ;
    py::enum_<dg::geo::equilibrium>( m, "equilibrium")
        .value("solovev", dg::geo::equilibrium::solovev)
        .value("taylor", dg::geo::equilibrium::taylor)
        .value("polynomial", dg::geo::equilibrium::polynomial)
        .value("guenter", dg::geo::equilibrium::guenter)
        .value("toroidal", dg::geo::equilibrium::toroidal)
        .value("circular", dg::geo::equilibrium::circular)
        ;
    py::enum_<dg::geo::modifier>( m, "modifier")
        .value("none", dg::geo::modifier::none)
        .value("heaviside", dg::geo::modifier::heaviside)
        .value("sol_pfr", dg::geo::modifier::sol_pfr)
        .value("sol_pfr_2X", dg::geo::modifier::sol_pfr_2X)
        ;
    py::class_<dg::geo::MagneticFieldParameters>(m,"MagneticFieldParameters")
        .def(py::init<>())
        .def(py::init<double,double,double,dg::geo::equilibrium,dg::geo::modifier,dg::geo::description>())
        .def("a",&dg::geo::MagneticFieldParameters::a)
        .def("elongation",&dg::geo::MagneticFieldParameters::elongation)
        .def("triangularity",&dg::geo::MagneticFieldParameters::triangularity)
        .def("getEquilibrium",&dg::geo::MagneticFieldParameters::getEquilibrium)
        .def("getModifier",&dg::geo::MagneticFieldParameters::getModifier)
        .def("getDescription",&dg::geo::MagneticFieldParameters::getDescription)
        ;
    py::class_<dg::geo::TokamakMagneticField>(m,"TokamakMagneticField")
        .def( "R0", &dg::geo::TokamakMagneticField::R0)
        .def( "psip", &dg::geo::TokamakMagneticField::psip)
        .def( "psipR", &dg::geo::TokamakMagneticField::psipR)
        .def( "psipZ", &dg::geo::TokamakMagneticField::psipZ)
        .def( "psipRR", &dg::geo::TokamakMagneticField::psipRR)
        .def( "psipRZ", &dg::geo::TokamakMagneticField::psipRZ)
        .def( "psipZZ", &dg::geo::TokamakMagneticField::psipZZ)
        .def( "ipol", &dg::geo::TokamakMagneticField::ipol)
        .def( "ipolR", &dg::geo::TokamakMagneticField::ipolR)
        .def( "ipolZ", &dg::geo::TokamakMagneticField::ipolZ)
        .def( "get_psip", &dg::geo::TokamakMagneticField::get_psip)
        .def( "get_ipol", &dg::geo::TokamakMagneticField::get_ipol)
        .def( "params", &dg::geo::TokamakMagneticField::params)
    ;
    py::class_<dg::geo::LaplacePsip>(m,"LaplacePsip")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::LaplacePsip& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::Bmodule>(m,"Bmodule")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::Bmodule& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::InvB>(m,"InvB")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::InvB& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::LnB>(m,"LnB")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::LnB& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BR>(m,"BR")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BR& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BZ>(m,"BZ")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BZ& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::CurvatureNablaBR>(m,"CurvatureNablaBR")
        .def(py::init<const dg::geo::TokamakMagneticField&,int>())
        .def( "__call__", py::vectorize([]( dg::geo::CurvatureNablaBR& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::CurvatureNablaBZ>(m,"CurvatureNablaBZ")
        .def(py::init<const dg::geo::TokamakMagneticField&,int>())
        .def( "__call__", py::vectorize([]( dg::geo::CurvatureNablaBZ& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::CurvatureKappaR>(m,"CurvatureKappaR")
        .def(py::init<const dg::geo::TokamakMagneticField&,int>())
        .def( "__call__", py::vectorize([]( dg::geo::CurvatureKappaR& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::CurvatureKappaZ>(m,"CurvatureKappaZ")
        .def(py::init<const dg::geo::TokamakMagneticField&,int>())
        .def( "__call__", py::vectorize([]( dg::geo::CurvatureKappaZ& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::DivCurvatureKappa>(m,"DivCurvatureKappa")
        .def(py::init<const dg::geo::TokamakMagneticField&,int>())
        .def( "__call__", py::vectorize([]( dg::geo::DivCurvatureKappa& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::DivCurvatureNablaB>(m,"DivCurvatureNablaB")
        .def(py::init<const dg::geo::TokamakMagneticField&,int>())
        .def( "__call__", py::vectorize([]( dg::geo::DivCurvatureNablaB& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::TrueCurvatureNablaBR>(m,"TrueCurvatureNablaBR")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::TrueCurvatureNablaBR& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::TrueCurvatureNablaBZ>(m,"TrueCurvatureNablaBZ")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::TrueCurvatureNablaBZ& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::TrueCurvatureNablaBP>(m,"TrueCurvatureNablaBP")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::TrueCurvatureNablaBP& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::TrueCurvatureKappaR>(m,"TrueCurvatureKappaR")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::TrueCurvatureKappaR& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::TrueCurvatureKappaZ>(m,"TrueCurvatureKappaZ")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::TrueCurvatureKappaZ& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::TrueCurvatureKappaP>(m,"TrueCurvatureKappaP")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::TrueCurvatureKappaP& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::TrueDivCurvatureKappa>(m,"TrueDivCurvatureKappa")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::TrueDivCurvatureKappa& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::TrueDivCurvatureNablaB>(m,"TrueDivCurvatureNablaB")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::TrueDivCurvatureNablaB& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::GradLnB>(m,"GradLnB")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::GradLnB& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::Divb>(m,"Divb")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::Divb& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BFieldP>(m,"BFieldP")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BFieldP& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BFieldR>(m,"BFieldR")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BFieldR& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BFieldZ>(m,"BFieldZ")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BFieldZ& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BFieldT>(m,"BFieldT")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BFieldT& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BHatR>(m,"BHatR")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BHatR& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BHatZ>(m,"BHatZ")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BHatZ& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BHatP>(m,"BHatP")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BHatP& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BHatRR>(m,"BHatRR")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BHatRR& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BHatRZ>(m,"BHatRZ")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BHatRZ& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BHatZR>(m,"BHatZR")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BHatZR& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BHatZZ>(m,"BHatZZ")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BHatZZ& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BHatPR>(m,"BHatPR")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BHatPR& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::BHatPZ>(m,"BHatPZ")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::BHatPZ& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::DivVVP>(m,"DivVVP")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::DivVVP& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::RhoP>(m,"RhoP")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::RhoP& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::Hoo>(m,"Hoo")
        .def(py::init<const dg::geo::TokamakMagneticField&>())
        .def( "__call__", py::vectorize([]( dg::geo::Hoo& my,
                        double R, double Z){ return my(R,Z);}));
    m.def( "createBHat", &dg::geo::createBHat);
    m.def( "createCurvatureKappa", &dg::geo::createCurvatureKappa);
    m.def( "createCurvatureNablaB", &dg::geo::createCurvatureNablaB);
    m.def( "createEPhi", &dg::geo::createEPhi);
    m.def( "createGradPsip", &dg::geo::createGradPsip);
    m.def( "createTrueCurvatureKappa", &dg::geo::createTrueCurvatureKappa);
    m.def( "createTrueCurvatureNablaB", &dg::geo::createTrueCurvatureNablaB);
    py::class_<dg::geo::NablaPsiInv>(m,"NablaPsiInv")
        .def(py::init<const dg::geo::CylindricalFunctorsLvl1&>())
        .def( "__call__", py::vectorize([]( dg::geo::NablaPsiInv& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::NablaPsiInvX>(m,"NablaPsiInvX")
        .def(py::init<const dg::geo::CylindricalFunctorsLvl2&>())
        .def( "__call__", py::vectorize([]( dg::geo::NablaPsiInvX& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::NablaPsiInvY>(m,"NablaPsiInvY")
        .def(py::init<const dg::geo::CylindricalFunctorsLvl2&>())
        .def( "__call__", py::vectorize([]( dg::geo::NablaPsiInvY& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::Liseikin_XX>(m,"Liseikin_XX")
        .def(py::init<const dg::geo::CylindricalFunctorsLvl1&,double,double>())
        .def( "__call__", py::vectorize([]( dg::geo::Liseikin_XX& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::Liseikin_XY>(m,"Liseikin_XY")
        .def(py::init<const dg::geo::CylindricalFunctorsLvl1&,double,double>())
        .def( "__call__", py::vectorize([]( dg::geo::Liseikin_XY& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::Liseikin_YY>(m,"Liseikin_YY")
        .def(py::init<const dg::geo::CylindricalFunctorsLvl1&,double,double>())
        .def( "__call__", py::vectorize([]( dg::geo::Liseikin_YY& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::DivLiseikinX>(m,"DivLiseikinX")
        .def(py::init<const dg::geo::CylindricalFunctorsLvl2&,double,double>())
        .def( "__call__", py::vectorize([]( dg::geo::DivLiseikinX& my,
                        double R, double Z){ return my(R,Z);}));
    py::class_<dg::geo::DivLiseikinY>(m,"DivLiseikinY")
        .def(py::init<const dg::geo::CylindricalFunctorsLvl2&,double,double>())
        .def( "__call__", py::vectorize([]( dg::geo::DivLiseikinY& my,
                        double R, double Z){ return my(R,Z);}));
    m.def( "make_NablaPsiInvCollective",&dg::geo::make_NablaPsiInvCollective);
    m.def( "make_LiseikinCollective",&dg::geo::make_LiseikinCollective);

}
