#define RULE30_EXTENDED_PERIOD_SEARCH_NO_MAIN
#include "../../src/cuda/extended_period_search.cpp"

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <exception>
#include <functional>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace search = rule30::cuda::extended_period_search;

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

search::SearchConfig base_cpu_config() {
  search::SearchConfig config{};
  config.backend = search::Backend::kCpu;
  config.minimum_preperiod = 0;
  config.maximum_preperiod = 0;
  config.minimum_period = 1;
  config.maximum_period = 3;
  config.horizon = 12;
  config.maximum_evaluation_chunk = 5;
  config.host_memory_budget_bytes = 8ULL * 1024ULL * 1024ULL;
  config.device_memory_budget_bytes = 8ULL * 1024ULL * 1024ULL;
  config.maximum_output_bytes = 64ULL * 1024ULL;
  config.maximum_witnesses = 64;
  return config;
}

std::vector<std::uint8_t> naive_reconstruct(
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
  std::vector<std::uint8_t> neighbor(horizon + 1U, 0U);
  for (std::size_t time = 0; time <= horizon; ++time) {
    neighbor[time] = right[time][1];
  }
  std::vector<std::uint8_t> output;
  for (std::size_t depth = 1; depth <= horizon; ++depth) {
    const std::size_t length = center.size() - depth;
    std::vector<std::uint8_t> next(length, 0U);
    for (std::size_t time = 0; time < length; ++time) {
      next[time] = static_cast<std::uint8_t>(
          current[time + 1U] ^ (current[time] | neighbor[time]));
    }
    output.push_back(next[0]);
    neighbor.assign(current.begin(), current.begin() + length);
    current = std::move(next);
  }
  return output;
}

struct BruteSummary {
  std::uint64_t seed_descriptions{};
  std::uint64_t unique_traces{};
  std::uint64_t duplicate_descriptions{};
  std::uint64_t compatible_traces{};
  std::uint64_t incompatible_traces{};
  std::uint64_t compatible_descriptions{};
  std::uint64_t incompatible_descriptions{};
  std::map<std::size_t, std::pair<std::uint64_t, std::uint64_t>> histogram;
};

BruteSummary brute_force(const search::SearchConfig& config) {
  std::map<std::vector<std::uint8_t>, std::uint64_t> traces;
  BruteSummary summary{};
  for (std::size_t preperiod = config.minimum_preperiod;
       preperiod <= config.maximum_preperiod; ++preperiod) {
    for (std::size_t period = config.minimum_period;
         period <= config.maximum_period; ++period) {
      const std::uint64_t count = 1ULL << (preperiod + period);
      for (std::uint64_t code = 0; code < count; ++code) {
        std::vector<std::uint8_t> trace(config.horizon + 1U, 0U);
        for (std::size_t time = 0; time <= config.horizon; ++time) {
          const std::size_t bit_index =
              time < preperiod
                  ? time
                  : preperiod + (time - preperiod) % period;
          trace[time] = static_cast<std::uint8_t>((code >> bit_index) & 1U);
        }
        if (trace[0] == 0U) {
          continue;
        }
        ++summary.seed_descriptions;
        ++traces[trace];
      }
    }
  }
  summary.unique_traces = traces.size();
  summary.duplicate_descriptions = summary.seed_descriptions - traces.size();
  for (const auto& [trace, multiplicity] : traces) {
    const auto tail = naive_reconstruct(trace);
    const auto found = std::find(tail.begin(), tail.end(), 1U);
    if (found == tail.end()) {
      ++summary.compatible_traces;
      summary.compatible_descriptions += multiplicity;
    } else {
      ++summary.incompatible_traces;
      summary.incompatible_descriptions += multiplicity;
      const std::size_t depth =
          static_cast<std::size_t>(found - tail.begin()) + 1U;
      ++summary.histogram[depth].first;
      summary.histogram[depth].second += multiplicity;
    }
  }
  return summary;
}

void require_same_finite_results(const search::SearchResult& left,
                                 const search::SearchResult& right,
                                 const std::string& context) {
  const auto& a = left.stats;
  const auto& b = right.stats;
  require(a.descriptions_total == b.descriptions_total &&
              a.descriptions_rejected_c0 == b.descriptions_rejected_c0 &&
              a.descriptions_seed_compatible ==
                  b.descriptions_seed_compatible &&
              a.distinct_trace_sequences == b.distinct_trace_sequences &&
              a.duplicate_descriptions == b.duplicate_descriptions &&
              a.traces_evaluated == b.traces_evaluated &&
              a.finite_compatible_traces == b.finite_compatible_traces &&
              a.finite_incompatible_traces == b.finite_incompatible_traces &&
              a.finite_compatible_descriptions ==
                  b.finite_compatible_descriptions &&
              a.finite_incompatible_descriptions ==
                  b.finite_incompatible_descriptions,
          context + ": exact totals differ");
  require(left.first_nonzero_histogram.size() ==
              right.first_nonzero_histogram.size(),
          context + ": histogram lengths differ");
  for (std::size_t index = 0; index < left.first_nonzero_histogram.size();
       ++index) {
    const auto& x = left.first_nonzero_histogram[index];
    const auto& y = right.first_nonzero_histogram[index];
    require(x.depth == y.depth && x.distinct_traces == y.distinct_traces &&
                x.descriptions == y.descriptions,
            context + ": histogram bins differ");
  }
  require(left.witnesses.size() == right.witnesses.size(),
          context + ": witness counts differ");
  for (std::size_t index = 0; index < left.witnesses.size(); ++index) {
    const auto& x = left.witnesses[index];
    const auto& y = right.witnesses[index];
    require(x.canonical_description.preperiod ==
                    y.canonical_description.preperiod &&
                x.canonical_description.period ==
                    y.canonical_description.period &&
                x.canonical_description.code == y.canonical_description.code &&
                x.first_nonzero_left_depth == y.first_nonzero_left_depth &&
                x.represented_descriptions == y.represented_descriptions,
            context + ": compact witnesses differ");
  }
}

void test_validation_and_caps() {
  const auto base = base_cpu_config();
  expect_invalid_argument(
      [&] {
        auto invalid = base;
        invalid.minimum_period = 0;
        (void)search::run_search(invalid);
      },
      "zero period");
  expect_invalid_argument(
      [&] {
        auto invalid = base;
        invalid.horizon = 2;
        (void)search::run_search(invalid);
      },
      "horizon shorter than description");
  expect_invalid_argument(
      [&] {
        auto invalid = base;
        invalid.maximum_preperiod = 32;
        invalid.minimum_period = 32;
        invalid.maximum_period = 32;
        invalid.horizon = 64;
        (void)search::run_search(invalid);
      },
      "64-bit description");
  expect_invalid_argument(
      [&] {
        auto invalid = base;
        invalid.host_memory_budget_bytes = 64;
        (void)search::run_search(invalid);
      },
      "host memory cap");
  expect_invalid_argument(
      [&] {
        auto invalid = base;
        invalid.maximum_output_bytes = 1;
        (void)search::run_search(invalid);
      },
      "materialized output cap");

  auto small_report = base;
  small_report.maximum_output_bytes = 128;
  const auto result = search::run_search(small_report);
  expect_invalid_argument([&] { (void)search::result_json(result); },
                          "serialized report cap");
}

void test_c0_filter_and_duplicate_accounting() {
  auto config = base_cpu_config();
  config.maximum_period = 2;
  config.horizon = 8;
  const auto result = search::run_search(config);
  require(result.stats.descriptions_total == 6,
          "periods 1..2 must cover six descriptions");
  require(result.stats.descriptions_rejected_c0 == 3 &&
              result.stats.descriptions_seed_compatible == 3,
          "c0=1 filtering must reject exactly the even description codes");
  require(result.stats.distinct_trace_sequences == 2 &&
              result.stats.duplicate_descriptions == 1,
          "period-one all-ones and period-two 11 must be one trace sequence");
  require(result.stats.traces_evaluated == 2,
          "duplicate descriptions must not be reevaluated");
}

void test_cpu_oracle_against_independent_bruteforce() {
  auto config = base_cpu_config();
  config.maximum_preperiod = 2;
  config.maximum_period = 3;
  config.horizon = 10;
  config.maximum_evaluation_chunk = 3;
  const auto expected = brute_force(config);
  const auto actual = search::run_search(config);
  require(actual.stats.descriptions_seed_compatible ==
                  expected.seed_descriptions &&
              actual.stats.distinct_trace_sequences == expected.unique_traces &&
              actual.stats.duplicate_descriptions ==
                  expected.duplicate_descriptions &&
              actual.stats.finite_compatible_traces ==
                  expected.compatible_traces &&
              actual.stats.finite_incompatible_traces ==
                  expected.incompatible_traces &&
              actual.stats.finite_compatible_descriptions ==
                  expected.compatible_descriptions &&
              actual.stats.finite_incompatible_descriptions ==
                  expected.incompatible_descriptions,
          "CPU path differs from independent brute-force accounting");
  require(actual.first_nonzero_histogram.size() == expected.histogram.size(),
          "CPU path differs from independent brute-force histogram size");
  for (const auto& bin : actual.first_nonzero_histogram) {
    const auto expected_bin = expected.histogram.at(bin.depth);
    require(bin.distinct_traces == expected_bin.first &&
                bin.descriptions == expected_bin.second,
            "CPU path differs from independent brute-force histogram");
  }
}

void test_cpu_chunk_boundaries_and_determinism() {
  auto small_chunks = base_cpu_config();
  small_chunks.maximum_preperiod = 2;
  small_chunks.maximum_period = 4;
  small_chunks.horizon = 16;
  small_chunks.maximum_evaluation_chunk = 3;
  const auto first = search::run_search(small_chunks);
  const auto second = search::run_search(small_chunks);
  require_same_finite_results(first, second, "repeated CPU search");
  require(first.stats.evaluation_chunks > 1,
          "small CPU chunks should cross chunk boundaries");

  auto one_chunk = small_chunks;
  one_chunk.maximum_evaluation_chunk = 10000;
  const auto unchunked = search::run_search(one_chunk);
  require_same_finite_results(first, unchunked,
                              "chunked versus unchunked CPU search");
  const auto json = search::result_json(first);
  require(json.find("finite reconstruction horizon only") != std::string::npos,
          "JSON must state the finite claim scope");
}

void run_cpu_tests() {
  test_validation_and_caps();
  test_c0_filter_and_duplicate_accounting();
  test_cpu_oracle_against_independent_bruteforce();
  test_cpu_chunk_boundaries_and_determinism();
}

void run_gpu_tests() {
  int count = 0;
  try {
    count = rule30::cuda::device_count();
  } catch (const std::exception& error) {
    std::cerr << "SKIP: CUDA runtime unavailable: " << error.what() << '\n';
    std::exit(77);
  }
  if (count == 0) {
    std::cerr << "SKIP: no CUDA device available\n";
    std::exit(77);
  }
  const auto device = rule30::cuda::probe_device(0);
  require(device.compute_major == 7 && device.compute_minor == 5,
          "extended search tests require the assigned sm_75 GPU");

  auto cpu_config = base_cpu_config();
  cpu_config.minimum_period = 6;
  cpu_config.maximum_period = 6;
  cpu_config.horizon = 31;
  cpu_config.maximum_evaluation_chunk = 17;
  cpu_config.threads_per_block = 7;
  const auto expected = search::run_search(cpu_config);
  require(expected.stats.distinct_trace_sequences == 32,
          "fixed period six with c0=1 must produce 32 distinct traces");
  require(expected.stats.evaluation_chunks == 2,
          "32 traces in chunks of 17 must cross one chunk boundary");

  auto gpu_config = cpu_config;
  gpu_config.backend = search::Backend::kCuda;
  const auto actual = search::run_search(gpu_config);
  require_same_finite_results(expected, actual,
                              "CPU versus CUDA uneven-grid search");
  require(actual.stats.evaluation_chunks == 2,
          "CUDA outer search must retain exact chunk accounting");
  require(actual.stats.period_kernel_milliseconds >= 0.0 &&
              actual.stats.sideways_kernel_milliseconds >= 0.0 &&
              actual.stats.period_end_to_end_milliseconds >=
                  actual.stats.period_kernel_milliseconds &&
              actual.stats.sideways_end_to_end_milliseconds >=
                  actual.stats.sideways_kernel_milliseconds &&
              actual.stats.peak_device_bytes <=
                  gpu_config.device_memory_budget_bytes,
          "CUDA resource or timing accounting is inconsistent");

  auto smaller_chunks = gpu_config;
  smaller_chunks.maximum_evaluation_chunk = 5;
  const auto rechunked = search::run_search(smaller_chunks);
  require_same_finite_results(actual, rechunked,
                              "CUDA chunk-boundary invariance");
  require(rechunked.stats.evaluation_chunks == 7,
          "32 traces in chunks of five must require seven outer chunks");
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 2) {
      throw std::invalid_argument(
          "usage: rule30_cuda_extended_period_search_tests cpu|gpu");
    }
    const std::string mode(argv[1]);
    if (mode == "cpu") {
      run_cpu_tests();
      std::cout << "All extended period-search CPU tests passed\n";
    } else if (mode == "gpu") {
      run_gpu_tests();
      std::cout << "All extended period-search CUDA tests passed\n";
    } else {
      throw std::invalid_argument("test mode must be cpu or gpu");
    }
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "extended period-search test failure: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
