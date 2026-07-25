#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>

namespace {
constexpr std::array<int, 4> GAPS{2, 3, 4, 5};
constexpr int MIN_K = 5;
constexpr int MAX_K = 10;
constexpr int UNIFORM_MAX_K = 40;

std::uint64_t advance_fringe(std::uint64_t state) {
    const std::uint64_t row = 1 | (state << 1);
    const std::uint64_t odd = row ^ ((row >> 1) | (row >> 2));
    return (odd << 1) ^ (odd | (odd >> 1));
}

std::pair<int, std::uint64_t> first_return(std::uint64_t z) {
    std::uint64_t state = 4 * z;
    for (int gap = 1; gap <= 5; ++gap) {
        state = advance_fringe(state);
        if ((state & 3) == 0) return {gap, state >> 2};
    }
    throw std::runtime_error("five-block return bound failed");
}

std::uint64_t witness_base(int gap, int k) {
    if (gap == 2) {
        if (k == 5) return 100;
        if (k == 6) return 12;
        if (k >= 7) return 4;
    }
    if (gap == 3) {
        if (k == 5) return 25;
        if (k == 6) return 3;
        if (k >= 7) return 1;
    }
    if (gap == 4) {
        if (k == 5) return 6;
        if (k >= 6) return 0;
    }
    if (gap == 5) {
        constexpr std::array<std::uint64_t, 8> BASES{
            407, 16191, 23, 199, 415, 11, 7, 15
        };
        if (k >= 5 && k <= 12) return BASES.at(k - 5);
        if (k >= 13) return 7;
    }
    throw std::runtime_error("missing witness base");
}

int uniform_start(int gap) {
    if (gap == 2 || gap == 3) return 7;
    if (gap == 4) return 6;
    if (gap == 5) return 13;
    throw std::runtime_error("unknown gap");
}

std::uint64_t uniform_base(int gap) {
    if (gap == 2) return 4;
    if (gap == 3) return 1;
    if (gap == 4) return 0;
    if (gap == 5) return 7;
    throw std::runtime_error("unknown gap");
}

void verify_witness(int gap, int k, std::uint64_t base) {
    const int source_bits = k + 2 * gap;
    const std::uint64_t lifted = base + (std::uint64_t{1} << (source_bits - 1));
    const auto [left_gap, left] = first_return(base);
    const auto [right_gap, right] = first_return(lifted);
    const std::uint64_t mask = (std::uint64_t{1} << k) - 1;
    const std::uint64_t difference = (left ^ right) & mask;
    if (left_gap != gap || right_gap != gap) {
        throw std::runtime_error("witness left conditioned cylinder");
    }
    if (difference != (std::uint64_t{1} << (k - 1))) {
        throw std::runtime_error("witness failed to flip the top target bit");
    }
}
}  // namespace

int main() {
    std::uint64_t total_states = 0;
    for (int gap : GAPS) {
        for (int k = MIN_K; k <= MAX_K; ++k) {
            const int source_bits = k + 2 * gap;
            const std::uint64_t states = std::uint64_t{1} << source_bits;
            const std::uint64_t mask = (std::uint64_t{1} << k) - 1;
            std::uint64_t conditioned = 0;
            std::uint64_t checksum = 0;
            std::vector<bool> outputs(std::uint64_t{1} << k, false);
            for (std::uint64_t z = 0; z < states; ++z) {
                const auto [observed_gap, successor] = first_return(z);
                if (observed_gap != gap) continue;
                const std::uint64_t residue = successor & mask;
                ++conditioned;
                outputs[residue] = true;
                checksum = checksum * 0x100000001B3ULL + residue;
            }
            std::uint64_t distinct = 0;
            for (bool value : outputs) if (value) ++distinct;
            verify_witness(gap, k, witness_base(gap, k));
            total_states += states;
            std::cout << "level gap=" << gap
                      << " k=" << k
                      << " source_bits=" << source_bits
                      << " states=" << states
                      << " conditioned=" << conditioned
                      << " distinct=" << distinct
                      << " checksum=0x" << std::hex << std::setw(16)
                      << std::setfill('0') << checksum << std::dec
                      << std::setfill(' ') << '\n';
        }
    }
    for (int gap : GAPS) {
        for (int k = uniform_start(gap); k <= UNIFORM_MAX_K; ++k) {
            verify_witness(gap, k, uniform_base(gap));
        }
        std::cout << "uniform gap=" << gap
                  << " start_k=" << uniform_start(gap)
                  << " base=" << uniform_base(gap)
                  << " checked_through=" << UNIFORM_MAX_K << '\n';
    }
    std::cout << "total_states_exhausted=" << total_states << '\n';
    std::cout << "exact_conditioned_precision=k+2r_for_k_at_least_5\n";
    return 0;
}
