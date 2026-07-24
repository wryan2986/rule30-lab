#include <algorithm>
#include <bit>
#include <cstdint>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>

namespace {

uint64_t forward_t(uint64_t state) {
    return state ^ ((state << 1) | (state << 2));
}

uint64_t fringe_step(uint64_t state) {
    const uint64_t packed = 1 + 2 * state;
    const uint64_t odd = packed ^ ((packed >> 1) | (packed >> 2));
    return (odd << 1) ^ (odd | (odd >> 1));
}

std::vector<char> actual_driver(std::size_t length) {
    uint64_t state = 0;
    std::vector<char> result;
    result.reserve(length);
    for (std::size_t index = 0; index < length; ++index) {
        result.push_back((state & 3) == 0 ? 'u' : 't');
        if (index + 1 < length) {
            state = fringe_step(state);
        }
    }
    return result;
}

uint64_t width_mask(unsigned width) {
    return width == 64 ? ~uint64_t{0} : ((uint64_t{1} << width) - 1);
}

uint64_t inverse_t_mod(uint64_t output, unsigned width) {
    output &= width_mask(width);
    uint64_t state = 0;
    for (unsigned position = 0; position < width; ++position) {
        const uint64_t previous_one = position >= 1 ? ((state >> (position - 1)) & 1) : 0;
        const uint64_t previous_two = position >= 2 ? ((state >> (position - 2)) & 1) : 0;
        const uint64_t bit = ((output >> position) & 1) ^ (previous_one | previous_two);
        state |= bit << position;
    }
    return state;
}

uint64_t inverse_generator_mod(char name, uint64_t output, unsigned width) {
    if (width == 0) {
        return 0;
    }
    output &= width_mask(width);
    if (name == 't') {
        return inverse_t_mod(output, width);
    }
    if (name == 'u') {
        return inverse_t_mod(output ^ 1, width);
    }
    const uint64_t recovered_low_bit = (output & 1) ^ 1;
    const uint64_t adjusted = output ^ 1 ^ (recovered_low_bit == 0 ? 2 : 0);
    return inverse_t_mod(adjusted, width);
}

uint64_t backward_zero_branch(char branch, uint64_t successor, unsigned width) {
    const unsigned inner_width = width - 2;
    uint64_t state = inverse_generator_mod(branch, successor, inner_width);
    state = inverse_generator_mod('p', state, inner_width);
    return ((state << 2) | 3) & width_mask(width);
}

uint64_t actual_survivor_64() {
    const auto driver = actual_driver(32);
    uint64_t state = 0;
    unsigned precision = 0;
    for (auto iterator = driver.rbegin(); iterator != driver.rend(); ++iterator) {
        precision += 2;
        state = backward_zero_branch(*iterator, state, precision);
    }
    return state;
}

int valuation_difference(uint64_t left, uint64_t right) {
    const uint64_t difference = left - right;
    return difference == 0 ? 64 : std::countr_zero(difference);
}

void run_phase(char phase, uint64_t initial, int maximum_length, uint64_t survivor) {
    std::vector<uint64_t> current{initial};
    std::unordered_set<uint64_t> cumulative;
    cumulative.reserve(17000000);

    for (int length = 1; length <= maximum_length; ++length) {
        if (length > 1) {
            std::vector<uint64_t> next;
            next.reserve(current.size() * 3);
            for (uint64_t state : current) {
                const uint64_t stepped = forward_t(state);
                next.push_back(stepped);
                next.push_back(stepped ^ 1);
                if ((state & 1) == 0) {
                    next.push_back(stepped ^ 3);
                }
            }
            std::sort(next.begin(), next.end());
            next.erase(std::unique(next.begin(), next.end()), next.end());
            current.swap(next);
        }

        for (uint64_t state : current) {
            cumulative.insert(state);
        }

        int best_valuation = -1;
        uint64_t best_state = 0;
        for (uint64_t state : cumulative) {
            const int valuation = valuation_difference(state, survivor);
            if (valuation > best_valuation) {
                best_valuation = valuation;
                best_state = state;
            }
        }

        std::cout << phase << ' ' << length << ' ' << current.size() << ' '
                  << cumulative.size() << ' ' << best_valuation << ' '
                  << best_valuation / 2 << ' ' << best_state << '\n';
    }
}

}  // namespace

int main(int argc, char** argv) {
    int maximum_length = 26;
    if (argc == 2) {
        maximum_length = std::stoi(argv[1]);
    }
    if (maximum_length < 1 || maximum_length > 26) {
        std::cerr << "maximum length must be between 1 and 26\n";
        return 2;
    }

    const uint64_t survivor = actual_survivor_64();
    if (survivor != 0x7fe13f3088c146c7ULL) {
        std::cerr << "unexpected actual survivor residue\n";
        return 3;
    }

    std::cout << "survivor_hex 0x" << std::hex << survivor << std::dec << '\n';
    std::cout << "phase length exact_states cumulative_states matching_bits complete_pairs best_state\n";
    run_phase('p', 3, maximum_length, survivor);
    run_phase('u', 1, maximum_length, survivor);
    return 0;
}
