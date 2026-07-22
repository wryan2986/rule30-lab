add_executable(rule30_cpp_tests test_engine.cpp)
target_link_libraries(rule30_cpp_tests PRIVATE rule30::cpp_core)
target_compile_features(rule30_cpp_tests PRIVATE cxx_std_20)
target_compile_definitions(rule30_cpp_tests PRIVATE
  RULE30_SOURCE_DIR="${PROJECT_SOURCE_DIR}"
)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(rule30_cpp_tests PRIVATE
    -Wall
    -Wextra
    -Wpedantic
    -Wconversion
    -Wsign-conversion
  )
endif()

add_test(NAME cpp_unit COMMAND rule30_cpp_tests)
set_tests_properties(cpp_unit PROPERTIES LABELS "cpp;unit")

add_test(
  NAME cpp_cli_contract
  COMMAND "${CMAKE_COMMAND}"
    "-DRULE30_CLI=$<TARGET_FILE:rule30_cpp>"
    "-DRULE30_TEST_DIRECTORY=${CMAKE_CURRENT_BINARY_DIR}/cli-contract"
    -P "${CMAKE_CURRENT_SOURCE_DIR}/check_cli.cmake"
)
set_tests_properties(cpp_cli_contract PROPERTIES LABELS "cpp;cli")
