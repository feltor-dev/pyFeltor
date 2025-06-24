#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <pybind11_json/pybind11_json.hpp>

#include "dg/algorithm.h"
#include "dg/file/json_utilities.h"
#include "dg/geometries/geometries.h"

namespace py = pybind11;


PYBIND11_MODULE(flux, m) {
    m.def( "createSolovevField", &dg::geo::createSolovevField);
    m.def( "createPolynomialField", &dg::geo::createPolynomialField);
    m.def( "createGuenterField", &dg::geo::createGuenterField);
    m.def( "createToroidalField", &dg::geo::createToroidalField);
    m.def( "createCircularField", &dg::geo::createCircularField);
    m.def( "createModifiedField", []( const nlohmann::json& gs, const nlohmann::json&
                jsmod, dg::geo::CylindricalFunctor& wall,
                dg::geo::CylindricalFunctor& transition)
            { return dg::geo::createModifiedField( gs, jsmod, wall, transition);});
    m.def( "createWallRegion", []( const dg::geo::TokamakMagneticField& mag, const nlohmann::json&
                jsmod) { return dg::geo::createWallRegion( mag, jsmod);});
    m.def( "createMagneticField", []( const nlohmann::json& json){
            return dg::geo::createMagneticField( json); });
    m.def( "createSheathRegion", []( nlohmann::json jsmod, dg::geo::TokamakMagneticField mag,
    dg::geo::CylindricalFunctor wall, py::object& grid, dg::geo::CylindricalFunctor& sheath)
    {
        auto x0_ = grid.attr("x0").cast<py::array_t<double>>(); //this is a numpy array
        auto x0 = x0_.mutable_unchecked<1>();
        auto x1_ = grid.attr("x1").cast<py::array_t<double>>(); //this is a numpy array
        auto x1 = x1_.mutable_unchecked<1>();

        dg::Grid2d g2d( x0[0], x1[0], x0[1], x1[1], 1,1,1);
        dg::geo::createSheathRegion( jsmod, mag, wall, g2d, sheath);
        x0[0] = g2d.x0();
        x1[0] = g2d.x1();
        x0[1] = g2d.y0();
        x1[1] = g2d.y1();
        return;
    });

}
