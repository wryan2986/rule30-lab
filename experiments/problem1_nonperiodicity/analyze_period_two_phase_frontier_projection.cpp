#include <algorithm>
#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {
constexpr int MAXIMUM_COMPLEXITY = 25;
constexpr std::uint64_t KNOWN_COUNTEREXAMPLE = 0x1bcd3a7b3fdfbULL;
constexpr char KNOWN_WORD[] = "uuuttttutuptttututututuu";

std::uint64_t forward_generator(char name, std::uint64_t state) {
    const std::uint64_t stepped = state ^ ((state << 1) | (state << 2));
    if (name == 't') return stepped;
    if (name == 'u') return stepped ^ 1;
    if (name == 'p') return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    throw std::invalid_argument("unknown generator");
}

std::uint64_t projected_child_formula(std::uint64_t parent) {
    const std::uint64_t quotient = parent >> 2;
    switch (parent & 3) {
        case 0: return forward_generator('t', quotient);
        case 1: return forward_generator('u', quotient);
        case 2:
        case 3: return forward_generator('p', quotient);
    }
    throw std::runtime_error("unreachable residue");
}

int bit_length(std::uint64_t value) {
    return value == 0 ? 0 : 64 - __builtin_clzll(value);
}

std::vector<std::uint64_t> next_level(const std::vector<std::uint64_t>& states) {
    std::vector<std::uint64_t> next;
    next.reserve(states.size() * 3);
    for (std::uint64_t state : states) {
        const std::uint64_t stepped = forward_generator('t', state);
        next.push_back(stepped);
        next.push_back(stepped ^ 1);
        if ((state & 1) == 0) next.push_back(stepped ^ 3);
    }
    std::sort(next.begin(), next.end());
    next.erase(std::unique(next.begin(), next.end()), next.end());
    return next;
}

bool contains(const std::vector<std::uint64_t>& states, std::uint64_t value) {
    return std::binary_search(states.begin(), states.end(), value);
}

struct LevelSummary {
    std::uint64_t outputs = 0;
    std::uint64_t projected = 0;
    std::uint64_t uncovered = 0;
    std::array<std::uint64_t, 5> fibers{};
};

LevelSummary projection_summary(
    const std::vector<std::uint64_t>& previous,
    const std::vector<std::uint64_t>& current
) {
    LevelSummary summary;
    summary.outputs = current.size();
    std::size_t previous_index = 0;
    std::size_t current_index = 0;
    while (current_index < current.size()) {
        const std::uint64_t parent = current[current_index] >> 2;
        std::size_t end = current_index + 1;
        while (end < current.size() && (current[end] >> 2) == parent) ++end;
        const std::size_t fiber = end - current_index;
        if (fiber < 2 || fiber > 4) {
            throw std::runtime_error("projection fiber outside 2..4");
        }
        while (previous_index < previous.size() && previous[previous_index] < parent) {
            ++previous_index;
        }
        if (previous_index == previous.size() || previous[previous_index] != parent) {
            throw std::runtime_error("projection left preceding frontier");
        }
        ++summary.projected;
        ++summary.fibers[fiber];
        current_index = end;
    }
    summary.uncovered = previous.size() - summary.projected;
    return summary;
}

std::uint64_t apply_word(std::uint64_t state, const std::string& word) {
    for (char name : word) state = forward_generator(name, state);
    return state;
}

void verify_nonconverse(
    char phase,
    int complexity,
    const std::vector<std::uint64_t>& parent_level,
    const std::vector<std::uint64_t>& child_level
) {
    if (phase == 'p' && complexity == 3) {
        if (!contains(parent_level, 12)
            || !contains(child_level, 50)
            || !contains(child_level, 51)
            || contains(child_level, 48)
            || contains(child_level, 49)) {
            throw std::runtime_error("phase-p strict nonconverse example failed");
        }
    }
    if (phase == 'u' && complexity == 4) {
        if (!contains(parent_level, 26)
            || !contains(child_level, 104)
            || !contains(child_level, 105)
            || !contains(child_level, 107)
            || contains(child_level, 106)) {
            throw std::runtime_error("phase-u strict nonconverse example failed");
        }
    }
}

struct PhaseTotals {
    std::uint64_t outputs_checked = 0;
    std::uint64_t formula_checks = 0;
    std::uint64_t projected_parents = 0;
    std::uint64_t uncovered_parents = 0;
    std::array<std::uint64_t, 5> fibers{};
    std::uint64_t checksum = 1469598103934665603ULL;
};

PhaseTotals run_phase(char phase) {
    std::vector<std::uint64_t> states{
        phase == 'p' ? std::uint64_t{3} : std::uint64_t{1}
    };
    PhaseTotals totals;
    std::cout << "phase=" << phase << '\n';
    for (int complexity = 1; complexity <= MAXIMUM_COMPLEXITY; ++complexity) {
        const int expected_bits = phase == 'p'
            ? 2 * complexity
            : 2 * complexity - 1;
        for (std::uint64_t state : states) {
            if (bit_length(state) != expected_bits) {
                throw std::runtime_error("frontier bit-length law failed");
            }
            const std::uint64_t expected = projected_child_formula(state);
            for (char name : {'t', 'u', 'p'}) {
                if ((forward_generator(name, state) >> 2) != expected) {
                    throw std::runtime_error("projection identity failed");
                }
                ++totals.formula_checks;
            }
            totals.checksum ^= state + static_cast<std::uint64_t>(complexity);
            totals.checksum *= 1099511628211ULL;
        }
        totals.outputs_checked += states.size();

        if (complexity == MAXIMUM_COMPLEXITY) {
            std::cout << "level=" << complexity
                      << " distinct_outputs=" << states.size()
                      << '\n';
            break;
        }

        std::vector<std::uint64_t> next = next_level(states);
        const LevelSummary summary = projection_summary(states, next);
        verify_nonconverse(phase, complexity + 1, states, next);
        totals.projected_parents += summary.projected;
        totals.uncovered_parents += summary.uncovered;
        for (int size = 2; size <= 4; ++size) {
            totals.fibers[size] += summary.fibers[size];
        }
        std::cout << "level=" << (complexity + 1)
                  << " distinct_outputs=" << summary.outputs
                  << " projected_parents=" << summary.projected
                  << " preceding_outputs=" << states.size()
                  << " uncovered_preceding=" << summary.uncovered
                  << " fibers_2=" << summary.fibers[2]
                  << " fibers_3=" << summary.fibers[3]
                  << " fibers_4=" << summary.fibers[4]
                  << '\n';
        states.swap(next);
    }
    std::cout << "phase_outputs_checked=" << totals.outputs_checked << '\n';
    std::cout << "phase_formula_checks=" << totals.formula_checks << '\n';
    std::cout << "phase_projected_parents=" << totals.projected_parents << '\n';
    std::cout << "phase_uncovered_parents=" << totals.uncovered_parents << '\n';
    std::cout << "phase_fibers_2=" << totals.fibers[2] << '\n';
    std::cout << "phase_fibers_3=" << totals.fibers[3] << '\n';
    std::cout << "phase_fibers_4=" << totals.fibers[4] << '\n';
    std::cout << "phase_checksum=0x" << std::hex << std::setw(16)
              << std::setfill('0') << totals.checksum << std::dec
              << std::setfill(' ') << '\n';
    return totals;
}
}  // namespace

int main() {
    const std::uint64_t reproduced = apply_word(1, KNOWN_WORD);
    if (reproduced != KNOWN_COUNTEREXAMPLE) {
        throw std::runtime_error("known counterexample generator word failed");
    }

    const PhaseTotals p = run_phase('p');
    const PhaseTotals u = run_phase('u');

    const std::array<int, 3> depths{12, 14, 16};
    std::cout << "known_counterexample=0x" << std::hex
              << KNOWN_COUNTEREXAMPLE << std::dec << '\n';
    for (int depth : depths) {
        const std::uint64_t ancestor = KNOWN_COUNTEREXAMPLE >> (2 * depth);
        const int residual_complexity = 25 - depth;
        const int expected_bits = 2 * residual_complexity - 1;
        if (bit_length(ancestor) != expected_bits) {
            throw std::runtime_error("known ancestor bit-length mismatch");
        }
        std::cout << "known_ancestor depth=" << depth
                  << " residual_complexity=" << residual_complexity
                  << " value=0x" << std::hex << ancestor << std::dec
                  << " bit_length=" << bit_length(ancestor)
                  << '\n';
    }

    std::cout << "total_outputs_checked="
              << p.outputs_checked + u.outputs_checked << '\n';
    std::cout << "total_formula_checks="
              << p.formula_checks + u.formula_checks << '\n';
    std::cout << "projection_theorem=true\n";
    std::cout << "nonempty_fiber_size_range=2..4\n";
    return 0;
}
