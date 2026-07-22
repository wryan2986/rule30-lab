#include "rule30_cuda/batch_period.hpp"

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <exception>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;

struct Options {
  std::size_t bit_count{262147};
  std::size_t candidate_count{4099};
  std::size_t window{8191};
  std::size_t memory_budget_mib{64};
  int repetitions{3};
  int threads_per_block{256};
  int device_index{0};
};

std::size_t parse_size(const char* value, const char* name) {
  const std::string text(value);
  std::size_t consumed = 0;
  const unsigned long long parsed = std::stoull(text, &consumed);
  if (consumed != text.size() || parsed > std::numeric_limits<std::size_t>::max()) {
    throw std::invalid_argument(std::string("invalid value for ") + name);
  }
  return static_cast<std::size_t>(parsed);
}

std::size_t mebibytes_to_bytes(std::size_t value) {
  constexpr std::size_t kBytesPerMebibyte = 1024ULL * 1024ULL;
  if (value > std::numeric_limits<std::size_t>::max() / kBytesPerMebibyte) {
    throw std::invalid_argument("--memory-budget-mib is too large");
  }
  return value * kBytesPerMebibyte;
}

int parse_int(const char* value, const char* name) {
  const std::string text(value);
  std::size_t consumed = 0;
  const long parsed = std::stol(text, &consumed);
  if (consumed != text.size() || parsed < std::numeric_limits<int>::min() ||
      parsed > std::numeric_limits<int>::max()) {
    throw std::invalid_argument(std::string("invalid value for ") + name);
  }
  return static_cast<int>(parsed);
}

Options parse_options(int argc, char** argv) {
  Options options;
  for (int index = 1; index < argc; index += 2) {
    if (index + 1 >= argc) {
      throw std::invalid_argument("every option requires a value");
    }
    const std::string option(argv[index]);
    if (option == "--bits") {
      options.bit_count = parse_size(argv[index + 1], "--bits");
    } else if (option == "--candidates") {
      options.candidate_count = parse_size(argv[index + 1], "--candidates");
    } else if (option == "--window") {
      options.window = parse_size(argv[index + 1], "--window");
    } else if (option == "--memory-budget-mib") {
      options.memory_budget_mib =
          parse_size(argv[index + 1], "--memory-budget-mib");
    } else if (option == "--repetitions") {
      options.repetitions = parse_int(argv[index + 1], "--repetitions");
    } else if (option == "--threads") {
      options.threads_per_block = parse_int(argv[index + 1], "--threads");
    } else if (option == "--device") {
      options.device_index = parse_int(argv[index + 1], "--device");
    } else {
      throw std::invalid_argument("unknown option: " + option);
    }
  }
  if (options.bit_count < 256 || options.candidate_count == 0 ||
      options.window == 0 || options.memory_budget_mib == 0 ||
      options.repetitions <= 0 || options.threads_per_block <= 0) {
    throw std::invalid_argument("all sizes, repetitions, and threads must be positive");
  }
  return options;
}

std::uint64_t next_random(std::uint64_t& state) {
  state ^= state << 13;
  state ^= state >> 7;
  state ^= state << 17;
  return state;
}

rule30::cuda::PeriodResult evaluate_cpu(
    const std::vector<std::uint8_t>& bits,
    const rule30::cuda::PeriodCandidate& candidate) {
  rule30::cuda::PeriodResult result{};
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

struct TimingSummary {
  double minimum{};
  double median{};
  double maximum{};
  double mean{};
  double standard_deviation{};
};

TimingSummary summarize_timings(std::vector<double> values) {
  std::sort(values.begin(), values.end());
  const std::size_t middle = values.size() / 2;
  const double median = (values.size() & 1U) != 0U
                            ? values[middle]
                            : (values[middle - 1] + values[middle]) / 2.0;
  const double mean =
      std::accumulate(values.begin(), values.end(), 0.0) / values.size();
  const double squared_deviation =
      std::accumulate(values.begin(), values.end(), 0.0,
                      [mean](double sum, double value) {
                        const double difference = value - mean;
                        return sum + difference * difference;
                      });
  return {values.front(), median, values.back(), mean,
          std::sqrt(squared_deviation / values.size())};
}

void print_timing_summary(const char* name, const TimingSummary& summary,
                          bool trailing_comma) {
  std::cout << "  \"" << name << "\": {"
            << "\"minimum\": " << summary.minimum << ", "
            << "\"median\": " << summary.median << ", "
            << "\"maximum\": " << summary.maximum << ", "
            << "\"mean\": " << summary.mean << ", "
            << "\"standard_deviation\": " << summary.standard_deviation
            << '}' << (trailing_comma ? ",\n" : "\n");
}

std::uint64_t result_hash(const std::vector<rule30::cuda::PeriodResult>& results) {
  std::uint64_t hash = 0xcbf29ce484222325ULL;
  const auto absorb = [&hash](std::uint64_t value) {
    for (int byte = 0; byte < 8; ++byte) {
      hash ^= (value >> (byte * 8)) & 0xffU;
      hash *= 1099511628211ULL;
    }
  };
  for (const auto& result : results) {
    absorb(result.first_mismatch);
    absorb(result.comparisons_checked);
    absorb(result.matches);
  }
  return hash;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    constexpr std::size_t kBasePeriod = 31;

    std::uint64_t random_state = 0x4d595df4d0f33173ULL;
    std::vector<std::uint8_t> pattern(kBasePeriod);
    for (auto& bit : pattern) {
      bit = static_cast<std::uint8_t>(next_random(random_state) & 1U);
    }
    std::vector<std::uint8_t> bits(options.bit_count);
    for (std::size_t index = 0; index < bits.size(); ++index) {
      bits[index] = pattern[index % pattern.size()];
    }

    std::vector<rule30::cuda::PeriodCandidate> candidates;
    candidates.reserve(options.candidate_count);
    for (std::size_t index = 0; index < options.candidate_count; ++index) {
      const std::size_t period =
          (index & 1U) == 0U ? kBasePeriod * (1U + index % 3U) : 30U;
      if (period >= bits.size()) {
        throw std::invalid_argument("--bits is too small for generated periods");
      }
      const std::size_t available = bits.size() - period;
      const std::size_t requested_window = std::min(options.window, available);
      const std::size_t maximum_offset = available - requested_window;
      const std::size_t offset = maximum_offset == 0
                                     ? 0
                                     : next_random(random_state) %
                                           (maximum_offset + 1);
      const std::size_t start = period + offset;
      candidates.push_back({start, start + requested_window, period});
    }

    const auto evaluate_cpu_batch = [&bits, &candidates] {
      std::vector<rule30::cuda::PeriodResult> output;
      output.reserve(candidates.size());
      for (const auto& candidate : candidates) {
        output.push_back(evaluate_cpu(bits, candidate));
      }
      return output;
    };
    const auto cpu_results = evaluate_cpu_batch();
    std::vector<double> cpu_times;
    cpu_times.reserve(static_cast<std::size_t>(options.repetitions));
    for (int repetition = 0; repetition < options.repetitions; ++repetition) {
      const auto cpu_start = Clock::now();
      const auto measured = evaluate_cpu_batch();
      cpu_times.push_back(std::chrono::duration<double, std::milli>(
                              Clock::now() - cpu_start)
                              .count());
      if (measured != cpu_results) {
        throw std::runtime_error("CPU oracle was nondeterministic");
      }
    }

    rule30::cuda::BatchConfig config{};
    config.device_index = options.device_index;
    config.threads_per_block = options.threads_per_block;
    config.device_memory_budget_bytes =
        mebibytes_to_bytes(options.memory_budget_mib);

    rule30::cuda::BatchStats warmup_stats{};
    const auto warmup = rule30::cuda::evaluate_period_candidates(
        bits, candidates, config, &warmup_stats);
    if (warmup != cpu_results) {
      throw std::runtime_error("warm-up GPU results disagree with the CPU oracle");
    }

    std::vector<double> kernel_times;
    std::vector<double> end_to_end_times;
    std::vector<double> host_to_device_times;
    std::vector<double> device_to_host_times;
    std::vector<rule30::cuda::PeriodResult> gpu_results;
    rule30::cuda::BatchStats final_stats{};
    for (int repetition = 0; repetition < options.repetitions; ++repetition) {
      gpu_results = rule30::cuda::evaluate_period_candidates(
          bits, candidates, config, &final_stats);
      if (gpu_results != cpu_results) {
        throw std::runtime_error("GPU results disagree with the CPU oracle");
      }
      kernel_times.push_back(final_stats.kernel_milliseconds);
      end_to_end_times.push_back(final_stats.end_to_end_milliseconds);
      host_to_device_times.push_back(final_stats.host_to_device_milliseconds);
      device_to_host_times.push_back(final_stats.device_to_host_milliseconds);
    }

    const std::size_t matches = static_cast<std::size_t>(std::count_if(
        gpu_results.begin(), gpu_results.end(),
        [](const auto& result) { return result.matches != 0; }));
    const auto [minimum_window, maximum_window] = std::minmax_element(
        candidates.begin(), candidates.end(), [](const auto& left, const auto& right) {
          return left.end - left.start < right.end - right.start;
        });
    const TimingSummary cpu_timing = summarize_timings(cpu_times);
    const TimingSummary host_to_device_timing =
        summarize_timings(host_to_device_times);
    const TimingSummary kernel_timing = summarize_timings(kernel_times);
    const TimingSummary device_to_host_timing =
        summarize_timings(device_to_host_times);
    const TimingSummary end_to_end_timing =
        summarize_timings(end_to_end_times);
    const auto device = rule30::cuda::probe_device(options.device_index);

    std::cout << std::fixed << std::setprecision(6)
              << "{\n"
              << "  \"workload\": \"batch-period-equality\",\n"
              << "  \"device\": \"" << device.name << "\",\n"
              << "  \"compute_capability\": \"" << device.compute_major << '.'
              << device.compute_minor << "\",\n"
              << "  \"sass_architecture\": \"sm_75\",\n"
              << "  \"bit_count\": " << bits.size() << ",\n"
              << "  \"candidate_count\": " << candidates.size() << ",\n"
              << "  \"requested_window\": " << options.window << ",\n"
              << "  \"minimum_candidate_window\": "
              << minimum_window->end - minimum_window->start << ",\n"
              << "  \"maximum_candidate_window\": "
              << maximum_window->end - maximum_window->start << ",\n"
              << "  \"result_bytes\": "
              << gpu_results.size() * sizeof(rule30::cuda::PeriodResult) << ",\n"
              << "  \"matches\": " << matches << ",\n"
              << "  \"result_hash_fnv1a64\": \"" << std::hex << std::setw(16)
              << std::setfill('0') << result_hash(gpu_results) << std::dec
              << std::setfill(' ') << "\",\n"
              << "  \"cpu_warmup_runs\": 1,\n"
              << "  \"gpu_warmup_runs\": 1,\n"
              << "  \"measured_repetitions\": " << options.repetitions << ",\n"
              << "  \"chunks_per_run\": " << final_stats.chunks << ",\n"
              << "  \"peak_device_bytes\": " << final_stats.peak_device_bytes
              << ",\n";
    print_timing_summary("cpu_oracle_milliseconds", cpu_timing, true);
    print_timing_summary("host_to_device_milliseconds", host_to_device_timing,
                         true);
    print_timing_summary("kernel_milliseconds", kernel_timing, true);
    print_timing_summary("device_to_host_milliseconds", device_to_host_timing,
                         true);
    print_timing_summary("end_to_end_milliseconds", end_to_end_timing, false);
    std::cout << "}\n";
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "CUDA period benchmark failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
