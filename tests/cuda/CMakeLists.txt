add_executable(rule30_cuda_tests test_batch_period.cpp)
target_link_libraries(rule30_cuda_tests PRIVATE rule30::cuda)
target_compile_features(rule30_cuda_tests PRIVATE cxx_std_20)
target_compile_options(rule30_cuda_tests PRIVATE -Wall -Wextra -Wpedantic)

add_test(NAME rule30_cuda_batch_period COMMAND rule30_cuda_tests)
set_tests_properties(rule30_cuda_batch_period PROPERTIES SKIP_RETURN_CODE 77)

add_executable(rule30_cuda_evolution_tests test_direct_evolution.cpp)
target_link_libraries(rule30_cuda_evolution_tests PRIVATE rule30::cuda)
target_compile_features(rule30_cuda_evolution_tests PRIVATE cxx_std_20)
target_compile_options(
  rule30_cuda_evolution_tests PRIVATE -Wall -Wextra -Wpedantic
)
target_compile_definitions(
  rule30_cuda_evolution_tests
  PRIVATE
    RULE30_CENTER_VECTOR_PATH="${CMAKE_CURRENT_SOURCE_DIR}/../reference_vectors/center_c00000000_c00009999.u8"
)

add_test(NAME rule30_cuda_direct_evolution COMMAND rule30_cuda_evolution_tests)
set_tests_properties(
  rule30_cuda_direct_evolution PROPERTIES SKIP_RETURN_CODE 77
)

add_executable(rule30_cuda_sideways_tests test_batch_sideways.cpp)
target_link_libraries(rule30_cuda_sideways_tests PRIVATE rule30::cuda)
target_compile_features(rule30_cuda_sideways_tests PRIVATE cxx_std_20)
target_compile_options(
  rule30_cuda_sideways_tests PRIVATE -Wall -Wextra -Wpedantic
)
target_compile_definitions(
  rule30_cuda_sideways_tests
  PRIVATE
    RULE30_CENTER_VECTOR_PATH="${CMAKE_CURRENT_SOURCE_DIR}/../reference_vectors/center_c00000000_c00009999.u8"
)

add_test(NAME rule30_cuda_batch_sideways COMMAND rule30_cuda_sideways_tests)
set_tests_properties(
  rule30_cuda_batch_sideways PROPERTIES SKIP_RETURN_CODE 77
)

add_executable(
  rule30_cuda_generate_contract_tests
  test_generate_cli.cpp
)
target_link_libraries(rule30_cuda_generate_contract_tests PRIVATE rule30::cuda)
target_compile_features(
  rule30_cuda_generate_contract_tests PRIVATE cxx_std_20
)
target_compile_options(
  rule30_cuda_generate_contract_tests PRIVATE -Wall -Wextra -Wpedantic
)
add_dependencies(rule30_cuda_generate_contract_tests rule30_cuda_generate)

add_test(
  NAME rule30_cuda_generate_contract_cpu
  COMMAND
    rule30_cuda_generate_contract_tests cpu
    $<TARGET_FILE:rule30_cuda_generate>
    "${CMAKE_CURRENT_SOURCE_DIR}/../reference_vectors/center_c00000000_c00009999.u8"
)

add_test(
  NAME rule30_cuda_generate_contract_gpu
  COMMAND
    rule30_cuda_generate_contract_tests gpu
    $<TARGET_FILE:rule30_cuda_generate>
    "${CMAKE_CURRENT_SOURCE_DIR}/../reference_vectors/center_c00000000_c00009999.u8"
)
set_tests_properties(
  rule30_cuda_generate_contract_gpu PROPERTIES SKIP_RETURN_CODE 77
)
