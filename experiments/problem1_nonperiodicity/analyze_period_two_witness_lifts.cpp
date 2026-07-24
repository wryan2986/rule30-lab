#include <algorithm>
#include <array>
#include <climits>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr std::array<char, 3> LETTERS{'t', 'p', 'u'};

uint64_t mix64(uint64_t value) {
    value += 0x9e3779b97f4a7c15ULL;
    value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
    value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
    return value ^ (value >> 31);
}

class FlatTable {
  public:
    FlatTable(std::size_t capacity, bool store_values)
        : keys_(capacity, 0),
          values_(store_values ? capacity : 0),
          mask_(capacity - 1) {
        if (capacity == 0 || (capacity & (capacity - 1)) != 0) {
            throw std::invalid_argument("capacity must be a power of two");
        }
    }

    bool insert(uint64_t key, uint8_t value = 0) {
        const uint64_t stored = key + 1;
        std::size_t position = mix64(key) & mask_;
        while (true) {
            if (keys_[position] == 0) {
                keys_[position] = stored;
                if (!values_.empty()) values_[position] = value;
                ++size_;
                return true;
            }
            if (keys_[position] == stored) return false;
            position = (position + 1) & mask_;
        }
    }

    int find(uint64_t key) const {
        const uint64_t stored = key + 1;
        std::size_t position = mix64(key) & mask_;
        while (true) {
            const uint64_t observed = keys_[position];
            if (observed == 0) return -1;
            if (observed == stored) {
                return values_.empty() ? 0 : values_[position];
            }
            position = (position + 1) & mask_;
        }
    }

    std::size_t size() const { return size_; }

  private:
    std::vector<uint64_t> keys_;
    std::vector<uint8_t> values_;
    std::size_t mask_;
    std::size_t size_ = 0;
};

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
    const uint64_t stepped = forward_t(state) & width_mask(width);
    if (letter == 't') return stepped;
    if (letter == 'u') return stepped ^ 1;
    if (letter == 'p') {
        return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    }
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
        const uint64_t adjusted =
            output ^ 1 ^ (recovered_low_bit == 0 ? 2 : 0);
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

std::array<int, 4> lift_profile(int base_depth, char phase) {
    const int width = 2 * (base_depth + 1);
    const uint64_t base = actual_survivor_residue(base_depth);
    std::array<uint32_t, 4> targets{};
    for (int digit = 0; digit < 4; ++digit) {
        targets[digit] = static_cast<uint32_t>(
            base + (static_cast<uint64_t>(digit) << (2 * base_depth))
        );
    }

    const std::size_t state_count = std::size_t{1} << width;
    std::vector<uint8_t> distance(state_count, 255);
    std::vector<uint32_t> queue;
    queue.reserve(std::min<std::size_t>(state_count, 100'000'000));
    const uint32_t start = static_cast<uint32_t>(
        forward_generator(phase, 0, width)
    );
    distance[start] = 0;
    queue.push_back(start);

    std::array<int, 4> answer{-1, -1, -1, -1};
    int remaining = 4;
    for (int digit = 0; digit < 4; ++digit) {
        if (start == targets[digit]) {
            answer[digit] = 1;
            --remaining;
        }
    }

    for (std::size_t head = 0; head < queue.size() && remaining; ++head) {
        const uint32_t state = queue[head];
        const uint8_t next_distance = distance[state] + 1;
        for (char letter : LETTERS) {
            const uint32_t image = static_cast<uint32_t>(
                forward_generator(letter, state, width)
            );
            if (distance[image] != 255) continue;
            distance[image] = next_distance;
            queue.push_back(image);
            for (int digit = 0; digit < 4; ++digit) {
                if (answer[digit] < 0 && image == targets[digit]) {
                    answer[digit] = next_distance + 1;
                    --remaining;
                }
            }
        }
    }
    if (remaining) throw std::runtime_error("lift target was unreachable");
    return answer;
}

struct BackwardBall {
    FlatTable distances;
    explicit BackwardBall(std::size_t capacity) : distances(capacity, true) {}
};

BackwardBall build_backward_ball(
    uint64_t target,
    int width,
    int maximum_distance,
    std::size_t capacity
) {
    BackwardBall ball(capacity);
    std::vector<uint64_t> frontier{target};
    std::vector<uint64_t> next;
    ball.distances.insert(target, 0);
    for (int distance = 0; distance < maximum_distance; ++distance) {
        next.clear();
        next.reserve(frontier.size() * 2);
        for (uint64_t image : frontier) {
            for (char letter : LETTERS) {
                const uint64_t source = inverse_generator_mod(letter, image, width);
                if (ball.distances.insert(source, distance + 1)) {
                    next.push_back(source);
                }
            }
        }
        frontier.swap(next);
    }
    return ball;
}

struct PhaseDistance {
    int minimum_length;
    std::size_t forward_states;
};

PhaseDistance solve_phase(
    char phase,
    int width,
    int reverse_depth,
    const FlatTable& backward,
    std::size_t forward_capacity
) {
    const uint64_t start = forward_generator(phase, 0, width);
    FlatTable seen(forward_capacity, false);
    std::vector<uint64_t> frontier{start};
    std::vector<uint64_t> next;
    seen.insert(start);
    int best = INT_MAX;
    int forward_depth = 0;

    while (!frontier.empty()) {
        for (uint64_t state : frontier) {
            const int backward_distance = backward.find(state);
            if (backward_distance >= 0) {
                best = std::min(
                    best,
                    1 + forward_depth + backward_distance
                );
            }
        }
        if (best != INT_MAX
            && forward_depth >= best - 1 - reverse_depth) {
            break;
        }

        next.clear();
        next.reserve(frontier.size() * 2);
        for (uint64_t state : frontier) {
            for (char letter : LETTERS) {
                const uint64_t image = forward_generator(letter, state, width);
                if (seen.insert(image)) next.push_back(image);
            }
        }
        frontier.swap(next);
        ++forward_depth;
    }

    if (best == INT_MAX) {
        throw std::runtime_error("forward and reverse searches did not meet");
    }
    return {best, seen.size()};
}

struct SearchSettings {
    int depth;
    int reverse_depth;
    std::size_t backward_capacity;
    std::size_t forward_capacity;
    int expected_p;
    int expected_u;
};

void run_actual_distance(const SearchSettings& settings) {
    const int width = 2 * settings.depth;
    const uint64_t target = actual_survivor_residue(settings.depth);
    auto backward = build_backward_ball(
        target,
        width,
        settings.reverse_depth,
        settings.backward_capacity
    );
    const auto p = solve_phase(
        'p', width, settings.reverse_depth,
        backward.distances, settings.forward_capacity
    );
    const auto u = solve_phase(
        'u', width, settings.reverse_depth,
        backward.distances, settings.forward_capacity
    );
    if (p.minimum_length != settings.expected_p
        || u.minimum_length != settings.expected_u) {
        throw std::runtime_error("unexpected exact phase distance");
    }
    std::cout << "distance " << settings.depth << ' '
              << p.minimum_length << ' ' << u.minimum_length << ' '
              << backward.distances.size() << ' '
              << p.forward_states << ' ' << u.forward_states << '\n';
}

}  // namespace

int main(int argc, char** argv) {
    int maximum_profile_depth = 12;
    bool run_distances = true;
    if (argc >= 2) maximum_profile_depth = std::stoi(argv[1]);
    if (argc >= 3) run_distances = std::stoi(argv[2]) != 0;
    if (maximum_profile_depth < 1 || maximum_profile_depth > 12) {
        std::cerr << "maximum profile depth must lie between 1 and 12\n";
        return 2;
    }

    for (int base_depth = 1; base_depth <= maximum_profile_depth; ++base_depth) {
        const auto p = lift_profile(base_depth, 'p');
        const auto u = lift_profile(base_depth, 'u');
        const int actual_digit = static_cast<int>(
            (actual_survivor_residue(base_depth + 1) >> (2 * base_depth)) & 3
        );
        std::cout << "profile " << base_depth << ' ' << actual_digit;
        for (int value : p) std::cout << ' ' << value;
        for (int value : u) std::cout << ' ' << value;
        std::cout << '\n';
    }

    if (run_distances) {
        run_actual_distance({21, 25, std::size_t{1} << 25,
                             std::size_t{1} << 25, 49, 52});
        run_actual_distance({22, 27, std::size_t{1} << 26,
                             std::size_t{1} << 24, 51, 52});
    }
    return 0;
}
