#include "rule30_cuda/batch_period.hpp"
#include "rule30_cuda/direct_evolution.hpp"

#include <algorithm>
#include <charconv>
#include <csignal>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <system_error>

namespace {

constexpr std::size_t kBytesPerMebibyte = 1024ULL * 1024ULL;
constexpr std::size_t kOutputChunkBytes = 64ULL * 1024ULL;

enum class OutputFormat {
  raw,
  json,
};

struct Options {
  std::size_t count{};
  OutputFormat format{OutputFormat::raw};
  int device_index{0};
  int threads_per_block{256};
  std::size_t memory_budget_mib{256};
  std::size_t max_output_mib{64};
};

struct ParseResult {
  Options options{};
  bool show_help{};
};

struct SeenOptions {
  bool count{};
  bool format{};
  bool device{};
  bool threads{};
  bool memory_budget{};
  bool max_output{};
};

void print_usage(std::ostream& output, const std::string_view program) {
  output
      << "Usage:\n"
      << "  " << program
      << " generate --count N --format raw|json [--device INDEX]"
         " [--threads N]\n"
      << "      [--memory-budget-mib N] [--max-output-mib N]\n\n"
      << "Raw output is exactly N numeric bytes (0 or 1), ordered c_0 "
         "through c_(N-1).\n"
      << "JSON output is a finite-prefix summary and never includes the full "
         "bit prefix.\n"
      << "Defaults: --device 0, --threads 256, --memory-budget-mib 256, "
         "--max-output-mib 64.\n"
      << "The output budget caps the center bytes plus the packed final row "
         "returned by the CUDA API.\n";
}

void reject_duplicate(bool& seen, const std::string_view option) {
  if (seen) {
    throw std::invalid_argument(std::string(option) +
                                " may only be specified once");
  }
  seen = true;
}

std::string_view require_value(const int argc, char** const argv, int& index,
                               const std::string_view option) {
  if (index + 1 >= argc ||
      std::string_view(argv[index + 1]).starts_with("--")) {
    throw std::invalid_argument(std::string(option) + " requires a value");
  }
  ++index;
  return argv[index];
}

std::uint64_t parse_decimal(const std::string_view text,
                            const std::string_view option) {
  if (text.empty() ||
      !std::all_of(text.begin(), text.end(), [](const char character) {
        return character >= '0' && character <= '9';
      })) {
    throw std::invalid_argument(std::string(option) +
                                " requires a nonnegative decimal integer");
  }

  std::uint64_t value = 0;
  const auto [position, error] =
      std::from_chars(text.data(), text.data() + text.size(), value);
  if (error == std::errc::result_out_of_range) {
    throw std::out_of_range(std::string(option) + " is too large");
  }
  if (error != std::errc{} || position != text.data() + text.size()) {
    throw std::invalid_argument(std::string(option) +
                                " requires a nonnegative decimal integer");
  }
  return value;
}

std::size_t parse_size(const std::string_view text,
                       const std::string_view option) {
  static_assert(std::numeric_limits<std::size_t>::digits <= 64);
  const std::uint64_t value = parse_decimal(text, option);
  if (value > std::numeric_limits<std::size_t>::max()) {
    throw std::out_of_range(std::string(option) +
                            " is too large for this platform");
  }
  return static_cast<std::size_t>(value);
}

int parse_nonnegative_int(const std::string_view text,
                          const std::string_view option) {
  const std::uint64_t value = parse_decimal(text, option);
  if (value > static_cast<std::uint64_t>(std::numeric_limits<int>::max())) {
    throw std::out_of_range(std::string(option) + " is too large");
  }
  return static_cast<int>(value);
}

int parse_positive_int(const std::string_view text,
                       const std::string_view option) {
  const int value = parse_nonnegative_int(text, option);
  if (value == 0) {
    throw std::invalid_argument(std::string(option) + " must be positive");
  }
  return value;
}

OutputFormat parse_format(const std::string_view text) {
  if (text == "raw") {
    return OutputFormat::raw;
  }
  if (text == "json") {
    return OutputFormat::json;
  }
  throw std::invalid_argument("--format must be raw or json");
}

std::size_t mebibytes_to_bytes(const std::size_t value,
                               const std::string_view option) {
  if (value == 0) {
    throw std::invalid_argument(std::string(option) + " must be positive");
  }
  if (value > std::numeric_limits<std::size_t>::max() / kBytesPerMebibyte) {
    throw std::out_of_range(std::string(option) + " is too large");
  }
  return value * kBytesPerMebibyte;
}

ParseResult parse_arguments(const int argc, char** const argv) {
  if (argc < 2) {
    throw std::invalid_argument("the generate command is required");
  }

  const std::string_view command(argv[1]);
  if (command == "--help" || command == "-h") {
    return {{}, true};
  }
  if (command != "generate") {
    throw std::invalid_argument("unknown command; expected generate");
  }

  Options options{};
  SeenOptions seen{};
  for (int index = 2; index < argc; ++index) {
    const std::string_view option(argv[index]);
    if (option == "--help" || option == "-h") {
      return {{}, true};
    }
    if (option == "--count") {
      reject_duplicate(seen.count, option);
      options.count = parse_size(require_value(argc, argv, index, option), option);
    } else if (option == "--format") {
      reject_duplicate(seen.format, option);
      options.format = parse_format(require_value(argc, argv, index, option));
    } else if (option == "--device") {
      reject_duplicate(seen.device, option);
      options.device_index = parse_nonnegative_int(
          require_value(argc, argv, index, option), option);
    } else if (option == "--threads") {
      reject_duplicate(seen.threads, option);
      options.threads_per_block =
          parse_positive_int(require_value(argc, argv, index, option), option);
    } else if (option == "--memory-budget-mib") {
      reject_duplicate(seen.memory_budget, option);
      options.memory_budget_mib =
          parse_size(require_value(argc, argv, index, option), option);
    } else if (option == "--max-output-mib") {
      reject_duplicate(seen.max_output, option);
      options.max_output_mib =
          parse_size(require_value(argc, argv, index, option), option);
    } else {
      throw std::invalid_argument("unknown option: " + std::string(option));
    }
  }

  if (!seen.count) {
    throw std::invalid_argument("--count is required");
  }
  if (!seen.format) {
    throw std::invalid_argument("--format is required");
  }

  static_cast<void>(
      mebibytes_to_bytes(options.memory_budget_mib, "--memory-budget-mib"));
  static_cast<void>(
      mebibytes_to_bytes(options.max_output_mib, "--max-output-mib"));
  return {options, false};
}

std::string discrepancy_text(const std::uint64_t ones,
                             const std::uint64_t zeros) {
  if (ones >= zeros) {
    return std::to_string(ones - zeros);
  }
  return "-" + std::to_string(zeros - ones);
}

std::string json_escape(const std::string_view input) {
  constexpr char kHexDigits[] = "0123456789abcdef";
  std::string output;
  output.reserve(input.size());
  for (const unsigned char character : input) {
    switch (character) {
      case '"':
        output += "\\\"";
        break;
      case '\\':
        output += "\\\\";
        break;
      case '\b':
        output += "\\b";
        break;
      case '\f':
        output += "\\f";
        break;
      case '\n':
        output += "\\n";
        break;
      case '\r':
        output += "\\r";
        break;
      case '\t':
        output += "\\t";
        break;
      default:
        if (character < 0x20U) {
          output += "\\u00";
          output.push_back(kHexDigits[character >> 4U]);
          output.push_back(kHexDigits[character & 0x0fU]);
        } else {
          output.push_back(static_cast<char>(character));
        }
        break;
    }
  }
  return output;
}

void write_stdout(const char* const data, const std::size_t size,
                  const std::string_view format) {
  std::size_t offset = 0;
  while (offset < size) {
    const std::size_t chunk = std::min(kOutputChunkBytes, size - offset);
    std::cout.write(data + offset, static_cast<std::streamsize>(chunk));
    if (!std::cout) {
      throw std::runtime_error("failed to write " + std::string(format) +
                               " output");
    }
    offset += chunk;
  }
  std::cout.flush();
  if (!std::cout) {
    throw std::runtime_error("failed to flush " + std::string(format) +
                             " output");
  }
}

std::string make_json(
    const Options& options,
    const rule30::cuda::DirectEvolutionResult& result,
    const rule30::cuda::DeviceInfo& device) {
  std::ostringstream hash;
  hash << std::hex << std::setw(16) << std::setfill('0')
       << result.center_hash_fnv1a64;

  std::ostringstream output;
  output << '{' << "\"count\":" << options.count << ','
         << "\"ones\":" << result.center_ones << ','
         << "\"zeros\":" << result.center_zeros << ','
         << "\"discrepancy\":"
         << discrepancy_text(result.center_ones, result.center_zeros) << ','
         << "\"center_hash_fnv1a64\":\"" << hash.str() << "\","
         << "\"backend\":\"cuda-direct-evolution\","
         << "\"device\":\"" << json_escape(device.name) << "\","
         << "\"device_index\":" << device.device_index << ','
         << "\"compute_capability\":\"" << device.compute_major << '.'
         << device.compute_minor << "\","
         << "\"bit_order\":\"c_0_to_c_n_minus_1\","
         << "\"interpretation\":\"exact finite prefix only; no "
            "infinite-sequence conclusion\"}\n";
  return output.str();
}

void validate_result(const Options& options,
                     const rule30::cuda::DirectEvolutionResult& result) {
  if (result.center_bits.size() != options.count) {
    throw std::runtime_error("CUDA API returned an incorrect center-bit count");
  }
  if (result.center_ones + result.center_zeros != options.count) {
    throw std::runtime_error("CUDA API returned inconsistent center counts");
  }
}

void execute(const Options& options) {
  rule30::cuda::DirectEvolutionConfig config{};
  config.device_index = options.device_index;
  config.threads_per_block = options.threads_per_block;
  config.device_memory_budget_bytes =
      mebibytes_to_bytes(options.memory_budget_mib, "--memory-budget-mib");
  config.max_output_bytes =
      mebibytes_to_bytes(options.max_output_mib, "--max-output-mib");

  const auto result = rule30::cuda::evolve_single_history(options.count, config);
  validate_result(options, result);

  if (options.format == OutputFormat::raw) {
    write_stdout(reinterpret_cast<const char*>(result.center_bits.data()),
                 result.center_bits.size(), "raw");
    return;
  }

  const auto device = rule30::cuda::probe_device(options.device_index);
  const std::string json = make_json(options, result, device);
  write_stdout(json.data(), json.size(), "JSON");
}

}  // namespace

int main(const int argc, char** const argv) {
#ifdef SIGPIPE
  std::signal(SIGPIPE, SIG_IGN);
#endif
  std::ios::sync_with_stdio(false);

  ParseResult parsed{};
  try {
    parsed = parse_arguments(argc, argv);
  } catch (const std::exception& error) {
    std::cerr << "rule30_cuda_generate: " << error.what() << '\n';
    print_usage(std::cerr, argc > 0 ? argv[0] : "rule30_cuda_generate");
    return 2;
  }

  if (parsed.show_help) {
    try {
      std::ostringstream usage;
      print_usage(usage, argc > 0 ? argv[0] : "rule30_cuda_generate");
      const std::string text = usage.str();
      write_stdout(text.data(), text.size(), "help");
      return EXIT_SUCCESS;
    } catch (const std::exception& error) {
      std::cerr << "rule30_cuda_generate: " << error.what() << '\n';
      return EXIT_FAILURE;
    }
  }

  try {
    execute(parsed.options);
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "rule30_cuda_generate: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
