#include "rule30_cuda/batch_period.hpp"
#include "rule30_cuda/batch_sideways.hpp"

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <exception>
#include <fstream>
#include <functional>
#include <iostream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <vector>

#ifndef RULE30_CENTER_VECTOR_PATH
#error "RULE30_CENTER_VECTOR_PATH must name the frozen 10,000-bit vector"
#endif

namespace {

void require(bool condition, const std::string& message) {
  if (!condition) {
    throw std::runtime_error(message);
  }
}

void expect_invalid_argument(const std::function<void()>& function,
                             const std::string& description) {
  try {
    function();
  } catch (const std::invalid_argument&) {
    return;
  }
  throw std::runtime_error("expected invalid_argument: " + description);
}

std::vector<std::uint8_t> reconstruct_cpu_one(
    const std::vector<std::uint8_t>& center) {
  const std::size_t horizon = center.size() - 1U;
  std::vector<std::vector<std::uint8_t>> right(
      horizon + 1U, std::vector<std::uint8_t>(horizon + 2U, 0U));
  for (std::size_t time = 0; time <= horizon; ++time) {
    right[time][0] = center[time];
  }
  for (std::size_t time = 0; time < horizon; ++time) {
    for (std::size_t position = 1; position <= horizon; ++position) {
      right[time + 1U][position] = static_cast<std::uint8_t>(
          right[time][position - 1U] ^
          (right[time][position] | right[time][position + 1U]));
    }
  }

  std::vector<std::uint8_t> current = center;
  std::vector<std::uint8_t> neighbor(horizon + 1U);
  for (std::size_t time = 0; time <= horizon; ++time) {
    neighbor[time] = right[time][1];
  }
  std::vector<std::uint8_t> reconstructed;
  reconstructed.reserve(horizon);
  for (std::size_t depth = 1; depth <= horizon; ++depth) {
    const std::size_t length = horizon + 1U - depth;
    std::vector<std::uint8_t> next(length);
    for (std::size_t time = 0; time < length; ++time) {
      next[time] = static_cast<std::uint8_t>(
          current[time + 1U] ^ (current[time] | neighbor[time]));
    }
    reconstructed.push_back(next[0]);
    neighbor.assign(current.begin(), current.begin() + length);
    current = std::move(next);
  }
  return reconstructed;
}

std::vector<std::uint8_t> reconstruct_cpu_batch(
    const std::vector<std::uint8_t>& traces, std::size_t trace_length) {
  const std::size_t count = traces.size() / trace_length;
  const std::size_t horizon = trace_length - 1U;
  std::vector<std::uint8_t> output;
  output.reserve(count * horizon);
  for (std::size_t candidate = 0; candidate < count; ++candidate) {
    const auto begin = traces.begin() + candidate * trace_length;
    const std::vector<std::uint8_t> trace(begin, begin + trace_length);
    const auto reconstructed = reconstruct_cpu_one(trace);
    output.insert(output.end(), reconstructed.begin(), reconstructed.end());
  }
  return output;
}

std::uint64_t next_random(std::uint64_t& state) {
  state ^= state << 13U;
  state ^= state >> 7U;
  state ^= state << 17U;
  return state;
}

std::vector<std::uint8_t> deterministic_traces(std::size_t count,
                                               std::size_t trace_length,
                                               std::uint64_t seed) {
  std::vector<std::uint8_t> traces(count * trace_length);
  for (auto& bit : traces) {
    bit = static_cast<std::uint8_t>(next_random(seed) & 1U);
  }
  return traces;
}

void test_host_validation_and_zero_work() {
  rule30::cuda::SidewaysBatchConfig config{};
  expect_invalid_argument(
      [&] {
        (void)rule30::cuda::reconstruct_left_initial_batch({}, 0, config);
      },
      "zero trace length");
  expect_invalid_argument(
      [&] {
        const std::vector<std::uint8_t> traces{0, 1, 0};
        (void)rule30::cuda::reconstruct_left_initial_batch(traces, 2, config);
      },
      "nonintegral flattened trace count");
  expect_invalid_argument(
      [&] {
        const std::vector<std::uint8_t> traces{0, 2};
        (void)rule30::cuda::reconstruct_left_initial_batch(traces, 2, config);
      },
      "nonbinary center byte");
  expect_invalid_argument(
      [&] {
        const std::vector<std::uint8_t> traces(6, 0U);
        auto bounded = config;
        bounded.max_horizon = 1;
        (void)rule30::cuda::reconstruct_left_initial_batch(traces, 3, bounded);
      },
      "horizon above explicit bound");
  expect_invalid_argument(
      [&] {
        const std::vector<std::uint8_t> traces(10, 0U);
        auto limited = config;
        limited.max_output_bytes = 7;
        (void)rule30::cuda::reconstruct_left_initial_batch(traces, 5, limited);
      },
      "host output budget");

  rule30::cuda::SidewaysBatchStats empty_stats{};
  const auto empty = rule30::cuda::reconstruct_left_initial_batch(
      std::vector<std::uint8_t>{}, 7, config, &empty_stats);
  require(empty.empty() && empty_stats.candidates_evaluated == 0 &&
              empty_stats.horizon == 6 && empty_stats.chunks == 0,
          "empty batch accounting is incorrect");

  rule30::cuda::SidewaysBatchStats zero_horizon_stats{};
  const std::vector<std::uint8_t> single_samples{1, 0, 1};
  const auto zero_horizon = rule30::cuda::reconstruct_left_initial_batch(
      single_samples, 1, config, &zero_horizon_stats);
  require(zero_horizon.empty() &&
              zero_horizon_stats.candidates_evaluated == 3 &&
              zero_horizon_stats.horizon == 0 &&
              zero_horizon_stats.chunks == 0,
          "zero-horizon traces should require no GPU work or output");
}

void test_small_horizons_against_cpu_oracle() {
  for (const std::size_t horizon : {1U, 2U, 3U, 31U, 32U, 33U, 64U}) {
    const std::size_t trace_length = horizon + 1U;
    const auto traces = deterministic_traces(
        17, trace_length, 0x9e3779b97f4a7c15ULL + horizon);
    const auto expected = reconstruct_cpu_batch(traces, trace_length);

    rule30::cuda::SidewaysBatchConfig config{};
    config.threads_per_block = 7;
    config.device_memory_budget_bytes = 8ULL * 1024ULL * 1024ULL;
    config.max_horizon = 64;
    const auto actual = rule30::cuda::reconstruct_left_initial_batch(
        traces, trace_length, config);
    require(actual == expected,
            "GPU sideways result differs from CPU oracle at horizon=" +
                std::to_string(horizon));
  }
}

void test_true_trace_reconstructs_zero_tail() {
  std::ifstream input(RULE30_CENTER_VECTOR_PATH, std::ios::binary);
  require(input.good(), "cannot open the frozen center vector");
  std::vector<std::uint8_t> trace(129);
  input.read(reinterpret_cast<char*>(trace.data()),
             static_cast<std::streamsize>(trace.size()));
  require(input.gcount() == static_cast<std::streamsize>(trace.size()),
          "frozen center vector is shorter than the test trace");

  rule30::cuda::SidewaysBatchConfig config{};
  config.threads_per_block = 32;
  config.max_horizon = 128;
  const auto actual = rule30::cuda::reconstruct_left_initial_batch(
      trace, trace.size(), config);
  require(actual.size() == 128,
          "true-trace reconstruction has the wrong finite horizon");
  require(std::all_of(actual.begin(), actual.end(),
                      [](std::uint8_t bit) { return bit == 0U; }),
          "true center trace did not reconstruct an all-zero finite left tail");
  require(actual == reconstruct_cpu_one(trace),
          "true-trace CUDA and CPU reconstructions disagree");
}

void test_chunking_uneven_grid_determinism_and_limits(
    const rule30::cuda::DeviceInfo& device) {
  constexpr std::size_t kCount = 1003;
  constexpr std::size_t kTraceLength = 64;
  constexpr std::size_t kHorizon = kTraceLength - 1U;
  const auto traces = deterministic_traces(
      kCount, kTraceLength, 0x243f6a8885a308d3ULL);
  const auto expected = reconstruct_cpu_batch(traces, kTraceLength);

  rule30::cuda::SidewaysBatchConfig config{};
  config.threads_per_block = 96;
  config.max_chunk_candidates = 197;
  config.device_memory_budget_bytes = 16ULL * 1024ULL * 1024ULL;
  config.max_horizon = kHorizon;
  rule30::cuda::SidewaysBatchStats first_stats{};
  const auto first = rule30::cuda::reconstruct_left_initial_batch(
      traces, kTraceLength, config, &first_stats);
  rule30::cuda::SidewaysBatchStats second_stats{};
  const auto second = rule30::cuda::reconstruct_left_initial_batch(
      traces, kTraceLength, config, &second_stats);

  require(first == expected,
          "multi-chunk sideways result differs from the CPU oracle");
  require(second == first,
          "multi-chunk sideways reconstruction is nondeterministic");
  require(first_stats.chunk_capacity == 197 && first_stats.chunks == 6,
          "1003 candidates in chunks of 197 must require six launches");
  require(first_stats.peak_device_bytes <=
              config.device_memory_budget_bytes,
          "reported sideways peak exceeds its configured device budget");
  require(first_stats.kernel_milliseconds >= 0.0 &&
              first_stats.host_to_device_milliseconds >= 0.0 &&
              first_stats.device_to_host_milliseconds >= 0.0 &&
              first_stats.end_to_end_milliseconds >=
                  first_stats.kernel_milliseconds,
          "sideways timings are inconsistent");

  constexpr std::size_t kWorkspaceBytes = 3U * (kHorizon + 2U);
  constexpr std::size_t kBytesPerCandidate =
      kTraceLength + kHorizon + kWorkspaceBytes;
  expect_invalid_argument(
      [&] {
        auto too_small = config;
        too_small.max_chunk_candidates = 1;
        too_small.device_memory_budget_bytes = kBytesPerCandidate - 1U;
        const std::vector<std::uint8_t> one_trace(traces.begin(),
                                                  traces.begin() + kTraceLength);
        (void)rule30::cuda::reconstruct_left_initial_batch(
            one_trace, kTraceLength, too_small);
      },
      "device budget below one trace, output, and workspace");
  expect_invalid_argument(
      [&] {
        auto too_many_threads = config;
        too_many_threads.threads_per_block = device.max_threads_per_block + 1;
        const std::vector<std::uint8_t> one_trace(traces.begin(),
                                                  traces.begin() + kTraceLength);
        (void)rule30::cuda::reconstruct_left_initial_batch(
            one_trace, kTraceLength, too_many_threads);
      },
      "threads per block above the device limit");
}

}  // namespace

int main() {
  try {
    test_host_validation_and_zero_work();

    int count = 0;
    try {
      count = rule30::cuda::device_count();
    } catch (const std::exception& error) {
      std::cerr << "SKIP: CUDA runtime unavailable: " << error.what() << '\n';
      return 77;
    }
    if (count == 0) {
      std::cerr << "SKIP: no CUDA device available\n";
      return 77;
    }
    const auto device = rule30::cuda::probe_device(0);
    require(device.compute_major == 7 && device.compute_minor == 5,
            "tests require the assigned sm_75 GPU");

    test_small_horizons_against_cpu_oracle();
    test_true_trace_reconstructs_zero_tail();
    test_chunking_uneven_grid_determinism_and_limits(device);
    std::cout << "All CUDA batched-sideways tests passed on " << device.name
              << '\n';
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "CUDA batched-sideways test failure: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
