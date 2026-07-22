#include "rule30_cuda/batch_period.hpp"
#include "rule30_cuda/direct_evolution.hpp"

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <exception>
#include <fstream>
#include <functional>
#include <iostream>
#include <iterator>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

#ifndef RULE30_CENTER_VECTOR_PATH
#error "RULE30_CENTER_VECTOR_PATH must name the frozen 10,000-bit vector"
#endif

namespace {

constexpr std::uint64_t kFnvOffsetBasis = 0xcbf29ce484222325ULL;
constexpr std::uint64_t kFnvPrime = 1099511628211ULL;

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

void expect_overflow_error(const std::function<void()>& function,
                           const std::string& description) {
  try {
    function();
  } catch (const std::overflow_error&) {
    return;
  }
  throw std::runtime_error("expected overflow_error: " + description);
}

std::uint64_t hash_bytes(const std::vector<std::uint8_t>& values) {
  std::uint64_t hash = kFnvOffsetBasis;
  for (const std::uint8_t value : values) {
    hash ^= value;
    hash *= kFnvPrime;
  }
  return hash;
}

std::uint64_t hash_words(const std::vector<std::uint64_t>& values) {
  std::uint64_t hash = kFnvOffsetBasis;
  for (const std::uint64_t value : values) {
    for (unsigned int byte = 0; byte < 8U; ++byte) {
      hash ^= (value >> (8U * byte)) & 0xffU;
      hash *= kFnvPrime;
    }
  }
  return hash;
}

rule30::cuda::DirectEvolutionResult cell_array_oracle(
    std::size_t center_bit_count) {
  rule30::cuda::DirectEvolutionResult result{};
  result.center_hash_fnv1a64 = kFnvOffsetBasis;
  result.final_row_hash_fnv1a64 = kFnvOffsetBasis;
  if (center_bit_count == 0) {
    return result;
  }

  const std::size_t width = center_bit_count * 2U - 1U;
  const std::size_t center = center_bit_count - 1U;
  std::vector<std::uint8_t> current(width, 0U);
  std::vector<std::uint8_t> next(width, 0U);
  current[center] = 1U;
  result.center_bits.assign(center_bit_count, 0U);
  result.center_bits[0] = 1U;

  for (std::size_t step = 1; step < center_bit_count; ++step) {
    const std::size_t low = center - step;
    const std::size_t high = center + step;
    for (std::size_t index = low; index <= high; ++index) {
      const std::uint8_t left = index == 0 ? 0U : current[index - 1U];
      const std::uint8_t middle = current[index];
      const std::uint8_t right =
          index + 1U == width ? 0U : current[index + 1U];
      next[index] = static_cast<std::uint8_t>(left ^ (middle | right));
    }
    result.center_bits[step] = next[center];
    std::swap(current, next);
  }

  result.final_row_words.assign(
      width / 64U + static_cast<std::size_t>(width % 64U != 0U), 0U);
  for (std::size_t index = 0; index < width; ++index) {
    result.final_row_words[index / 64U] |=
        static_cast<std::uint64_t>(current[index]) << (index & 63U);
  }
  result.center_ones = static_cast<std::uint64_t>(
      std::count(result.center_bits.begin(), result.center_bits.end(), 1U));
  result.center_zeros =
      static_cast<std::uint64_t>(center_bit_count) - result.center_ones;
  result.center_hash_fnv1a64 = hash_bytes(result.center_bits);
  result.final_row_hash_fnv1a64 = hash_words(result.final_row_words);
  return result;
}

std::size_t expected_word_updates(std::size_t center_bit_count) {
  if (center_bit_count < 2U) {
    return 0;
  }
  const std::size_t center = center_bit_count - 1U;
  std::size_t updates = 0;
  for (std::size_t step = 1; step < center_bit_count; ++step) {
    const std::size_t low_word = (center - step) / 64U;
    const std::size_t high_word = (center + step) / 64U;
    updates += high_word - low_word + 1U;
  }
  return updates;
}

void test_host_validation_and_empty_input() {
  rule30::cuda::DirectEvolutionConfig config{};
  expect_invalid_argument(
      [&] {
        auto invalid = config;
        invalid.device_index = -1;
        (void)rule30::cuda::evolve_single_history(1, invalid);
      },
      "negative device index");
  expect_invalid_argument(
      [&] {
        auto invalid = config;
        invalid.threads_per_block = 0;
        (void)rule30::cuda::evolve_single_history(1, invalid);
      },
      "zero threads per block");
  expect_invalid_argument(
      [&] {
        auto invalid = config;
        invalid.device_memory_budget_bytes = 0;
        (void)rule30::cuda::evolve_single_history(1, invalid);
      },
      "zero device budget");
  expect_invalid_argument(
      [&] {
        auto invalid = config;
        invalid.max_output_bytes = 88;
        (void)rule30::cuda::evolve_single_history(65, invalid);
      },
      "output budget below 65 bytes plus three packed words");
  expect_overflow_error(
      [&] {
        (void)rule30::cuda::evolve_single_history(
            std::numeric_limits<std::size_t>::max(), config);
      },
      "final row width");

  rule30::cuda::DirectEvolutionStats stats{};
  stats.kernel_launches = 99;
  const auto empty = rule30::cuda::evolve_single_history(0, config, &stats);
  require(empty.center_bits.empty() && empty.final_row_words.empty(),
          "zero bits must produce empty exact outputs");
  require(empty.center_ones == 0 && empty.center_zeros == 0,
          "zero bits must produce zero counts");
  require(empty.center_hash_fnv1a64 == kFnvOffsetBasis &&
              empty.final_row_hash_fnv1a64 == kFnvOffsetBasis,
          "empty hashes must use the documented FNV-1a offset basis");
  require(stats.kernel_launches == 0 && stats.center_bit_count == 0,
          "zero-bit statistics must report no work");
}

void test_counts_boundaries_and_independent_oracle() {
  const std::vector<std::size_t> counts{
      1,  2,  3,  31, 32, 33, 63, 64,
      65, 66, 95, 96, 97, 127, 128, 129, 257};

  for (const std::size_t count : counts) {
    rule30::cuda::DirectEvolutionConfig config{};
    // Seven threads intentionally leaves most active-word grids partial.
    config.threads_per_block = 7;
    config.device_memory_budget_bytes = 16ULL * 1024ULL * 1024ULL;
    rule30::cuda::DirectEvolutionStats stats{};
    const auto actual =
        rule30::cuda::evolve_single_history(count, config, &stats);
    const auto expected = cell_array_oracle(count);
    require(actual == expected,
            "GPU disagrees with independent cell-array oracle at N=" +
                std::to_string(count));

    const std::size_t row_bits = count * 2U - 1U;
    const std::size_t row_words =
        row_bits / 64U + static_cast<std::size_t>(row_bits % 64U != 0U);
    require(actual.center_bits.size() == count,
            "center output has an extra or missing final byte");
    require(actual.final_row_words.size() == row_words,
            "final packed row has an extra or missing word");
    require(stats.center_bit_count == count &&
                stats.final_row_bit_count == row_bits &&
                stats.final_row_word_count == row_words,
            "shape statistics are incorrect");
    require(stats.kernel_launches == count - 1U,
            "direct evolution must launch exactly once per dependent row");
    require(stats.row_word_updates == expected_word_updates(count),
            "active packed-word update accounting is incorrect");
    require(actual.center_ones + actual.center_zeros == count,
            "center one/zero counts do not cover the exact output");

    const unsigned int final_bits = static_cast<unsigned int>(row_bits & 63U);
    if (final_bits != 0U) {
      require((actual.final_row_words.back() >> final_bits) == 0U,
              "unused bits in the final partial packed word are nonzero");
    }
  }
}

void test_shared_center_vector() {
  std::ifstream input(RULE30_CENTER_VECTOR_PATH, std::ios::binary);
  require(input.good(), "cannot open the frozen 10,000-bit center vector");
  const std::vector<std::uint8_t> expected{
      std::istreambuf_iterator<char>(input), std::istreambuf_iterator<char>()};
  require(expected.size() == 10'000,
          "frozen center vector does not contain exactly 10,000 bytes");

  rule30::cuda::DirectEvolutionConfig config{};
  config.threads_per_block = 96;
  config.device_memory_budget_bytes = 32ULL * 1024ULL * 1024ULL;
  const auto actual = rule30::cuda::evolve_single_history(expected.size(), config);
  require(actual.center_bits == expected,
          "CUDA center output differs from the frozen shared vector");
  require(actual.center_ones == 5032 && actual.center_zeros == 4968,
          "10,000-bit balance checkpoint is incorrect");
}

void test_determinism_and_resource_limits(const rule30::cuda::DeviceInfo& device) {
  constexpr std::size_t kCount = 513;
  constexpr std::size_t kRowBits = kCount * 2U - 1U;
  constexpr std::size_t kRowWords =
      kRowBits / 64U + static_cast<std::size_t>(kRowBits % 64U != 0U);
  constexpr std::size_t kRequiredDeviceBytes =
      2U * kRowWords * sizeof(std::uint64_t) + kCount;

  rule30::cuda::DirectEvolutionConfig config{};
  config.threads_per_block = 13;
  config.device_memory_budget_bytes = kRequiredDeviceBytes;
  const auto first = rule30::cuda::evolve_single_history(kCount, config);
  const auto second = rule30::cuda::evolve_single_history(kCount, config);
  require(first == second, "direct evolution or its hashes are nondeterministic");

  expect_invalid_argument(
      [&] {
        auto too_small = config;
        too_small.device_memory_budget_bytes = kRequiredDeviceBytes - 1U;
        (void)rule30::cuda::evolve_single_history(kCount, too_small);
      },
      "device budget one byte below the exact buffer requirement");
  expect_invalid_argument(
      [&] {
        auto too_many_threads = config;
        too_many_threads.threads_per_block = device.max_threads_per_block + 1;
        (void)rule30::cuda::evolve_single_history(2, too_many_threads);
      },
      "threads per block above the device limit");
}

}  // namespace

int main() {
  try {
    test_host_validation_and_empty_input();

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
    test_counts_boundaries_and_independent_oracle();
    test_shared_center_vector();
    test_determinism_and_resource_limits(device);

    std::cout << "All CUDA direct-evolution tests passed on " << device.name
              << '\n';
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "CUDA direct-evolution test failure: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
