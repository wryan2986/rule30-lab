if(CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
  cmake_minimum_required(VERSION 3.25)
  project(rule30_cuda LANGUAGES CXX CUDA)
  include(CTest)
  set(CMAKE_CXX_STANDARD 20)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
  set(CMAKE_CXX_EXTENSIONS OFF)
  set(CMAKE_CUDA_STANDARD 20)
  set(CMAKE_CUDA_STANDARD_REQUIRED ON)
endif()

find_package(CUDAToolkit REQUIRED)

add_library(
  rule30_cuda STATIC
  batch_period.cu
  batch_sideways.cu
  direct_evolution.cu
)
add_library(rule30::cuda ALIAS rule30_cuda)
target_include_directories(
  rule30_cuda
  PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)
target_link_libraries(rule30_cuda PUBLIC CUDA::cudart)
target_compile_features(rule30_cuda PUBLIC cxx_std_20 cuda_std_20)
set_target_properties(
  rule30_cuda
  PROPERTIES
    CUDA_ARCHITECTURES "75-real"
    CUDA_SEPARABLE_COMPILATION OFF
    CUDA_RUNTIME_LIBRARY Shared
)
target_compile_options(
  rule30_cuda
  PRIVATE
    $<$<COMPILE_LANGUAGE:CXX>:-Wall;-Wextra;-Wpedantic>
    $<$<COMPILE_LANGUAGE:CUDA>:-Xcompiler=-Wall,-Wextra>
)

add_executable(rule30_cuda_probe device_probe.cpp)
target_link_libraries(rule30_cuda_probe PRIVATE rule30::cuda)
target_compile_options(rule30_cuda_probe PRIVATE -Wall -Wextra -Wpedantic)

add_executable(rule30_cuda_generate generate_cli.cpp)
target_link_libraries(rule30_cuda_generate PRIVATE rule30::cuda)
target_compile_features(rule30_cuda_generate PRIVATE cxx_std_20)
target_compile_options(
  rule30_cuda_generate PRIVATE -Wall -Wextra -Wpedantic
)

add_executable(rule30_cuda_period_benchmark period_benchmark.cpp)
target_link_libraries(rule30_cuda_period_benchmark PRIVATE rule30::cuda)
target_compile_options(
  rule30_cuda_period_benchmark PRIVATE -Wall -Wextra -Wpedantic
)

add_executable(rule30_cuda_evolution_benchmark direct_evolution_benchmark.cpp)
target_link_libraries(rule30_cuda_evolution_benchmark PRIVATE rule30::cuda)
target_compile_options(
  rule30_cuda_evolution_benchmark PRIVATE -Wall -Wextra -Wpedantic
)

add_executable(rule30_cuda_sideways_benchmark sideways_benchmark.cpp)
target_link_libraries(rule30_cuda_sideways_benchmark PRIVATE rule30::cuda)
target_compile_options(
  rule30_cuda_sideways_benchmark PRIVATE -Wall -Wextra -Wpedantic
)

add_executable(
  rule30_cuda_extended_period_search
  extended_period_search.cpp
)
target_link_libraries(rule30_cuda_extended_period_search PRIVATE rule30::cuda)
target_compile_features(
  rule30_cuda_extended_period_search PRIVATE cxx_std_20
)
target_compile_options(
  rule30_cuda_extended_period_search PRIVATE -Wall -Wextra -Wpedantic
)

if(BUILD_TESTING AND NOT TARGET rule30_cuda_tests)
  add_subdirectory(
    "${CMAKE_CURRENT_SOURCE_DIR}/../../tests/cuda"
    "${CMAKE_CURRENT_BINARY_DIR}/tests"
  )
endif()
