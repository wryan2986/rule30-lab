#include "rule30_cuda/batch_period.hpp"

#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <exception>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using rule30::cuda::PeriodCandidate;
using rule30::cuda::PeriodResult;

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

PeriodResult cpu_oracle(const std::vector<std::uint8_t>& bits,
                        const PeriodCandidate& candidate) {
  PeriodResult result{};
  for (std::uint64_t t = candidate.start; t < candidate.end; ++t) {
    ++result.comparisons_checked;
    if (bits.at(static_cast<std::size_t>(t)) !=
        bits.at(static_cast<std::size_t>(t - candidate.period))) {
      result.first_mismatch = t;
      result.matches = 0;
      return result;
    }
  }
  result.matches = 1;
  return result;
}

std::vector<PeriodResult> cpu_oracle(
    const std::vector<std::uint8_t>& bits,
    const std::vector<PeriodCandidate>& candidates) {
  std::vector<PeriodResult> output;
  output.reserve(candidates.size());
  for (const auto& candidate : candidates) {
    output.push_back(cpu_oracle(bits, candidate));
  }
  return output;
}

std::uint64_t next_random(std::uint64_t& state) {
  state ^= state << 13;
  state ^= state >> 7;
  state ^= state << 17;
  return state;
}

void test_host_validation() {
  const std::vector<std::uint8_t> bits{1, 0, 1, 1};
  rule30::cuda::BatchConfig config{};

  expect_invalid_argument(
      [&] {
        const std::vector<PeriodCandidate> candidates{{1, 4, 0}};
        (void)rule30::cuda::evaluate_period_candidates(bits, candidates, config);
      },
      "zero period");
  expect_invalid_argument(
      [&] {
        const std::vector<PeriodCandidate> candidates{{0, 2, 1}};
        (void)rule30::cuda::evaluate_period_candidates(bits, candidates, config);
      },
      "start before period");
  expect_invalid_argument(
      [&] {
        const std::vector<PeriodCandidate> candidates{{3, 2, 1}};
        (void)rule30::cuda::evaluate_period_candidates(bits, candidates, config);
      },
      "reversed range");
  expect_invalid_argument(
      [&] {
        const std::vector<PeriodCandidate> candidates{{1, 5, 1}};
        (void)rule30::cuda::evaluate_period_candidates(bits, candidates, config);
      },
      "range beyond sequence");
  expect_invalid_argument(
      [&] {
        const std::vector<PeriodCandidate> candidates{{1, 4, 1}};
        auto bad_config = config;
        bad_config.max_output_bytes = sizeof(PeriodResult) - 1;
        (void)rule30::cuda::evaluate_period_candidates(bits, candidates,
                                                       bad_config);
      },
      "output budget");

  rule30::cuda::BatchStats stats{};
  const auto empty = rule30::cuda::evaluate_period_candidates(
      std::vector<std::uint8_t>{}, std::vector<PeriodCandidate>{}, config,
      &stats);
  require(empty.empty(), "empty batch should produce no output");
  require(stats.candidates_evaluated == 0 && stats.chunks == 0,
          "empty batch should report zero work");
}

void test_known_periods() {
  const std::vector<std::uint8_t> pattern{1, 0, 1, 1, 0, 0, 1};
  std::vector<std::uint8_t> bits(4099);
  for (std::size_t index = 0; index < bits.size(); ++index) {
    bits[index] = pattern[index % pattern.size()];
  }

  const std::vector<PeriodCandidate> candidates{
      {7, bits.size(), 7},
      {14, bits.size(), 14},
      {21, 21, 7},
      {1, bits.size(), 1},
      {8, 1025, 8},
  };
  const auto expected = cpu_oracle(bits, candidates);

  rule30::cuda::BatchConfig config{};
  config.threads_per_block = 128;
  rule30::cuda::BatchStats stats{};
  const auto actual = rule30::cuda::evaluate_period_candidates(
      bits, candidates, config, &stats);
  require(actual == expected, "known-period GPU results differ from CPU oracle");
  require(actual[0].matches == 1 && actual[1].matches == 1,
          "known multiples of the base period should match");
  require(actual[2].matches == 1 && actual[2].comparisons_checked == 0,
          "empty comparison range should match vacuously");
  require(actual[3].matches == 0,
          "period one should fail for the nonconstant pattern");
  require(actual[3].first_mismatch == 1 &&
              actual[3].comparisons_checked == 1,
          "first mismatch location or comparison count is incorrect");
  require(stats.chunks == 1 && stats.candidates_evaluated == candidates.size(),
          "small batch accounting is incorrect");
  require(stats.end_to_end_milliseconds >= stats.kernel_milliseconds,
          "end-to-end timing should include kernel timing");
}

void test_chunking_uneven_grid_and_determinism() {
  std::uint64_t state = 0x9e3779b97f4a7c15ULL;
  std::vector<std::uint8_t> bits(8191);
  for (auto& bit : bits) {
    bit = static_cast<std::uint8_t>(next_random(state) & 1U);
  }

  std::vector<PeriodCandidate> candidates;
  candidates.reserve(1003);
  for (std::size_t index = 0; index < 1003; ++index) {
    const std::size_t period = 1 + next_random(state) % 193;
    const std::size_t start = period + next_random(state) % 300;
    const std::size_t maximum_length = std::min<std::size_t>(997, bits.size() - start);
    const std::size_t length = next_random(state) % (maximum_length + 1);
    candidates.push_back({start, start + length, period});
  }
  const auto expected = cpu_oracle(bits, candidates);

  rule30::cuda::BatchConfig config{};
  config.threads_per_block = 96;
  config.device_memory_budget_bytes =
      bits.size() + 197 * (sizeof(PeriodCandidate) + sizeof(PeriodResult));
  rule30::cuda::BatchStats first_stats{};
  const auto first = rule30::cuda::evaluate_period_candidates(
      bits, candidates, config, &first_stats);
  rule30::cuda::BatchStats second_stats{};
  const auto second = rule30::cuda::evaluate_period_candidates(
      bits, candidates, config, &second_stats);

  require(first == expected, "chunked GPU results differ from CPU oracle");
  require(second == first, "repeated deterministic GPU run changed results");
  require(first_stats.chunk_capacity == 197,
          "memory budget did not produce the expected chunk capacity");
  require(first_stats.chunks == 6,
          "1003 candidates in chunks of 197 should require six launches");
  require(first_stats.peak_device_bytes <=
              config.device_memory_budget_bytes,
          "reported peak device memory exceeds the configured budget");
  require(first_stats.kernel_milliseconds >= 0.0 &&
              first_stats.host_to_device_milliseconds >= 0.0 &&
              first_stats.device_to_host_milliseconds >= 0.0,
          "timings must be nonnegative");
}

void test_different_batch_sizes() {
  std::vector<std::uint8_t> bits(2048);
  for (std::size_t index = 0; index < bits.size(); ++index) {
    bits[index] = static_cast<std::uint8_t>((index * 17U + index / 5U) & 1U);
  }

  for (const std::size_t count : {1U, 95U, 96U, 97U, 257U}) {
    std::vector<PeriodCandidate> candidates;
    candidates.reserve(count);
    for (std::size_t index = 0; index < count; ++index) {
      const std::size_t period = 1 + index % 31;
      candidates.push_back({period, 1024 + index % 257, period});
    }
    const auto expected = cpu_oracle(bits, candidates);
    rule30::cuda::BatchConfig config{};
    config.threads_per_block = 96;
    const auto actual =
        rule30::cuda::evaluate_period_candidates(bits, candidates, config);
    require(actual == expected,
            "GPU disagreement at batch size " + std::to_string(count));
  }
}

void test_too_small_device_budget() {
  const std::vector<std::uint8_t> bits(1024, 0);
  const std::vector<PeriodCandidate> candidates{{1, bits.size(), 1}};
  rule30::cuda::BatchConfig config{};
  config.device_memory_budget_bytes = bits.size();
  expect_invalid_argument(
      [&] {
        (void)rule30::cuda::evaluate_period_candidates(bits, candidates, config);
      },
      "device memory budget too small for one candidate");
}

}  // namespace

int main() {
  try {
    test_host_validation();

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
    require(device.total_global_memory_bytes > 0,
            "device probe reported zero global memory");
    require(device.max_threads_per_block >= 256,
            "device probe reported an implausibly small block limit");
    require(device.max_grid_size_x > 0,
            "device probe reported an invalid x-grid limit");

    test_known_periods();
    test_chunking_uneven_grid_and_determinism();
    test_different_batch_sizes();
    test_too_small_device_budget();

    std::cout << "All CUDA batch-period tests passed on " << device.name << "\n";
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "CUDA test failure: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
