cmake_minimum_required(VERSION 3.1)
project(test_package LANGUAGES C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(hdr_histogram REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
if(HDRHISTOGRAM_SHARED)
  target_link_libraries(${PROJECT_NAME} hdr_histogram::hdr_histogram)
else()
  target_link_libraries(${PROJECT_NAME} hdr_histogram::hdr_histogram_static)
endif()
