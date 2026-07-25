#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace {
constexpr int MAXIMUM_COMPLEXITY = 25;
constexpr std::uint64_t KNOWN_COUNTEREXAMPLE = 0x1bcd3a7b3fdfbULL;
constexpr std::array<unsigned, 4> CHILD_MASK{0b1011, 0b1100, 0b1110, 0b0011};

std::uint64_t forward_generator(char name, std::uint64_t state) {
    const std::uint64_t stepped = state ^ ((state << 1) | (state << 2));
    if (name == 't') return stepped;
    if (name == 'u') return stepped ^ 1;
    if (name == 'p') return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    throw std::invalid_argument("unknown generator");
}

int bit_length(std::uint64_t value) {
    return value == 0 ? 0 : 64 - __builtin_clzll(value);
}

int expected_bits(char phase, int complexity) {
    return phase == 'p' ? 2 * complexity : 2 * complexity - 1;
}

std::optional<std::uint64_t> inverse_t(std::uint64_t output) {
    if (output == 0) return std::uint64_t{0};
    const int width = bit_length(output) - 2;
    if (width <= 0) return std::nullopt;
    std::uint64_t state = 0;
    for (int position = 0; position < width; ++position) {
        unsigned lower = 0;
        if (position >= 1) lower |= static_cast<unsigned>((state >> (position - 1)) & 1);
        if (position >= 2) lower |= static_cast<unsigned>((state >> (position - 2)) & 1);
        const unsigned value = static_cast<unsigned>((output >> position) & 1) ^ lower;
        state |= static_cast<std::uint64_t>(value) << position;
    }
    if (forward_generator('t', state) != output) return std::nullopt;
    return state;
}

std::optional<std::uint64_t> inverse_generator(char name, std::uint64_t output) {
    if (name == 't') return inverse_t(output);
    std::optional<std::uint64_t> state;
    if (name == 'u') {
        state = inverse_t(output ^ 1);
    } else if (name == 'p') {
        const unsigned recovered_low = static_cast<unsigned>(output & 1) ^ 1;
        const std::uint64_t adjusted = output ^ 1 ^ (recovered_low == 0 ? 2 : 0);
        state = inverse_t(adjusted);
    } else {
        throw std::invalid_argument("unknown inverse generator");
    }
    if (!state || forward_generator(name, *state) != output) return std::nullopt;
    return state;
}

std::optional<std::uint64_t> candidate_parent(std::uint64_t quotient, int digit) {
    const char generator = digit == 0 ? 't' : digit == 1 ? 'u' : 'p';
    const auto residual = inverse_generator(generator, quotient);
    if (!residual) return std::nullopt;
    return 4 * (*residual) + static_cast<std::uint64_t>(digit);
}

std::vector<std::uint64_t> next_level(const std::vector<std::uint64_t>& current) {
    std::vector<std::uint64_t> next;
    next.reserve(current.size() * 3);
    for (std::uint64_t state : current) {
        for (char generator : {'t', 'u', 'p'}) next.push_back(forward_generator(generator, state));
    }
    std::sort(next.begin(), next.end());
    next.erase(std::unique(next.begin(), next.end()), next.end());
    return next;
}

bool contains(const std::vector<std::uint64_t>& values, std::uint64_t target) {
    return std::binary_search(values.begin(), values.end(), target);
}

unsigned actual_fiber(const std::vector<std::uint64_t>& next, std::uint64_t quotient) {
    unsigned mask = 0;
    for (int digit = 0; digit < 4; ++digit) {
        if (contains(next, 4 * quotient + static_cast<std::uint64_t>(digit))) mask |= 1U << digit;
    }
    return mask;
}

bool allowed_fiber(unsigned mask) {
    return mask == 0b0000 || mask == 0b0011 || mask == 0b1011
        || mask == 0b1100 || mask == 0b1111;
}

struct Totals {
    std::uint64_t outputs = 0;
    std::uint64_t quotients = 0;
    std::uint64_t candidate_checks = 0;
    std::array<std::uint64_t, 16> fibers{};
    std::array<std::uint64_t, 16> predecessors{};
    std::uint64_t checksum = 1469598103934665603ULL;
};

Totals run_phase(char phase) {
    std::vector<std::uint64_t> current{phase == 'p' ? 3ULL : 1ULL};
    Totals totals;
    std::cout << "phase=" << phase << '\n';
    for (int complexity = 1; complexity <= MAXIMUM_COMPLEXITY; ++complexity) {
        for (std::uint64_t state : current) {
            if (bit_length(state) != expected_bits(phase, complexity)) {
                throw std::runtime_error("frontier bit-length law failed");
            }
            totals.checksum ^= state + (static_cast<std::uint64_t>(complexity) << 56);
            totals.checksum *= 1099511628211ULL;
        }
        totals.outputs += current.size();
        if (complexity == MAXIMUM_COMPLEXITY) {
            std::cout << "level=" << complexity << " outputs=" << current.size() << '\n';
            break;
        }

        const std::vector<std::uint64_t> next = next_level(current);
        std::array<std::uint64_t, 16> level_fibers{};
        std::uint64_t uncovered = 0;
        for (std::uint64_t quotient : current) {
            unsigned predecessor = 0;
            unsigned predicted = 0;
            for (int digit = 0; digit < 4; ++digit) {
                const auto parent = candidate_parent(quotient, digit);
                if (parent && contains(current, *parent)) {
                    predecessor |= 1U << digit;
                    predicted |= CHILD_MASK[digit];
                }
                ++totals.candidate_checks;
            }
            if ((predecessor & 0b0100) && !(predecessor & 0b1000)) {
                throw std::runtime_error("digit-two predecessor lacked digit-three mate");
            }
            const unsigned actual = actual_fiber(next, quotient);
            if (predicted != actual) throw std::runtime_error("lift recursion mismatch");
            if (!allowed_fiber(actual)) throw std::runtime_error("fiber escaped alphabet");
            ++totals.fibers[actual];
            ++totals.predecessors[predecessor];
            ++level_fibers[actual];
            ++totals.quotients;
            uncovered += actual == 0;
        }
        std::cout << "level=" << complexity
                  << " outputs=" << current.size()
                  << " next_outputs=" << next.size()
                  << " uncovered=" << uncovered
                  << " masks_0011=" << level_fibers[0b0011]
                  << " masks_1011=" << level_fibers[0b1011]
                  << " masks_1100=" << level_fibers[0b1100]
                  << " masks_1111=" << level_fibers[0b1111] << '\n';
        current = next;
    }
    std::cout << "phase_outputs_checked=" << totals.outputs << '\n';
    std::cout << "phase_quotients_checked=" << totals.quotients << '\n';
    std::cout << "phase_candidate_parent_checks=" << totals.candidate_checks << '\n';
    for (unsigned mask : {0U, 3U, 11U, 12U, 15U}) {
        std::cout << "phase_fiber_" << std::bitset<4>(mask)
                  << '=' << totals.fibers[mask] << '\n';
    }
    std::cout << "phase_checksum=0x" << std::hex << std::setw(16)
              << std::setfill('0') << totals.checksum << std::dec
              << std::setfill(' ') << '\n';
    return totals;
}

using Key = std::tuple<char, int, std::uint64_t>;
std::map<Key, bool> member_cache;
std::map<Key, std::string> witness_cache;

bool member(char phase, int complexity, std::uint64_t target) {
    const Key key{phase, complexity, target};
    if (const auto it = member_cache.find(key); it != member_cache.end()) return it->second;
    bool result = false;
    if (complexity >= 1 && bit_length(target) == expected_bits(phase, complexity)) {
        if (complexity == 1) {
            result = target == (phase == 'p' ? 3ULL : 1ULL);
        } else {
            const std::uint64_t quotient = target >> 2;
            const int digit = static_cast<int>(target & 3);
            for (int parent_digit = 0; parent_digit < 4 && !result; ++parent_digit) {
                if (((CHILD_MASK[parent_digit] >> digit) & 1U) == 0) continue;
                const auto parent = candidate_parent(quotient, parent_digit);
                if (parent && member(phase, complexity - 1, *parent)) result = true;
            }
        }
    }
    member_cache.emplace(key, result);
    return result;
}

std::string witness(char phase, int complexity, std::uint64_t target) {
    const Key key{phase, complexity, target};
    if (const auto it = witness_cache.find(key); it != witness_cache.end()) return it->second;
    if (!member(phase, complexity, target)) return {};
    if (complexity == 1) {
        const std::string result(1, phase);
        witness_cache.emplace(key, result);
        return result;
    }
    const std::uint64_t quotient = target >> 2;
    const int digit = static_cast<int>(target & 3);
    for (int parent_digit = 0; parent_digit < 4; ++parent_digit) {
        if (((CHILD_MASK[parent_digit] >> digit) & 1U) == 0) continue;
        const auto parent = candidate_parent(quotient, parent_digit);
        if (!parent || !member(phase, complexity - 1, *parent)) continue;
        std::string prefix = witness(phase, complexity - 1, *parent);
        for (char generator : {'t', 'u', 'p'}) {
            if (forward_generator(generator, *parent) == target) {
                prefix.push_back(generator);
                witness_cache.emplace(key, prefix);
                return prefix;
            }
        }
    }
    throw std::runtime_error("membership lacked witness");
}

std::uint64_t apply_word(const std::string& word) {
    if (word.empty()) throw std::invalid_argument("empty word");
    std::uint64_t state = word.front() == 'p' ? 3ULL : 1ULL;
    for (std::size_t index = 1; index < word.size(); ++index) {
        state = forward_generator(word[index], state);
    }
    return state;
}
}  // namespace

int main() {
    const Totals p = run_phase('p');
    const Totals u = run_phase('u');
    if (!member('u', 25, KNOWN_COUNTEREXAMPLE)) {
        throw std::runtime_error("recursive criterion missed counterexample");
    }
    const std::string word = witness('u', 25, KNOWN_COUNTEREXAMPLE);
    if (word.size() != 25 || apply_word(word) != KNOWN_COUNTEREXAMPLE) {
        throw std::runtime_error("recursive witness replay failed");
    }
    std::cout << "known_counterexample=0x" << std::hex << KNOWN_COUNTEREXAMPLE << std::dec << '\n';
    std::cout << "recovered_generator_word=" << word << '\n';
    std::cout << "recursive_cache_entries=" << member_cache.size() << '\n';
    std::cout << "total_outputs_checked=" << p.outputs + u.outputs << '\n';
    std::cout << "total_quotients_checked=" << p.quotients + u.quotients << '\n';
    std::cout << "total_candidate_parent_checks=" << p.candidate_checks + u.candidate_checks << '\n';
    std::cout << "exact_lift_recursion=true\n";
    std::cout << "fiber_alphabet=0000,0011,1011,1100,1111\n";
    return 0;
}
