add_library(rule30_cpp_core STATIC
  engine.cpp
)
add_library(rule30::cpp_core ALIAS rule30_cpp_core)

target_include_directories(rule30_cpp_core
  PUBLIC
    "${PROJECT_SOURCE_DIR}/include"
)
target_compile_features(rule30_cpp_core PUBLIC cxx_std_20)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(rule30_cpp_core PRIVATE
    -Wall
    -Wextra
    -Wpedantic
    -Wconversion
    -Wsign-conversion
  )
endif()

set(RULE30_AVX2_IMPLEMENTATION OFF)
if(RULE30_ENABLE_AVX2 AND
   CMAKE_SYSTEM_PROCESSOR MATCHES "^(x86_64|AMD64|amd64|i[3-6]86)$" AND
   CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  include(CheckCXXCompilerFlag)
  check_cxx_compiler_flag("-mavx2" RULE30_COMPILER_SUPPORTS_MAVX2)
  if(RULE30_COMPILER_SUPPORTS_MAVX2)
    target_sources(rule30_cpp_core PRIVATE avx2.cpp)
    set_source_files_properties(avx2.cpp PROPERTIES COMPILE_OPTIONS "-mavx2")
    set(RULE30_AVX2_IMPLEMENTATION ON)
  endif()
endif()

if(RULE30_AVX2_IMPLEMENTATION)
  target_compile_definitions(rule30_cpp_core PRIVATE RULE30_HAVE_AVX2_IMPL=1)
else()
  target_compile_definitions(rule30_cpp_core PRIVATE RULE30_HAVE_AVX2_IMPL=0)
endif()

add_executable(rule30_cpp main.cpp)
target_link_libraries(rule30_cpp PRIVATE rule30::cpp_core)
target_compile_features(rule30_cpp PRIVATE cxx_std_20)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(rule30_cpp PRIVATE
    -Wall
    -Wextra
    -Wpedantic
    -Wconversion
    -Wsign-conversion
  )
endif()

if(BUILD_TESTING AND
   EXISTS "${PROJECT_SOURCE_DIR}/tests/cpp/CMakeLists.txt" AND
   NOT TARGET rule30_cpp_tests)
  add_subdirectory(
    "${PROJECT_SOURCE_DIR}/tests/cpp"
    "${CMAKE_CURRENT_BINARY_DIR}/tests-cpp"
  )
endif()
