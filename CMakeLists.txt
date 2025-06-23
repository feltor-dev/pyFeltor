## Inspired from https://github.com/pybind/scikit_build_example/blob/master/CMakeLists.txt

# Require CMake 3.15+ (matching scikit-build-core) Use new versions of all
# policies up to CMake 3.27
cmake_minimum_required( VERSION "3.26")


# Scikit-build-core sets these values for you, or you can just hard-code the
# name and version.
project(
  ${SKBUILD_PROJECT_NAME}
  VERSION ${SKBUILD_PROJECT_VERSION}
  LANGUAGES CXX)

include(cmake/CPM.cmake)
set( CCCL_THRUST_DEVICE_SYSTEM "CPP")
CPMAddPackage(
    NAME feltor
    GITHUB_REPOSITORY "feltor-dev/feltor"
    VERSION 8.2
    SYSTEM ON
    EXCLUDE_FROM_ALL ON
    OPTIONS "FELTOR_DG_WITH_MATRIX OFF" "FELTOR_FILE_WITH_NETCDF OFF"
)


# Find the module development requirements (requires FindPython from 3.17 or
# scikit-build-core's built-in backport)
# MW: https://cmake.org/cmake/help/latest/module/FindPython.html
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
# Install pyprojects pybind11
find_package(pybind11 CONFIG REQUIRED)

# Needs to come after feltor because json is already included there
# unless we use CPM_USE_LOCAL_PACKAGES
CPMAddPackage( "gh:pybind/pybind11_json#0.2.15")

set( PYFELTOR_EXE
    pyfeltor/dg/geo/geometries.cpp
    pyfeltor/dg/geo/polynomial.cpp
    pyfeltor/dg/geo/solovev.cpp
    pyfeltor/dg/geo/guenter.cpp
    pyfeltor/dg/geo/circular.cpp
    pyfeltor/dg/geo/flux.cpp
    pyfeltor/dg/geo/mod.cpp
    pyfeltor/dg/geo/toroidal.cpp
    pyfeltor/dg/geo/utility.cpp
)

# Add a library using FindPython's tooling (pybind11 also provides a helper like
# this)
python_add_library(_core MODULE WITH_SOABI ${PYFELTOR_EXE})
target_compile_features(_core PRIVATE cxx_std_17)
if (MSVC)
    # warning level 4
    target_compile_options(_core PRIVATE /W4 /permissive- /arch:AVX2 /O2 /EHsc -DFP_FAST_FMA -D_USE_MATH_DEFINES)
else()
    # additional warnings
    target_compile_options(_core PRIVATE -Wall -Wextra -Wpedantic -march=native -O2)
endif()

target_link_libraries(_core PRIVATE pybind11::headers)


target_link_libraries(_core PRIVATE feltor::dg::geometries)
target_link_libraries(_core PRIVATE pybind11_json)


# The install directory is the output (wheel) directory
install(TARGETS _core DESTINATION scikit_build_example)
