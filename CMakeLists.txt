cmake_minimum_required(VERSION 3.15)
project(wise_pears)

# C++ 23
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# require pybind  
find_package(pybind11 REQUIRED)

# TODO : update woo_test.cpp with real algorithm 
# this created the occlusion_cpp module from woo_test.cpp
pybind11_add_module(ray_occlusion_cpp tests/amanatides-woo_test.cpp)

# once compiled so an .so, add to the wise_pears package folder  
install(TARGETS ray_occlusion_cpp DESTINATION wise_pears)