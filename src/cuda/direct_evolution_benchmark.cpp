#include "rule30_cuda/batch_period.hpp"
#include "rule30_cuda/direct_evolution.hpp"

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstddef>
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

constexpr std::uint64_t kFnvOffsetBasis = 0xcbf29ce484222325ULL;
constexpr std::uint64_t kFnvPrime = 1099511628211ULL;

struct Options {
  std::size_t center_bit_count{32768};
  std::size_t memory_budget_mib{64};
  int repetitions{5};
  int threads_per_block{256};
  int device_index{0};
};

std::size_t parse_size(const char* value, const char* name) {
  const std::string text(value);
  if (text.empty() || text.front() == '-') {
    throw std::invalid_argument(std::string("invalid value for ") + name);
  }
  std::size_t consumed = 0;
  const unsigned long long parsed = std::stoull(text, &consumed);
  if (consumed != text.size() ||
      parsed > std::numeric_limits<std::size_t>::max()) {
    throw std::invalid_argument(std::string("invalid value for ") + name);
  }
  return static_cast<std::size_t>(parsed);
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

std::size_t mebibytes_to_bytes(std::size_t value) {
  constexpr std::size_t kBytesPerMebibyte = 1024ULL * 1024ULL;
  if (value > std::numeric_limits<std::size_t>::max() / kBytesPerMebibyte) {
    throw std::invalid_argument("--memory-budget-mib is too large");
  }
  return value * kBytesPerMebibyte;
}

Options parse_options(int argc, char** argv) {
  Options options;
  for (int index = 1; index < argc; index += 2) {
    if (index + 1 >= argc) {
      throw std::invalid_argument("every option requires a value");
    }
    const std::string option(argv[index]);
    if (option == "--center-bits") {
      options.center_bit_count =
          parse_size(argv[index + 1], "--center-bits");
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
  if (options.center_bit_count == 0 || options.memory_budget_mib == 0 ||
      options.repetitions <= 0 || options.threads_per_block <= 0 ||
      options.device_index < 0) {
    throw std::invalid_argument(
        "center bits, memory budget, repetitions, and threads must be positive");
  }
  return options;
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

// Independent host implementation. It shares the packed representation but
// does not call CUDA code or the CUDA implementation's internal helpers.
rule30::cuda::DirectEvolutionResult evolve_host_packed(
    std::size_t center_bit_count) {
  if (center_bit_count == 0 ||
      center_bit_count > std::numeric_limits<std::size_t>::max() / 2U + 1U) {
    throw std::invalid_argument("host benchmark requires a finite positive N");
  }
  const std::size_t row_bit_count = center_bit_count * 2U - 1U;
  const std::size_t row_word_count =
      row_bit_count / 64U +
      static_cast<std::size_t>(row_bit_count % 64U != 0U);
  const std::size_t center_position = center_bit_count - 1U;

  std::vector<std::uint64_t> current(row_word_count, 0U);
  std::vector<std::uint64_t> next(row_word_count, 0U);
  current[center_position / 64U] =
      std::uint64_t{1} << (center_position & 63U);

  rule30::cuda::DirectEvolutionResult result{};
  result.center_bits.assign(center_bit_count, 0U);
  result.center_bits[0] = 1U;

  for (std::size_t step = 1; step < center_bit_count; ++step) {
    const std::size_t source_radius = step - 1U;
    const std::size_t source_low_word =
        (center_position - source_radius) / 64U;
    const std::size_t source_high_word =
        (center_position + source_radius) / 64U;
    const std::size_t output_low_bit = center_position - step;
    const std::size_t output_high_bit = center_position + step;
    const std::size_t output_low_word = output_low_bit / 64U;
    const std::size_t output_high_word = output_high_bit / 64U;

    const auto load = [&](std::size_t word_index) {
      return word_index < source_low_word || word_index > source_high_word
                 ? std::uint64_t{0}
                 : current[word_index];
    };
    for (std::size_t word_index = output_low_word;
         word_index <= output_high_word; ++word_index) {
      const std::uint64_t middle = load(word_index);
      const std::uint64_t previous =
          word_index == 0U ? 0U : load(word_index - 1U);
      const std::uint64_t following =
          word_index + 1U == row_word_count ? 0U : load(word_index + 1U);
      const std::uint64_t left = (middle << 1U) | (previous >> 63U);
      const std::uint64_t right = (middle >> 1U) | (following << 63U);
      std::uint64_t output = left ^ (middle | right);

      if (word_index == output_low_word) {
        output &= std::numeric_limits<std::uint64_t>::max()
                  << (output_low_bit & 63U);
      }
      if (word_index == output_high_word) {
        const unsigned int high_offset =
            static_cast<unsigned int>(output_high_bit & 63U);
        if (high_offset != 63U) {
          output &= (std::uint64_t{1} << (high_offset + 1U)) - 1U;
        }
      }
      next[word_index] = output;
    }
    result.center_bits[step] = static_cast<std::uint8_t>(
        (next[center_position / 64U] >> (center_position & 63U)) & 1U);
    std::swap(current, next);
  }

  result.final_row_words = std::move(current);
  result.center_ones = static_cast<std::uint64_t>(
      std::count(result.center_bits.begin(), result.center_bits.end(), 1U));
  result.center_zeros =
      static_cast<std::uint64_t>(center_bit_count) - result.center_ones;
  result.center_hash_fnv1a64 = hash_bytes(result.center_bits);
  result.final_row_hash_fnv1a64 = hash_words(result.final_row_words);
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
  if (values.empty()) {
    throw std::invalid_argument("cannot summarize an empty timing sample");
  }
  std::sort(values.begin(), values.end());
  const std::size_t middle = values.size() / 2U;
  const double median =
      values.size() % 2U == 0U
          ? (values[middle - 1U] + values[middle]) / 2.0
          : values[middle];
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

std::string json_escape(const std::string& input) {
  std::string output;
  for (const char character : input) {
    if (character == '\\' || character == '"') {
      output.push_back('\\');
    }
    output.push_back(character);
  }
  return output;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    const auto device = rule30::cuda::probe_device(options.device_index);

    const auto host_warmup = evolve_host_packed(options.center_bit_count);
    rule30::cuda::DirectEvolutionConfig config{};
    config.device_index = options.device_index;
    config.threads_per_block = options.threads_per_block;
    config.device_memory_budget_bytes =
        mebibytes_to_bytes(options.memory_budget_mib);
    const auto gpu_warmup =
        rule30::cuda::evolve_single_history(options.center_bit_count, config);
    if (gpu_warmup != host_warmup) {
      throw std::runtime_error(
          "GPU warm-up result disagrees with the independent host oracle");
    }

    std::vector<double> host_times;
    std::vector<double> host_to_device_times;
    std::vector<double> kernel_times;
    std::vector<double> device_to_host_times;
    std::vector<double> transfer_times;
    std::vector<double> end_to_end_times;
    host_times.reserve(static_cast<std::size_t>(options.repetitions));
    host_to_device_times.reserve(static_cast<std::size_t>(options.repetitions));
    kernel_times.reserve(static_cast<std::size_t>(options.repetitions));
    device_to_host_times.reserve(static_cast<std::size_t>(options.repetitions));
    transfer_times.reserve(static_cast<std::size_t>(options.repetitions));
    end_to_end_times.reserve(static_cast<std::size_t>(options.repetitions));

    for (int repetition = 0; repetition < options.repetitions; ++repetition) {
      const auto start = Clock::now();
      const auto measured = evolve_host_packed(options.center_bit_count);
      host_times.push_back(
          std::chrono::duration<double, std::milli>(Clock::now() - start)
              .count());
      if (measured != host_warmup) {
        throw std::runtime_error("host oracle was nondeterministic");
      }
    }

    rule30::cuda::DirectEvolutionStats final_stats{};
    for (int repetition = 0; repetition < options.repetitions; ++repetition) {
      const auto measured = rule30::cuda::evolve_single_history(
          options.center_bit_count, config, &final_stats);
      if (measured != host_warmup) {
        throw std::runtime_error(
            "measured GPU result disagrees with the independent host oracle");
      }
      host_to_device_times.push_back(
          final_stats.host_to_device_milliseconds);
      kernel_times.push_back(final_stats.kernel_milliseconds);
      device_to_host_times.push_back(
          final_stats.device_to_host_milliseconds);
      transfer_times.push_back(final_stats.host_to_device_milliseconds +
                               final_stats.device_to_host_milliseconds);
      end_to_end_times.push_back(final_stats.end_to_end_milliseconds);
    }

    const TimingSummary host_timing = summarize_timings(host_times);
    const TimingSummary host_to_device_timing =
        summarize_timings(host_to_device_times);
    const TimingSummary kernel_timing = summarize_timings(kernel_times);
    const TimingSummary device_to_host_timing =
        summarize_timings(device_to_host_times);
    const TimingSummary transfer_timing = summarize_timings(transfer_times);
    const TimingSummary end_to_end_timing =
        summarize_timings(end_to_end_times);
    const double cpu_to_cuda_ratio =
        host_timing.median / end_to_end_timing.median;

    std::cout << std::fixed << std::setprecision(6)
              << "{\n"
              << "  \"workload\": \"single-history-direct-row-evolution\",\n"
              << "  \"interpretation\": \"finite benchmark; no mathematical "
                 "lower-bound claim\",\n"
              << "  \"device\": \"" << json_escape(device.name) << "\",\n"
              << "  \"compute_capability\": \"" << device.compute_major << '.'
              << device.compute_minor << "\",\n"
              << "  \"sass_architecture\": \"sm_75\",\n"
              << "  \"center_bit_count\": " << options.center_bit_count
              << ",\n"
              << "  \"final_row_bit_count\": "
              << final_stats.final_row_bit_count << ",\n"
              << "  \"final_row_word_count\": "
              << final_stats.final_row_word_count << ",\n"
              << "  \"result_bytes\": "
              << host_warmup.center_bits.size() +
                     host_warmup.final_row_words.size() * sizeof(std::uint64_t)
              << ",\n"
              << "  \"center_ones\": " << host_warmup.center_ones << ",\n"
              << "  \"center_zeros\": " << host_warmup.center_zeros << ",\n"
              << "  \"center_hash_fnv1a64\": \"" << std::hex
              << std::setw(16) << std::setfill('0')
              << host_warmup.center_hash_fnv1a64 << "\",\n"
              << "  \"final_row_hash_fnv1a64\": \"" << std::setw(16)
              << host_warmup.final_row_hash_fnv1a64 << std::dec
              << std::setfill(' ') << "\",\n"
              << "  \"cpu_gpu_exact_match\": true,\n"
              << "  \"sequential_kernel_launches_per_run\": "
              << final_stats.kernel_launches << ",\n"
              << "  \"packed_word_updates_per_run\": "
              << final_stats.row_word_updates << ",\n"
              << "  \"peak_device_bytes\": "
              << final_stats.peak_device_bytes << ",\n"
              << "  \"cpu_warmup_runs\": 1,\n"
              << "  \"gpu_warmup_runs\": 1,\n"
              << "  \"measured_repetitions\": " << options.repetitions
              << ",\n"
              << "  \"median_cpu_to_cuda_end_to_end_ratio\": "
              << cpu_to_cuda_ratio << ",\n"
              << "  \"cuda_end_to_end_median_is_lower\": "
              << (end_to_end_timing.median < host_timing.median ? "true" : "false")
              << ",\n";
    print_timing_summary("cpu_packed_milliseconds", host_timing, true);
    print_timing_summary("host_to_device_milliseconds",
                         host_to_device_timing, true);
    print_timing_summary("kernel_sequence_milliseconds", kernel_timing, true);
    print_timing_summary("device_to_host_milliseconds",
                         device_to_host_timing, true);
    print_timing_summary("total_transfer_milliseconds", transfer_timing, true);
    print_timing_summary("cuda_end_to_end_milliseconds", end_to_end_timing,
                         false);
    std::cout << "}\n";
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "CUDA direct-evolution benchmark failed: " << error.what()
              << '\n';
    return EXIT_FAILURE;
  }
}
