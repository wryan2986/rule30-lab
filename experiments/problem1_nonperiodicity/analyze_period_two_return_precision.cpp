#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <utility>

namespace {
constexpr int MIN_K = 4;
constexpr int MAX_EXHAUSTIVE_K = 10;
constexpr std::array<std::uint64_t, 9> BASES{
    203, 407, 16191, 23, 199, 415, 11, 7, 15
};

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

std::pair<int, std::uint64_t> outcome(std::uint64_t z, int k) {
    auto [gap, successor] = first_return(z);
    return {gap, successor & ((std::uint64_t{1} << k) - 1)};
}

std::uint64_t base_for_k(int k) {
    if (k >= 4 && k <= 12) return BASES.at(k - 4);
    if (k >= 13) return 7;
    throw std::runtime_error("unsupported k");
}

void verify_witness(int k) {
    const std::uint64_t base = base_for_k(k);
    const std::uint64_t lifted = base + (std::uint64_t{1} << (k + 9));
    const auto left = outcome(base, k);
    const auto right = outcome(lifted, k);
    if (left.first != 5 || right.first != 5) {
        throw std::runtime_error("witness left the gap-five cylinder");
    }
    if ((left.second ^ right.second) != (std::uint64_t{1} << (k - 1))) {
        throw std::runtime_error("witness did not flip the top target bit");
    }
    std::cout << "witness k=" << k
              << " base=" << base
              << " left=" << left.first << ':' << left.second
              << " right=" << right.first << ':' << right.second
              << " xor=" << (left.second ^ right.second) << '\n';
}
}  // namespace

int main() {
    std::uint64_t total_states = 0;
    for (int k = MIN_K; k <= MAX_EXHAUSTIVE_K; ++k) {
        const int source_bits = k + 10;
        const std::uint64_t states = std::uint64_t{1} << source_bits;
        std::map<int, std::uint64_t> gap_counts;
        std::uint64_t checksum = 0;
        for (std::uint64_t z = 0; z < states; ++z) {
            const auto [gap, successor] = outcome(z, k);
            ++gap_counts[gap];
            checksum = checksum * 0x100000001B3ULL
                + (static_cast<std::uint64_t>(gap) << k) + successor;
        }
        total_states += states;
        std::cout << "level k=" << k
                  << " source_bits=" << source_bits
                  << " states=" << states
                  << " checksum=" << std::hex << checksum << std::dec
                  << " gaps=";
        bool first = true;
        for (const auto& [gap, count] : gap_counts) {
            if (!first) std::cout << ',';
            first = false;
            std::cout << gap << ':' << count;
        }
        std::cout << '\n';
    }
    for (int k = 4; k <= 12; ++k) verify_witness(k);
    for (int k = 13; k <= 40; ++k) verify_witness(k);
    std::cout << "total_states_exhausted=" << total_states << '\n';
    std::cout << "exact_worst_case_precision=k+10\n";
    std::cout << "uniform_family_checked=13..40\n";
    return 0;
}
