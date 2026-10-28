cmake_minimum_required(VERSION 3.15)
project(wise_pears)

# C++ 23
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# require pybind  
find_package(pybind11 REQUIRED)

# TODO: make this test.cpp Amanatides and Woo occlusion algorithm 
# TODO 2: update woo_test.cpp with real algorithm 
# this created the _occlusion_cpp module from woo_test.cpp
pybind11_add_module(_occlusion_cpp tests/woo_test.cpp)

# once compiled so an .so, add to the wise_pears package folder  
install(TARGETS _occlusion_cpp DESTINATION wise_pears)