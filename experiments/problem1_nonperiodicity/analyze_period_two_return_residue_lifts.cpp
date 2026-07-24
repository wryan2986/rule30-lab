#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <tuple>
#include <vector>

namespace {
constexpr int OUTCOME_BITS = 6;
constexpr int DEPENDENCY_BITS = 16;
constexpr std::array<unsigned, 3> BAD{28, 44, 60};
constexpr std::array<unsigned, 8> OBSERVED{0, 3, 11, 24, 35, 43, 56, 63};

uint64_t advance_fringe(uint64_t state) {
    const uint64_t row = 1 | (state << 1);
    const uint64_t odd = row ^ ((row >> 1) | (row >> 2));
    return (odd << 1) ^ (odd | (odd >> 1));
}

std::pair<int, unsigned> return_outcome(uint64_t z) {
    uint64_t state = 4 * z;
    for (int gap = 1; gap <= 5; ++gap) {
        state = advance_fringe(state);
        if ((state & 3) == 0) return {gap, static_cast<unsigned>((state >> 2) & 63)};
    }
    throw std::runtime_error("five-block return bound failed");
}

bool is_bad(unsigned value) {
    for (unsigned bad : BAD) if (value == bad) return true;
    return false;
}
}

int main() {
    using Outcome = std::pair<int, unsigned>;
    std::vector<Outcome> outcomes(1u << DEPENDENCY_BITS);
    std::map<int, uint64_t> gap_counts;
    std::array<std::map<Outcome, uint64_t>, 64> relation;
    for (unsigned z = 0; z < outcomes.size(); ++z) {
        outcomes[z] = return_outcome(z);
        ++gap_counts[outcomes[z].first];
        ++relation[z & 63][outcomes[z]];
    }

    std::cout << "dependency_bits=" << DEPENDENCY_BITS << '\n';
    std::cout << "outcome_bits=" << OUTCOME_BITS << '\n';
    std::cout << "states_checked=" << outcomes.size() << '\n';
    std::cout << "gap_counts=";
    bool first = true;
    for (const auto& [gap, count] : gap_counts) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << gap << ':' << count;
    }
    std::cout << '\n';

    for (int bits = OUTCOME_BITS; bits < DEPENDENCY_BITS; ++bits) {
        const unsigned mask = (1u << bits) - 1;
        std::map<unsigned, std::pair<unsigned, Outcome>> seen;
        bool found = false;
        for (unsigned z = 0; z < outcomes.size(); ++z) {
            const unsigned residue = z & mask;
            auto it = seen.find(residue);
            if (it == seen.end()) {
                seen.emplace(residue, std::make_pair(z, outcomes[z]));
            } else if (it->second.second != outcomes[z]) {
                std::cout << "precision_witness bits=" << bits
                          << " residue=" << residue
                          << " left_z=" << it->second.first
                          << " left=" << it->second.second.first << ':' << it->second.second.second
                          << " right_z=" << z
                          << " right=" << outcomes[z].first << ':' << outcomes[z].second << '\n';
                found = true;
                break;
            }
        }
        if (!found) throw std::runtime_error("missing insufficiency witness");
    }
    std::cout << "precision_16_deterministic=true\n";

    for (unsigned residue : OBSERVED) {
        std::cout << "observed_row residue=" << residue << " outcomes=";
        first = true;
        for (const auto& [outcome, count] : relation[residue]) {
            if (!first) std::cout << ',';
            first = false;
            std::cout << outcome.first << ':' << outcome.second << ':' << count;
        }
        std::cout << '\n';
    }

    std::set<unsigned> seen{0};
    std::set<unsigned> frontier{0};
    int layer = 0;
    std::cout << "closure_layer_0=0\n";
    while (!frontier.empty()) {
        std::set<unsigned> next;
        for (unsigned residue : frontier) {
            for (const auto& [outcome, count] : relation[residue]) {
                (void)count;
                if (!seen.count(outcome.second)) next.insert(outcome.second);
            }
        }
        if (next.empty()) break;
        ++layer;
        std::cout << "closure_layer_" << layer << '=';
        first = true;
        for (unsigned value : next) {
            if (!first) std::cout << ',';
            first = false;
            std::cout << value;
        }
        std::cout << '\n';
        seen.insert(next.begin(), next.end());
        frontier = std::move(next);
    }
    std::cout << "closure_size=" << seen.size() << '\n';
    std::cout << "bad_reached=";
    first = true;
    for (unsigned value : seen) if (is_bad(value)) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << value;
    }
    std::cout << '\n';
    return 0;
}
