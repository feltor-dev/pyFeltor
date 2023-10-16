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
    m.def( "createWallRegion", []( const nlohmann::json& gs, const nlohmann::json&
                jsmod) { return dg::geo::createWallRegion( gs, jsmod);});
    m.def( "createMagneticField", []( const nlohmann::json& json){
            return dg::geo::createMagneticField( json); });
}
