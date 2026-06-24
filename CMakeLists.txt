cmake_minimum_required(VERSION 3.15)
project(shapely LANGUAGES C)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module NumPy)
find_package(geos REQUIRED)

find_program(CYTHON_EXECUTABLE NAMES cython cython3 REQUIRED)

set(SHAPELY_MACROS
    GEOS_USE_ONLY_R_API
    NPY_NO_DEPRECATED_API=0
    NPY_TARGET_VERSION=NPY_1_23_API_VERSION
)

# shapely.lib — main C extension wrapping GEOS C API
Python3_add_library(lib MODULE
    src/c_api.c
    src/coords.c
    src/geom_arr.c
    src/geos.c
    src/geos_funcs_O_b.c
    src/geos_funcs_YY_Y.c
    src/geos_funcs_YY_b.c
    src/geos_funcs_YY_d.c
    src/geos_funcs_YYd_Y.c
    src/geos_funcs_YYd_d.c
    src/geos_funcs_Y_Y.c
    src/geos_funcs_Y_b.c
    src/geos_funcs_Y_d.c
    src/geos_funcs_Y_i.c
    src/geos_funcs_Yd_Y.c
    src/geos_funcs_Ydb_Y.c
    src/geos_funcs_Ydd_b.c
    src/geos_funcs_Yi_Y.c
    src/lib.c
    src/pygeom.c
    src/pygeos.c
    src/signal_checks.c
    src/strtree.c
    src/ufuncs.c
    src/vector.c
)
target_compile_definitions(lib PRIVATE ${SHAPELY_MACROS})
target_include_directories(lib PRIVATE src ${Python3_NumPy_INCLUDE_DIRS})
target_link_libraries(lib PRIVATE GEOS::geos_c)
install(TARGETS lib DESTINATION shapely)
if(WIN32)
    install(FILES $<TARGET_FILE:GEOS::geos> $<TARGET_FILE:GEOS::geos_c> DESTINATION shapely)
endif()

# shapely._geos — Cython wrapper for GEOS context handle
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/_geos.c
    COMMAND ${CYTHON_EXECUTABLE} --3str
            -I ${CMAKE_CURRENT_SOURCE_DIR}/shapely
            ${CMAKE_CURRENT_SOURCE_DIR}/shapely/_geos.pyx
            -o ${CMAKE_CURRENT_BINARY_DIR}/_geos.c
    DEPENDS
        ${CMAKE_CURRENT_SOURCE_DIR}/shapely/_geos.pyx
        ${CMAKE_CURRENT_SOURCE_DIR}/shapely/_geos.pxd
    VERBATIM
)
Python3_add_library(_geos MODULE ${CMAKE_CURRENT_BINARY_DIR}/_geos.c)
target_compile_definitions(_geos PRIVATE ${SHAPELY_MACROS})
target_include_directories(_geos PRIVATE src ${Python3_NumPy_INCLUDE_DIRS})
target_link_libraries(_geos PRIVATE GEOS::geos_c)
install(TARGETS _geos DESTINATION shapely)

# shapely._geometry_helpers — Cython geometry helpers
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/_geometry_helpers.c
    COMMAND ${CYTHON_EXECUTABLE} --3str
            -I ${CMAKE_CURRENT_SOURCE_DIR}/shapely
            ${CMAKE_CURRENT_SOURCE_DIR}/shapely/_geometry_helpers.pyx
            -o ${CMAKE_CURRENT_BINARY_DIR}/_geometry_helpers.c
    DEPENDS
        ${CMAKE_CURRENT_SOURCE_DIR}/shapely/_geometry_helpers.pyx
        ${CMAKE_CURRENT_SOURCE_DIR}/shapely/_geos.pxd
        ${CMAKE_CURRENT_SOURCE_DIR}/shapely/_pygeos_api.pxd
    VERBATIM
)
Python3_add_library(_geometry_helpers MODULE ${CMAKE_CURRENT_BINARY_DIR}/_geometry_helpers.c)
target_compile_definitions(_geometry_helpers PRIVATE ${SHAPELY_MACROS})
target_include_directories(_geometry_helpers PRIVATE src ${Python3_NumPy_INCLUDE_DIRS})
target_link_libraries(_geometry_helpers PRIVATE GEOS::geos_c)
install(TARGETS _geometry_helpers DESTINATION shapely)
