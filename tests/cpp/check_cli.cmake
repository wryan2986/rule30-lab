if(NOT DEFINED RULE30_CLI OR NOT DEFINED RULE30_TEST_DIRECTORY)
  message(FATAL_ERROR "RULE30_CLI and RULE30_TEST_DIRECTORY are required")
endif()

file(MAKE_DIRECTORY "${RULE30_TEST_DIRECTORY}")
set(raw_output "${RULE30_TEST_DIRECTORY}/center-nine.bin")
set(empty_output "${RULE30_TEST_DIRECTORY}/center-empty.bin")

execute_process(
  COMMAND "${RULE30_CLI}" generate --count 9 --backend scalar --format raw
          --chunk-size 3
  OUTPUT_FILE "${raw_output}"
  ERROR_VARIABLE raw_error
  RESULT_VARIABLE raw_result
)
if(NOT raw_result EQUAL 0)
  message(FATAL_ERROR "raw CLI failed (${raw_result}): ${raw_error}")
endif()
file(SIZE "${raw_output}" raw_size)
if(NOT raw_size EQUAL 9)
  message(FATAL_ERROR "raw CLI wrote ${raw_size} bytes instead of 9")
endif()
file(READ "${raw_output}" raw_hex HEX)
if(NOT raw_hex STREQUAL "010100010101000001")
  message(FATAL_ERROR "raw CLI bytes mismatch: ${raw_hex}")
endif()

execute_process(
  COMMAND "${RULE30_CLI}" generate --count 0 --backend scalar --format raw
  OUTPUT_FILE "${empty_output}"
  ERROR_VARIABLE empty_error
  RESULT_VARIABLE empty_result
)
if(NOT empty_result EQUAL 0)
  message(FATAL_ERROR "empty raw CLI failed (${empty_result}): ${empty_error}")
endif()
file(SIZE "${empty_output}" empty_size)
if(NOT empty_size EQUAL 0)
  message(FATAL_ERROR "N=0 raw CLI wrote ${empty_size} bytes")
endif()

execute_process(
  COMMAND "${RULE30_CLI}" generate --count 9 --backend scalar --format json
          --checkpoint 9 --checkpoint 3
  OUTPUT_VARIABLE json_output
  ERROR_VARIABLE json_error
  RESULT_VARIABLE json_result
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
if(NOT json_result EQUAL 0)
  message(FATAL_ERROR "JSON CLI failed (${json_result}): ${json_error}")
endif()
string(JSON json_count GET "${json_output}" count)
string(JSON json_ones GET "${json_output}" ones)
string(JSON json_discrepancy GET "${json_output}" discrepancy)
string(JSON json_backend GET "${json_output}" backend)
string(JSON checkpoint_count LENGTH "${json_output}" checkpoints)
if(NOT json_count EQUAL 9 OR NOT json_ones EQUAL 6 OR
   NOT json_discrepancy EQUAL 3 OR NOT json_backend STREQUAL "scalar" OR
   NOT checkpoint_count EQUAL 2)
  message(FATAL_ERROR "unexpected JSON summary: ${json_output}")
endif()

execute_process(
  COMMAND "${RULE30_CLI}" benchmark --count 64 --backend scalar --warmup 0
          --repetitions 2
  OUTPUT_VARIABLE benchmark_output
  ERROR_VARIABLE benchmark_error
  RESULT_VARIABLE benchmark_result
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
if(NOT benchmark_result EQUAL 0)
  message(FATAL_ERROR
          "benchmark CLI failed (${benchmark_result}): ${benchmark_error}")
endif()
string(JSON benchmark_count GET "${benchmark_output}" count)
string(JSON benchmark_repetitions GET "${benchmark_output}" repetitions)
string(JSON benchmark_median GET "${benchmark_output}" seconds median)
if(NOT benchmark_count EQUAL 64 OR NOT benchmark_repetitions EQUAL 2 OR
   benchmark_median LESS 0)
  message(FATAL_ERROR "unexpected benchmark JSON: ${benchmark_output}")
endif()
