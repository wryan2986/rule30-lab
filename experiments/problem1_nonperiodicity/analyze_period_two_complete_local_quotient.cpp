#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

using u128 = unsigned __int128;

std::string decimal_u128(u128 value) {
    if (value == 0) return "0";
    std::string digits;
    while (value > 0) {
        digits.push_back(static_cast<char>('0' + value % 10));
        value /= 10;
    }
    std::reverse(digits.begin(), digits.end());
    return digits;
}

namespace {

constexpr int SPAN = 5;
constexpr int MODULUS = 1 << (2 * SPAN);
constexpr int HISTORY_WIDTH = SPAN - 1;
constexpr int CERTIFICATE_STEPS = 112;
constexpr std::array<char, 3> LETTERS{'t', 'u', 'p'};

uint64_t forward_t(uint64_t state) {
    return state ^ ((state << 1) | (state << 2));
}

uint64_t forward_generator(int letter, uint64_t state) {
    const uint64_t stepped = forward_t(state);
    if (letter == 0) return stepped;
    if (letter == 1) return stepped ^ 1;
    return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
}

int power_int(int base, int exponent) {
    int result = 1;
    while (exponent-- > 0) result *= base;
    return result;
}

std::vector<int> decode_word(int code, int length) {
    std::vector<int> digits(length);
    for (int index = length - 1; index >= 0; --index) {
        digits[index] = code % 3;
        code /= 3;
    }
    return digits;
}

int apply_word_mod(int residue, int code, int length, int modulus) {
    for (int letter : decode_word(code, length)) {
        residue = static_cast<int>(forward_generator(letter, residue)) & (modulus - 1);
    }
    return residue;
}

struct LocalTables {
    std::array<std::vector<uint8_t>, SPAN + 1> minimal;
    std::array<int, SPAN + 1> word_counts{};
    std::array<int, SPAN + 1> residue_counts{};

    LocalTables() {
        for (int length = 1; length <= SPAN; ++length) {
            const int words = power_int(3, length);
            const int residues = 1 << (2 * length);
            word_counts[length] = words;
            residue_counts[length] = residues;
            minimal[length].assign(residues * words, 0);
            std::vector<int> best(residues, -1);
            for (int start = 0; start < residues; ++start) {
                std::fill(best.begin(), best.end(), -1);
                for (int word = 0; word < words; ++word) {
                    const int output = apply_word_mod(start, word, length, residues);
                    if (best[output] < 0) best[output] = word;
                }
                for (int word = 0; word < words; ++word) {
                    const int output = apply_word_mod(start, word, length, residues);
                    minimal[length][start * words + word] = (best[output] == word);
                }
            }
        }
    }

    bool is_minimal(int length, int start, int word) const {
        const int residue_mask = residue_counts[length] - 1;
        return minimal[length][(start & residue_mask) * word_counts[length] + word] != 0;
    }
};

struct State {
    uint16_t residue;
    uint8_t history_length;
    uint8_t history_code;
};

uint32_t state_key(const State& state) {
    return static_cast<uint32_t>(state.residue)
        | (static_cast<uint32_t>(state.history_length) << 10)
        | (static_cast<uint32_t>(state.history_code) << 13);
}

struct Automaton {
    LocalTables tables;
    std::array<std::array<uint16_t, MODULUS>, 3> inverse{};
    std::vector<State> states;
    std::vector<std::array<int32_t, 3>> transitions;
    std::unordered_map<uint32_t, int32_t> index;
    int32_t phase_p_start = -1;
    int32_t phase_u_start = -1;

    Automaton() {
        build_inverse();
        build_graph();
    }

    void build_inverse() {
        for (int letter = 0; letter < 3; ++letter) {
            std::array<bool, MODULUS> seen{};
            for (int state = 0; state < MODULUS; ++state) {
                const int image = static_cast<int>(forward_generator(letter, state)) & (MODULUS - 1);
                if (seen[image]) throw std::runtime_error("generator is not invertible");
                seen[image] = true;
                inverse[letter][image] = static_cast<uint16_t>(state);
            }
        }
    }

    int invert_suffix(int residue, int code, int length) const {
        const auto digits = decode_word(code, length);
        for (int index = length - 1; index >= 0; --index) {
            residue = inverse[digits[index]][residue];
        }
        return residue;
    }

    bool step(const State& state, int letter, State& output) const {
        const int new_residue = static_cast<int>(forward_generator(letter, state.residue)) & (MODULUS - 1);
        const int full_length = std::min<int>(SPAN, state.history_length + 1);
        const int full_code = state.history_code * 3 + letter;

        for (int length = 1; length <= full_length; ++length) {
            const int words = tables.word_counts[length];
            const int suffix = full_code % words;
            const int start = invert_suffix(new_residue, suffix, length);
            if (!tables.is_minimal(length, start, suffix)) return false;
        }

        output.residue = static_cast<uint16_t>(new_residue);
        output.history_length = static_cast<uint8_t>(std::min<int>(HISTORY_WIDTH, state.history_length + 1));
        output.history_code = static_cast<uint8_t>(full_code % power_int(3, HISTORY_WIDTH));
        return true;
    }

    int32_t add_state(const State& state, std::queue<int32_t>& queue) {
        const uint32_t key = state_key(state);
        const auto found = index.find(key);
        if (found != index.end()) return found->second;
        const int32_t id = static_cast<int32_t>(states.size());
        index.emplace(key, id);
        states.push_back(state);
        transitions.push_back({-2, -2, -2});
        queue.push(id);
        return id;
    }

    void build_graph() {
        index.reserve(30000);
        std::queue<int32_t> queue;
        phase_p_start = add_state(State{3, 1, 2}, queue);
        phase_u_start = add_state(State{1, 1, 1}, queue);
        while (!queue.empty()) {
            const int32_t source = queue.front();
            queue.pop();
            const State state = states[source];
            for (int letter = 0; letter < 3; ++letter) {
                State image{};
                transitions[source][letter] = step(state, letter, image)
                    ? add_state(image, queue)
                    : -1;
            }
        }
    }

    long double spectral_radius(int iterations = 500) const {
        std::vector<long double> vector(states.size(), 1.0L);
        std::vector<long double> updated(states.size());
        for (int iteration = 0; iteration < iterations; ++iteration) {
            long double scale = 0.0L;
            for (std::size_t source = 0; source < states.size(); ++source) {
                long double total = 0.0L;
                for (int32_t target : transitions[source]) {
                    if (target >= 0) total += vector[target];
                }
                updated[source] = total;
                scale = std::max(scale, total);
            }
            for (std::size_t position = 0; position < vector.size(); ++position) {
                vector[position] = updated[position] / scale;
            }
        }
        long double lower = std::numeric_limits<long double>::infinity();
        long double upper = 0.0L;
        for (std::size_t source = 0; source < states.size(); ++source) {
            long double total = 0.0L;
            for (int32_t target : transitions[source]) {
                if (target >= 0) total += vector[target];
            }
            if (vector[source] > 1e-24L) {
                const long double ratio = total / vector[source];
                lower = std::min(lower, ratio);
                upper = std::max(upper, ratio);
            }
        }
        return (lower + upper) / 2;
    }

    u128 maximum_continuations(int steps) const {
        std::vector<u128> current(states.size(), 1);
        std::vector<u128> updated(states.size());
        for (int step_index = 0; step_index < steps; ++step_index) {
            for (std::size_t source = 0; source < states.size(); ++source) {
                u128 total = 0;
                for (int32_t target : transitions[source]) {
                    if (target >= 0) total += current[target];
                }
                updated[source] = total;
            }
            current.swap(updated);
        }
        return *std::max_element(current.begin(), current.end());
    }

    uint64_t phase_count(int32_t start, int total_length) const {
        std::vector<uint64_t> current(states.size(), 0);
        std::vector<uint64_t> updated(states.size(), 0);
        current[start] = 1;
        for (int length = 2; length <= total_length; ++length) {
            std::fill(updated.begin(), updated.end(), 0);
            for (std::size_t source = 0; source < states.size(); ++source) {
                if (current[source] == 0) continue;
                for (int32_t target : transitions[source]) {
                    if (target >= 0) updated[target] += current[source];
                }
            }
            current.swap(updated);
        }
        uint64_t total = 0;
        for (uint64_t count : current) total += count;
        return total;
    }
};

}  // namespace

int main() {
    const Automaton automaton;
    const long double radius = automaton.spectral_radius();
    const u128 maximum = automaton.maximum_continuations(CERTIFICATE_STEPS);
    const u128 binary = u128{1} << CERTIFICATE_STEPS;
    if (!(maximum < binary)) {
        std::cerr << "below-binary certificate failed\n";
        return 2;
    }
    if (automaton.states.size() != 21615) {
        std::cerr << "unexpected reachable state count\n";
        return 3;
    }
    const u128 expected = (u128{0xff9da21103f2ULL} << 64) | u128{0xdca8bea29790526dULL};
    if (maximum != expected) {
        std::cerr << "unexpected continuation certificate\n";
        return 4;
    }

    std::size_t transition_count = 0;
    for (const auto& row : automaton.transitions) {
        transition_count += std::count_if(
            row.begin(), row.end(), [](int32_t value) { return value >= 0; });
    }

    std::cout << "span " << SPAN << '\n';
    std::cout << "modulus " << MODULUS << '\n';
    std::cout << "reachable_states " << automaton.states.size() << '\n';
    std::cout << "allowed_transitions " << transition_count << '\n';
    std::cout << std::setprecision(18);
    std::cout << "spectral_radius_approx " << static_cast<double>(radius) << '\n';
    std::cout << "generic_complexity_rate_approx "
              << static_cast<double>(std::log(2.0L) / std::log(radius)) << '\n';
    std::cout << "certificate_steps " << CERTIFICATE_STEPS << '\n';
    std::cout << "maximum_continuations " << decimal_u128(maximum) << '\n';
    std::cout << "binary_continuations " << decimal_u128(binary) << '\n';
    std::cout << "strictly_below_binary true\n";
    std::cout << "phase_p_length18 " << automaton.phase_count(automaton.phase_p_start, 18) << '\n';
    std::cout << "phase_u_length18 " << automaton.phase_count(automaton.phase_u_start, 18) << '\n';
    return 0;
}
