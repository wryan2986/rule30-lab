#include <algorithm>
#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr std::array<char, 3> LETTERS{'t', 'p', 'u'};

uint64_t width_mask(int width) {
    if (width < 0 || width > 62) {
        throw std::invalid_argument("width must lie between zero and 62");
    }
    return width == 0 ? 0 : ((uint64_t{1} << width) - 1);
}

uint64_t forward_t(uint64_t state) {
    return state ^ ((state << 1) | (state << 2));
}

uint64_t forward_generator(char letter, uint64_t state, int width) {
    const uint64_t mask = width_mask(width);
    const uint64_t stepped = forward_t(state) & mask;
    if (letter == 't') return stepped;
    if (letter == 'u') return stepped ^ 1;
    if (letter == 'p') return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    throw std::invalid_argument("unknown generator");
}

uint64_t inverse_t_mod(uint64_t output, int width) {
    output &= width_mask(width);
    uint64_t state = 0;
    for (int position = 0; position < width; ++position) {
        uint64_t previous = 0;
        if (position >= 1) previous |= (state >> (position - 1)) & 1;
        if (position >= 2) previous |= (state >> (position - 2)) & 1;
        const uint64_t bit = ((output >> position) & 1) ^ previous;
        state |= bit << position;
    }
    return state;
}

uint64_t inverse_generator_mod(char letter, uint64_t output, int width) {
    output &= width_mask(width);
    if (letter == 't') return inverse_t_mod(output, width);
    if (letter == 'u') return inverse_t_mod(output ^ 1, width);
    if (letter == 'p') {
        const uint64_t recovered_low_bit = (output & 1) ^ 1;
        const uint64_t adjusted = output ^ 1 ^ (recovered_low_bit == 0 ? 2 : 0);
        return inverse_t_mod(adjusted, width);
    }
    throw std::invalid_argument("unknown generator");
}

uint64_t fringe_step(uint64_t state) {
    const uint64_t packed = 1 + 2 * state;
    const uint64_t odd = packed ^ ((packed >> 1) | (packed >> 2));
    return (odd << 1) ^ (odd | (odd >> 1));
}

std::vector<char> actual_driver(int length) {
    uint64_t state = 0;
    std::vector<char> result;
    result.reserve(length);
    for (int index = 0; index < length; ++index) {
        result.push_back((state & 3) == 0 ? 'u' : 't');
        state = fringe_step(state);
    }
    return result;
}

uint64_t backward_zero_branch(char branch, uint64_t successor, int width) {
    const int inner_width = width - 2;
    uint64_t state = inverse_generator_mod(branch, successor, inner_width);
    state = inverse_generator_mod('p', state, inner_width);
    return ((state << 2) | 3) & width_mask(width);
}

uint64_t actual_survivor_residue(int depth) {
    const auto driver = actual_driver(depth);
    uint64_t state = 0;
    int precision = 0;
    for (auto iterator = driver.rbegin(); iterator != driver.rend(); ++iterator) {
        precision += 2;
        state = backward_zero_branch(*iterator, state, precision);
    }
    return state;
}

struct BackwardBall {
    std::unordered_map<uint64_t, uint8_t> distance;
    std::vector<std::size_t> layer_sizes;
};

BackwardBall build_backward_ball(
    uint64_t target, int width, int maximum_distance
) {
    BackwardBall ball;
    ball.distance.reserve(10'000'000);
    std::vector<uint64_t> frontier{target};
    std::vector<uint64_t> next;
    ball.distance.emplace(target, 0);
    ball.layer_sizes.push_back(1);
    for (int distance = 0; distance < maximum_distance; ++distance) {
        next.clear();
        next.reserve(frontier.size() * 2);
        for (uint64_t image : frontier) {
            for (char letter : LETTERS) {
                const uint64_t source = inverse_generator_mod(letter, image, width);
                if (ball.distance.emplace(source, distance + 1).second) {
                    next.push_back(source);
                }
            }
        }
        frontier.swap(next);
        ball.layer_sizes.push_back(frontier.size());
    }
    return ball;
}

struct PhaseResult {
    int minimum_length;
    std::size_t forward_states;
    int last_forward_depth;
};

PhaseResult solve_phase(
    char phase,
    int width,
    int reverse_depth,
    const std::unordered_map<uint64_t, uint8_t>& backward
) {
    const uint64_t start = forward_generator(phase, 0, width);
    std::unordered_set<uint64_t> seen;
    seen.reserve(20'000'000);
    std::vector<uint64_t> frontier{start};
    std::vector<uint64_t> next;
    seen.insert(start);
    int best = std::numeric_limits<int>::max();
    int forward_depth = 0;
    while (!frontier.empty()) {
        for (uint64_t state : frontier) {
            const auto found = backward.find(state);
            if (found != backward.end()) {
                best = std::min(best, 1 + forward_depth + static_cast<int>(found->second));
            }
        }
        if (best != std::numeric_limits<int>::max()
            && forward_depth >= best - 1 - reverse_depth) {
            break;
        }
        next.clear();
        next.reserve(frontier.size() * 2);
        for (uint64_t state : frontier) {
            for (char letter : LETTERS) {
                const uint64_t image = forward_generator(letter, state, width);
                if (seen.insert(image).second) next.push_back(image);
            }
        }
        frontier.swap(next);
        ++forward_depth;
    }
    if (best == std::numeric_limits<int>::max()) {
        throw std::runtime_error("forward and reverse searches did not meet");
    }
    return {best, seen.size(), forward_depth};
}

int reverse_depth_for(int depth) {
    switch (depth) {
        case 12: return 14;
        case 13: return 15;
        case 14: return 16;
        case 15: return 18;
        case 16: return 20;
        case 17: return 20;
        case 18: return 21;
        case 19: return 21;
        case 20: return 24;
        default: return depth + 2;
    }
}

std::pair<int, int> expected_distances(int depth) {
    static const std::array<std::pair<int, int>, 21> expected{{
        {0, 0},
        {1, 2}, {3, 2}, {7, 2}, {8, 7}, {8, 12},
        {12, 14}, {13, 14}, {17, 14}, {17, 18}, {17, 19},
        {21, 26}, {28, 27}, {30, 30}, {33, 30}, {34, 30},
        {36, 30}, {40, 40}, {40, 42}, {42, 42}, {47, 49},
    }};
    return expected.at(depth);
}

}  // namespace

int main(int argc, char** argv) {
    int minimum_depth = 12;
    int maximum_depth = 20;
    if (argc >= 2) minimum_depth = std::stoi(argv[1]);
    if (argc >= 3) maximum_depth = std::stoi(argv[2]);
    if (minimum_depth < 1 || maximum_depth > 20 || minimum_depth > maximum_depth) {
        std::cerr << "depth range must satisfy 1 <= minimum <= maximum <= 20\n";
        return 2;
    }

    std::cout << "depth target_hex reverse_depth reverse_states "
                 "p_length p_forward_states p_forward_depth "
                 "u_length u_forward_states u_forward_depth\n";
    for (int depth = minimum_depth; depth <= maximum_depth; ++depth) {
        const int width = 2 * depth;
        const uint64_t target = actual_survivor_residue(depth);
        const int reverse_depth = reverse_depth_for(depth);
        const BackwardBall ball = build_backward_ball(target, width, reverse_depth);
        const PhaseResult p_result = solve_phase(
            'p', width, reverse_depth, ball.distance
        );
        const PhaseResult u_result = solve_phase(
            'u', width, reverse_depth, ball.distance
        );
        const auto expected = expected_distances(depth);
        if (p_result.minimum_length != expected.first
            || u_result.minimum_length != expected.second) {
            std::cerr << "unexpected exact distance at depth " << depth << "\n";
            return 3;
        }
        std::cout << depth << " 0x" << std::hex << target << std::dec
                  << ' ' << reverse_depth
                  << ' ' << ball.distance.size()
                  << ' ' << p_result.minimum_length
                  << ' ' << p_result.forward_states
                  << ' ' << p_result.last_forward_depth
                  << ' ' << u_result.minimum_length
                  << ' ' << u_result.forward_states
                  << ' ' << u_result.last_forward_depth
                  << '\n';
    }
    return 0;
}
