#include "rule30_cuda/batch_period.hpp"

#include <cstdlib>
#include <exception>
#include <iostream>
#include <string>

namespace {

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
    int device_index = 0;
    if (argc == 3 && std::string(argv[1]) == "--device") {
      device_index = std::stoi(argv[2]);
    } else if (argc != 1) {
      std::cerr << "usage: rule30_cuda_probe [--device INDEX]\n";
      return EXIT_FAILURE;
    }

    const auto info = rule30::cuda::probe_device(device_index);
    std::cout << "{\n"
              << "  \"device_index\": " << info.device_index << ",\n"
              << "  \"name\": \"" << json_escape(info.name) << "\",\n"
              << "  \"compute_capability\": \"" << info.compute_major << '.'
              << info.compute_minor << "\",\n"
              << "  \"compiled_sass_architecture\": \"sm_75\",\n"
              << "  \"multiprocessors\": " << info.multiprocessor_count << ",\n"
              << "  \"max_threads_per_block\": "
              << info.max_threads_per_block << ",\n"
              << "  \"max_grid_size_x\": " << info.max_grid_size_x << ",\n"
              << "  \"total_memory_bytes\": "
              << info.total_global_memory_bytes << ",\n"
              << "  \"free_memory_bytes\": " << info.free_global_memory_bytes
              << ",\n"
              << "  \"driver_version\": " << info.driver_version << ",\n"
              << "  \"runtime_version\": " << info.runtime_version << "\n"
              << "}\n";
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "CUDA probe failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
