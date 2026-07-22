#include "rule30_cuda/batch_period.hpp"

#include <algorithm>
#include <array>
#include <cerrno>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <fcntl.h>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <system_error>
#include <utility>
#include <vector>

#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

namespace {

constexpr std::string_view kTenThousandFnv1a64 = "81cc5a51e61d2597";
constexpr std::string_view kEmptyFnv1a64 = "cbf29ce484222325";

void require(const bool condition, const std::string& message) {
  if (!condition) {
    throw std::runtime_error(message);
  }
}

class FileDescriptor {
 public:
  explicit FileDescriptor(const int descriptor) : descriptor_(descriptor) {}
  FileDescriptor(const FileDescriptor&) = delete;
  FileDescriptor& operator=(const FileDescriptor&) = delete;

  FileDescriptor(FileDescriptor&& other) noexcept
      : descriptor_(std::exchange(other.descriptor_, -1)) {}

  FileDescriptor& operator=(FileDescriptor&& other) noexcept {
    if (this != &other) {
      close();
      descriptor_ = std::exchange(other.descriptor_, -1);
    }
    return *this;
  }

  ~FileDescriptor() { close(); }

  [[nodiscard]] int get() const noexcept { return descriptor_; }

 private:
  void close() noexcept {
    if (descriptor_ >= 0) {
      static_cast<void>(::close(descriptor_));
      descriptor_ = -1;
    }
  }

  int descriptor_;
};

FileDescriptor make_temporary_file() {
  char path[] = "/tmp/rule30_cuda_generate_contract_XXXXXX";
  const int descriptor = ::mkstemp(path);
  if (descriptor < 0) {
    throw std::system_error(errno, std::generic_category(), "mkstemp failed");
  }
  if (::unlink(path) != 0) {
    const int error = errno;
    static_cast<void>(::close(descriptor));
    throw std::system_error(error, std::generic_category(), "unlink failed");
  }
  return FileDescriptor(descriptor);
}

FileDescriptor open_output_file(const char* const path) {
  const int descriptor = ::open(path, O_WRONLY);
  if (descriptor < 0) {
    throw std::system_error(errno, std::generic_category(),
                            std::string("open failed for ") + path);
  }
  return FileDescriptor(descriptor);
}

std::vector<std::uint8_t> read_all(const int descriptor) {
  if (::lseek(descriptor, 0, SEEK_SET) < 0) {
    throw std::system_error(errno, std::generic_category(), "lseek failed");
  }

  std::vector<std::uint8_t> output;
  std::array<std::uint8_t, 4096> buffer{};
  while (true) {
    const ssize_t count = ::read(descriptor, buffer.data(), buffer.size());
    if (count > 0) {
      output.insert(output.end(), buffer.begin(),
                    buffer.begin() + static_cast<std::size_t>(count));
      continue;
    }
    if (count == 0) {
      return output;
    }
    if (errno != EINTR) {
      throw std::system_error(errno, std::generic_category(), "read failed");
    }
  }
}

struct ProcessResult {
  int exit_code{};
  std::vector<std::uint8_t> standard_output;
  std::string standard_error;
};

ProcessResult run_cli(const std::string& executable,
                      std::vector<std::string> arguments,
                      const char* const redirected_stdout = nullptr) {
  std::vector<std::string> invocation;
  invocation.reserve(arguments.size() + 1U);
  invocation.push_back(executable);
  for (std::string& argument : arguments) {
    invocation.push_back(std::move(argument));
  }

  std::vector<char*> child_arguments;
  child_arguments.reserve(invocation.size() + 1U);
  for (std::string& argument : invocation) {
    child_arguments.push_back(argument.data());
  }
  child_arguments.push_back(nullptr);

  const bool capture_stdout = redirected_stdout == nullptr;
  FileDescriptor stdout_file = capture_stdout
                                   ? make_temporary_file()
                                   : open_output_file(redirected_stdout);
  FileDescriptor stderr_file = make_temporary_file();

  const pid_t child = ::fork();
  if (child < 0) {
    throw std::system_error(errno, std::generic_category(), "fork failed");
  }
  if (child == 0) {
    if (::dup2(stdout_file.get(), STDOUT_FILENO) < 0 ||
        ::dup2(stderr_file.get(), STDERR_FILENO) < 0) {
      constexpr char kMessage[] = "test harness dup2 failed\n";
      const ssize_t written = ::write(STDERR_FILENO, kMessage,
                                      sizeof(kMessage) - 1U);
      static_cast<void>(written);
      _exit(126);
    }
    ::execv(executable.c_str(), child_arguments.data());
    constexpr char kMessage[] = "test harness execv failed\n";
    const ssize_t written =
        ::write(STDERR_FILENO, kMessage, sizeof(kMessage) - 1U);
    static_cast<void>(written);
    _exit(127);
  }

  int status = 0;
  while (::waitpid(child, &status, 0) < 0) {
    if (errno != EINTR) {
      throw std::system_error(errno, std::generic_category(), "waitpid failed");
    }
  }

  ProcessResult result{};
  if (WIFEXITED(status)) {
    result.exit_code = WEXITSTATUS(status);
  } else if (WIFSIGNALED(status)) {
    result.exit_code = 128 + WTERMSIG(status);
  } else {
    throw std::runtime_error("child process ended in an unexpected state");
  }
  if (capture_stdout) {
    result.standard_output = read_all(stdout_file.get());
  }
  const auto error_bytes = read_all(stderr_file.get());
  result.standard_error.assign(error_bytes.begin(), error_bytes.end());
  return result;
}

void require_success(const ProcessResult& result,
                     const std::string& description) {
  require(result.exit_code == 0,
          description + " failed with exit " +
              std::to_string(result.exit_code) + ": " +
              result.standard_error);
  require(result.standard_error.empty(),
          description + " wrote unexpected stderr: " +
              result.standard_error);
}

void require_failure(const ProcessResult& result, const int exit_code,
                     const std::string_view expected_error,
                     const std::string& description) {
  require(result.exit_code == exit_code,
          description + " returned exit " +
              std::to_string(result.exit_code) + " instead of " +
              std::to_string(exit_code));
  require(result.standard_output.empty(),
          description + " wrote unexpected stdout");
  require(result.standard_error.find(expected_error) != std::string::npos,
          description + " stderr did not contain '" +
              std::string(expected_error) + "': " + result.standard_error);
}

std::vector<std::uint8_t> read_reference_vector(const std::string& path) {
  std::ifstream input(path, std::ios::binary);
  if (!input) {
    throw std::runtime_error("failed to open frozen vector: " + path);
  }
  const std::vector<char> bytes((std::istreambuf_iterator<char>(input)),
                                std::istreambuf_iterator<char>());
  if (input.bad()) {
    throw std::runtime_error("failed while reading frozen vector: " + path);
  }
  std::vector<std::uint8_t> output;
  output.reserve(bytes.size());
  for (const char byte : bytes) {
    output.push_back(static_cast<std::uint8_t>(byte));
  }
  return output;
}

std::string json_escape(const std::string_view input) {
  constexpr char kHexDigits[] = "0123456789abcdef";
  std::string output;
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

std::string expected_json(const rule30::cuda::DeviceInfo& device,
                          const std::size_t count,
                          const std::uint64_t ones,
                          const std::uint64_t zeros,
                          const std::string_view discrepancy,
                          const std::string_view hash) {
  std::ostringstream output;
  output << '{' << "\"count\":" << count << ',' << "\"ones\":" << ones
         << ',' << "\"zeros\":" << zeros << ',' << "\"discrepancy\":"
         << discrepancy << ",\"center_hash_fnv1a64\":\"" << hash << "\","
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

void run_cpu_contract(const std::string& executable) {
  const auto help = run_cli(executable, {"--help"});
  require_success(help, "help command");
  require(!help.standard_output.empty(), "help command wrote no usage text");

  const auto empty = run_cli(
      executable,
      {"generate", "--count", "0", "--format", "raw", "--device",
       "2147483647", "--threads", "1", "--memory-budget-mib", "1",
       "--max-output-mib", "1"});
  require_success(empty, "zero-count raw generation");
  require(empty.standard_output.empty(),
          "zero-count raw generation wrote bytes");

  struct InvalidCase {
    std::vector<std::string> arguments;
    std::string_view error;
  };
  const std::vector<InvalidCase> invalid_cases{
      {{}, "generate command is required"},
      {{"other"}, "unknown command"},
      {{"generate", "--format", "raw"}, "--count is required"},
      {{"generate", "--count", "0"}, "--format is required"},
      {{"generate", "--count"}, "--count requires a value"},
      {{"generate", "--count", "--format", "raw"},
       "--count requires a value"},
      {{"generate", "--count", "0", "--format"},
       "--format requires a value"},
      {{"generate", "--count", "0", "--format", "raw", "--device"},
       "--device requires a value"},
      {{"generate", "--count", "0", "--format", "raw", "--threads"},
       "--threads requires a value"},
      {{"generate", "--count", "0", "--format", "raw",
        "--memory-budget-mib"},
       "--memory-budget-mib requires a value"},
      {{"generate", "--count", "0", "--format", "raw",
        "--max-output-mib"},
       "--max-output-mib requires a value"},
      {{"generate", "--count", "-1", "--format", "raw"},
       "nonnegative decimal integer"},
      {{"generate", "--count", "1x", "--format", "raw"},
       "nonnegative decimal integer"},
      {{"generate", "--count", "18446744073709551616", "--format", "raw"},
       "--count is too large"},
      {{"generate", "--count", "0", "--format", "binary"},
       "--format must be raw or json"},
      {{"generate", "--count", "0", "--format", "raw", "--device", "-1"},
       "nonnegative decimal integer"},
      {{"generate", "--count", "0", "--format", "raw", "--device",
        "2147483648"},
       "--device is too large"},
      {{"generate", "--count", "0", "--format", "raw", "--threads", "0"},
       "--threads must be positive"},
      {{"generate", "--count", "0", "--format", "raw", "--threads",
        "2147483648"},
       "--threads is too large"},
      {{"generate", "--count", "0", "--format", "raw",
        "--memory-budget-mib", "0"},
       "--memory-budget-mib must be positive"},
      {{"generate", "--count", "0", "--format", "raw",
        "--max-output-mib", "0"},
       "--max-output-mib must be positive"},
      {{"generate", "--count", "0", "--format", "raw",
        "--memory-budget-mib", "18446744073709551615"},
       "--memory-budget-mib is too large"},
      {{"generate", "--count", "0", "--format", "raw",
        "--max-output-mib", "18446744073709551615"},
       "--max-output-mib is too large"},
      {{"generate", "--count", "0", "--format", "raw", "--unknown", "1"},
       "unknown option"},
      {{"generate", "--count", "0", "--format", "raw", "extra"},
       "unknown option"},
  };

  for (const InvalidCase& invalid : invalid_cases) {
    const auto result = run_cli(executable, invalid.arguments);
    require_failure(result, 2, invalid.error, "invalid argument contract");
  }

  const std::vector<std::pair<std::string, std::string>> duplicate_options{
      {"--count", "0"},
      {"--format", "raw"},
      {"--device", "0"},
      {"--threads", "1"},
      {"--memory-budget-mib", "1"},
      {"--max-output-mib", "1"},
  };
  for (const auto& [option, value] : duplicate_options) {
    std::vector<std::string> arguments{
        "generate",          "--count",          "0",
        "--format",         "raw",              "--device",
        "0",                 "--threads",        "1",
        "--memory-budget-mib", "1",              "--max-output-mib",
        "1",                 option,              value,
    };
    const auto result = run_cli(executable, std::move(arguments));
    require_failure(result, 2, option + " may only be specified once",
                    "duplicate option contract");
  }

  const auto arithmetic_overflow = run_cli(
      executable,
      {"generate", "--count",
       std::to_string(std::numeric_limits<std::size_t>::max()), "--format",
       "raw", "--max-output-mib", "1"});
  require_failure(arithmetic_overflow, 1, "final row bit count overflow",
                  "count arithmetic overflow");

  const auto output_budget = run_cli(
      executable,
      {"generate", "--count", "900000", "--format", "raw",
       "--max-output-mib", "1"});
  require_failure(output_budget, 1, "output exceeds max_output_bytes",
                  "output budget preflight");
}

int run_gpu_contract(const std::string& executable,
                     const std::string& vector_path) {
  int device_count = 0;
  try {
    device_count = rule30::cuda::device_count();
  } catch (const std::exception& error) {
    std::cerr << "SKIP: CUDA runtime unavailable: " << error.what() << '\n';
    return 77;
  }
  if (device_count == 0) {
    std::cerr << "SKIP: no CUDA device available\n";
    return 77;
  }

  rule30::cuda::DeviceInfo device{};
  try {
    device = rule30::cuda::probe_device(0);
  } catch (const std::exception& error) {
    std::cerr << "SKIP: CUDA device 0 unavailable: " << error.what() << '\n';
    return 77;
  }
  if (device.compute_major != 7 || device.compute_minor != 5) {
    std::cerr << "SKIP: contract target contains sm_75 SASS but device 0 is sm_"
              << device.compute_major << device.compute_minor << '\n';
    return 77;
  }

  const auto expected = read_reference_vector(vector_path);
  require(expected.size() == 10'000,
          "frozen vector does not contain exactly 10,000 bytes");
  require(std::all_of(expected.begin(), expected.end(),
                      [](const std::uint8_t bit) { return bit <= 1U; }),
          "frozen vector contains a non-binary byte");

  for (const std::size_t count : {1U, 63U, 64U, 65U, 127U, 128U, 129U}) {
    const auto actual = run_cli(
        executable,
        {"generate", "--count", std::to_string(count), "--format", "raw",
         "--device", "0", "--threads", "7", "--memory-budget-mib", "1",
         "--max-output-mib", "1"});
    require_success(actual, "raw boundary generation at N=" +
                                std::to_string(count));
    require(actual.standard_output.size() == count,
            "raw boundary output has the wrong byte count at N=" +
                std::to_string(count));
    require(std::equal(actual.standard_output.begin(),
                       actual.standard_output.end(), expected.begin()),
            "raw boundary output differs from the frozen vector at N=" +
                std::to_string(count));
  }

  const auto ten_thousand = run_cli(
      executable,
      {"generate", "--count", "10000", "--format", "raw", "--device", "0",
       "--threads", "96", "--memory-budget-mib", "1", "--max-output-mib",
       "1"});
  require_success(ten_thousand, "10,000-byte raw generation");
  require(ten_thousand.standard_output == expected,
          "10,000-byte raw output differs from the frozen vector");

  const auto empty_json = run_cli(
      executable,
      {"generate", "--count", "0", "--format", "json", "--device", "0",
       "--threads", "1", "--memory-budget-mib", "1", "--max-output-mib",
       "1"});
  require_success(empty_json, "zero-count JSON generation");
  const std::string empty_json_text(empty_json.standard_output.begin(),
                                    empty_json.standard_output.end());
  require(empty_json_text ==
              expected_json(device, 0, 0, 0, "0", kEmptyFnv1a64),
          "zero-count JSON summary mismatch: " + empty_json_text);

  const auto json = run_cli(
      executable,
      {"generate", "--count", "10000", "--format", "json", "--device", "0",
       "--threads", "96", "--memory-budget-mib", "1", "--max-output-mib",
       "1"});
  require_success(json, "10,000-bit JSON generation");
  const std::string json_text(json.standard_output.begin(),
                              json.standard_output.end());
  require(json_text == expected_json(device, 10'000, 5'032, 4'968, "64",
                                     kTenThousandFnv1a64),
          "JSON summary mismatch: " + json_text);
  require(json_text.find("center_bits") == std::string::npos,
          "JSON summary contains the full center-bit field");

  const auto memory_budget = run_cli(
      executable,
      {"generate", "--count", "700000", "--format", "raw", "--device", "0",
       "--memory-budget-mib", "1", "--max-output-mib", "1"});
  require_failure(memory_budget, 1, "device memory budget cannot hold",
                  "device memory budget preflight");

  const auto invalid_device = run_cli(
      executable,
      {"generate", "--count", "1", "--format", "raw", "--device",
       std::to_string(device_count)});
  require_failure(invalid_device, 1, "outside the available CUDA devices",
                  "unavailable device check");

  const auto excessive_threads = run_cli(
      executable,
      {"generate", "--count", "1", "--format", "raw", "--device", "0",
       "--threads", std::to_string(device.max_threads_per_block + 1)});
  require_failure(excessive_threads, 1, "threads_per_block exceeds",
                  "device thread-limit check");

  if (::access("/dev/full", W_OK) == 0) {
    for (const std::string& format : {std::string("raw"),
                                     std::string("json")}) {
      const auto write_error = run_cli(
          executable,
          {"generate", "--count", "1", "--format", format, "--device", "0",
           "--memory-budget-mib", "1", "--max-output-mib", "1"},
          "/dev/full");
      require(write_error.exit_code == 1,
              format + " write error returned the wrong exit code");
      require(write_error.standard_error.find("failed to write") !=
                      std::string::npos ||
                  write_error.standard_error.find("failed to flush") !=
                      std::string::npos,
              format + " write error was not reported: " +
                  write_error.standard_error);
    }
  }

  std::cout << "CUDA generation CLI GPU contract passed on " << device.name
            << '\n';
  return EXIT_SUCCESS;
}

}  // namespace

int main(const int argc, char** const argv) {
  try {
    if (argc != 4) {
      throw std::invalid_argument(
          "usage: rule30_cuda_generate_contract_tests cpu|gpu CLI VECTOR");
    }
    const std::string mode(argv[1]);
    const std::string executable(argv[2]);
    const std::string vector_path(argv[3]);

    if (mode == "cpu") {
      run_cpu_contract(executable);
      std::cout << "CUDA generation CLI CPU-only contract passed\n";
      return EXIT_SUCCESS;
    }
    if (mode == "gpu") {
      return run_gpu_contract(executable, vector_path);
    }
    throw std::invalid_argument("test mode must be cpu or gpu");
  } catch (const std::exception& error) {
    std::cerr << "CUDA generation CLI contract failure: " << error.what()
              << '\n';
    return EXIT_FAILURE;
  }
}
