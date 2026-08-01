#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <optional>
#include <set>
#include <stdexcept>
#include <tuple>
#include <vector>

using u64 = std::uint64_t;
constexpr int MAXK = 25;
constexpr std::array<unsigned, 4> CHILD{0b1011, 0b1100, 0b1110, 0b0011};

u64 forward(char generator, u64 state) {
    const u64 stepped = state ^ ((state << 1) | (state << 2));
    if (generator == 't') return stepped;
    if (generator == 'u') return stepped ^ 1;
    if (generator == 'p') return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    throw std::runtime_error("unknown generator");
}

std::vector<u64> next_level(const std::vector<u64>& current) {
    std::vector<u64> output;
    output.reserve(current.size() * 3);
    for (u64 state : current) {
        output.push_back(forward('t', state));
        output.push_back(forward('u', state));
        output.push_back(forward('p', state));
    }
    std::sort(output.begin(), output.end());
    output.erase(std::unique(output.begin(), output.end()), output.end());
    return output;
}

bool contains(const std::vector<u64>& values, u64 target) {
    return std::binary_search(values.begin(), values.end(), target);
}

int bit_length(u64 value) {
    return value ? 64 - __builtin_clzll(value) : 0;
}

std::optional<u64> inverse_t(u64 output) {
    if (output == 0) return u64{0};
    const int width = bit_length(output) - 2;
    if (width <= 0) return std::nullopt;
    u64 state = 0;
    for (int position = 0; position < width; ++position) {
        unsigned lower = 0;
        if (position >= 1) lower |= (state >> (position - 1)) & 1;
        if (position >= 2) lower |= (state >> (position - 2)) & 1;
        const unsigned bit = ((output >> position) & 1) ^ lower;
        state |= u64(bit) << position;
    }
    if (forward('t', state) != output) return std::nullopt;
    return state;
}

std::optional<u64> inverse_generator(char generator, u64 output) {
    std::optional<u64> state;
    if (generator == 't') {
        state = inverse_t(output);
    } else if (generator == 'u') {
        state = inverse_t(output ^ 1);
    } else if (generator == 'p') {
        const unsigned low = (output & 1) ^ 1;
        state = inverse_t(output ^ 1 ^ (low == 0 ? 2 : 0));
    } else {
        throw std::runtime_error("unknown generator");
    }
    if (!state || forward(generator, *state) != output) return std::nullopt;
    return state;
}

std::optional<u64> candidate_parent(u64 quotient, int digit) {
    const char generator = digit == 0 ? 't' : digit == 1 ? 'u' : 'p';
    const auto residual = inverse_generator(generator, quotient);
    if (!residual) return std::nullopt;
    return 4 * (*residual) + unsigned(digit);
}

unsigned fiber_from_predecessor(unsigned predecessor) {
    unsigned fiber = 0;
    for (int digit = 0; digit < 4; ++digit) {
        if ((predecessor >> digit) & 1) fiber |= CHILD[digit];
    }
    return fiber;
}

unsigned predecessor_mask(const std::vector<u64>& level, u64 quotient) {
    unsigned predecessor = 0;
    for (int digit = 0; digit < 4; ++digit) {
        const auto parent = candidate_parent(quotient, digit);
        if (parent && contains(level, *parent)) predecessor |= 1u << digit;
    }
    if ((predecessor & 4) && !(predecessor & 8)) {
        throw std::runtime_error("digit-2 predecessor lacked digit-3 mate");
    }
    return predecessor;
}

unsigned signature(const std::vector<u64>& level, u64 state) {
    const unsigned predecessor = predecessor_mask(level, state);
    return (predecessor << 4) | fiber_from_predecessor(predecessor);
}

struct Profile {
    unsigned source;
    std::array<unsigned, 4> target;
    bool operator<(const Profile& other) const {
        return std::tie(source, target) < std::tie(other.source, other.target);
    }
};

struct Campaign {
    u64 outputs = 0;
    std::set<unsigned> signatures;
    std::set<u64> edges;
    std::set<Profile> profiles;
    std::map<int, int> profiles_by_level;
};

Campaign campaign(char phase) {
    std::vector<u64> current{phase == 'p' ? 3ULL : 1ULL};
    Campaign result;
    for (int complexity = 1; complexity <= MAXK; ++complexity) {
        result.outputs += current.size();
        std::vector<unsigned> current_signatures;
        current_signatures.reserve(current.size());
        for (u64 state : current) {
            const unsigned value = signature(current, state);
            current_signatures.push_back(value);
            result.signatures.insert(value);
        }
        if (complexity == MAXK) break;

        auto next = next_level(current);
        std::vector<unsigned> next_signatures;
        next_signatures.reserve(next.size());
        for (u64 state : next) {
            const unsigned value = signature(next, state);
            next_signatures.push_back(value);
            result.signatures.insert(value);
        }

        std::set<Profile> level_profiles;
        for (std::size_t index = 0; index < current.size(); ++index) {
            const u64 state = current[index];
            Profile profile;
            profile.source = current_signatures[index];
            profile.target.fill(0xFFFF);
            for (int digit = 0; digit < 4; ++digit) {
                const u64 child = 4 * state + digit;
                const auto found = std::lower_bound(next.begin(), next.end(), child);
                if (found == next.end() || *found != child) continue;
                const std::size_t child_index = found - next.begin();
                const unsigned target = next_signatures[child_index];
                profile.target[digit] = target;
                const u64 code = (u64(profile.source) << 24)
                    | (u64(digit) << 20) | u64(target);
                result.edges.insert(code);
            }
            result.profiles.insert(profile);
            level_profiles.insert(profile);
        }
        result.profiles_by_level[complexity] = level_profiles.size();
        current.swap(next);
    }
    return result;
}

int main() {
    const Campaign phase_p = campaign('p');
    const Campaign phase_u = campaign('u');
    std::vector<unsigned> signatures(
        phase_p.signatures.begin(), phase_p.signatures.end()
    );
    std::map<unsigned, int> index;
    for (int position = 0; position < static_cast<int>(signatures.size()); ++position) {
        index[signatures[position]] = position;
    }

    const int signature_count = signatures.size();
    std::vector<std::array<unsigned, 4>> post(signature_count);
    for (auto& row : post) row.fill(0);
    for (u64 code : phase_p.edges) {
        const unsigned source = (code >> 24) & 0xFF;
        const unsigned digit = (code >> 20) & 0xF;
        const unsigned target = code & 0xFFFF;
        post[index[source]][digit] |= 1u << index[target];
    }

    const int subset_count = 1 << signature_count;
    std::vector<std::array<unsigned, 4>> subset_post(subset_count);
    for (auto& row : subset_post) row.fill(0);
    for (int subset = 1; subset < subset_count; ++subset) {
        const int bit = __builtin_ctz(subset);
        const int previous = subset & (subset - 1);
        for (int digit = 0; digit < 4; ++digit) {
            subset_post[subset][digit] =
                subset_post[previous][digit] | post[bit][digit];
        }
    }

    std::vector<char> good(signature_count * subset_count, 1);
    for (int current = 0; current < signature_count; ++current) {
        good[current * subset_count] = 0;
    }
    std::vector<int> removed_rounds;
    while (true) {
        std::vector<int> removed;
        for (int current = 0; current < signature_count; ++current) {
            for (int shadow_set = 1; shadow_set < subset_count; ++shadow_set) {
                const int key = current * subset_count + shadow_set;
                if (!good[key]) continue;
                bool valid = true;
                for (int digit = 0; digit < 4 && valid; ++digit) {
                    const unsigned current_targets = post[current][digit];
                    if (!current_targets) continue;
                    const unsigned shadow_targets = subset_post[shadow_set][digit];
                    if (!shadow_targets) {
                        valid = false;
                        break;
                    }
                    for (unsigned bits = current_targets; bits; bits &= bits - 1) {
                        const int target = __builtin_ctz(bits);
                        if (!good[target * subset_count + shadow_targets]) {
                            valid = false;
                            break;
                        }
                    }
                }
                if (!valid) removed.push_back(key);
            }
        }
        if (removed.empty()) break;
        for (int key : removed) good[key] = 0;
        removed_rounds.push_back(removed.size());
    }

    int good_count = 0;
    int singleton_count = 0;
    for (char value : good) good_count += value;
    for (int current = 0; current < signature_count; ++current) {
        for (int shadow = 0; shadow < signature_count; ++shadow) {
            singleton_count += good[current * subset_count + (1 << shadow)];
        }
    }
    const unsigned top_signature = 0xFF;
    const int top_index = index[top_signature];
    int universal_count = 0;
    for (int current = 0; current < signature_count; ++current) {
        universal_count += good[current * subset_count + (1 << top_index)];
    }

    std::vector<u64> phase_p_level_1{3};
    const auto phase_p_level_2 = next_level(phase_p_level_1);
    const unsigned source_signature = signature(phase_p_level_2, 12);
    bool concrete_shadow = false;
    for (u64 state : phase_p_level_1) {
        if ((state & 3) == (12 & 3)) concrete_shadow = true;
    }
    const bool abstract_shadow =
        good[index[source_signature] * subset_count + (1 << top_index)];

    if (signature_count != 12 || phase_p.edges.size() != 194
        || phase_u.edges.size() != 194 || phase_p.edges != phase_u.edges) {
        throw std::runtime_error("signature graph totals changed");
    }
    if (good_count != 47393
        || removed_rounds != std::vector<int>({147, 464, 1136})
        || singleton_count != 54 || universal_count != 12) {
        throw std::runtime_error("fixed point totals changed");
    }
    if (phase_p.profiles.size() != 448 || phase_u.profiles.size() != 441) {
        throw std::runtime_error("profile totals changed");
    }
    if (source_signature != 0x2C || !abstract_shadow || concrete_shadow) {
        throw std::runtime_error("concrete lift counterexample changed");
    }

    std::cout << "maximum_complexity=" << MAXK << '\n';
    std::cout << "phase_p_outputs=" << phase_p.outputs << '\n';
    std::cout << "phase_u_outputs=" << phase_u.outputs << '\n';
    std::cout << "total_outputs=" << phase_p.outputs + phase_u.outputs << '\n';
    std::cout << "signatures=" << signature_count << '\n';
    std::cout << "phase_p_edges=" << phase_p.edges.size() << '\n';
    std::cout << "phase_u_edges=" << phase_u.edges.size() << '\n';
    std::cout << "phase_p_profiles=" << phase_p.profiles.size() << '\n';
    std::cout << "phase_u_profiles=" << phase_u.profiles.size() << '\n';
    std::cout << "good_pairs=" << good_count << '\n';
    std::cout << "all_pairs=" << signature_count * (subset_count - 1) << '\n';
    std::cout << "removed_rounds=";
    for (std::size_t index = 0; index < removed_rounds.size(); ++index) {
        if (index) std::cout << ',';
        std::cout << removed_rounds[index];
    }
    std::cout << '\n';
    std::cout << "singleton_simulations=" << singleton_count << '\n';
    std::cout << "top_signature_simulates=" << universal_count << '\n';
    std::cout << "top_signature=1111/1111\n";
    std::cout << "concrete_source=phase-p/k2/state-12/signature-0010-1100\n";
    std::cout << "abstract_top_shadow=1\n";
    std::cout << "same_digit_previous_shadow=0\n";
    std::cout << "profiles_by_level=";
    for (const auto& [complexity, count] : phase_p.profiles_by_level) {
        std::cout << complexity << ':' << count << ',';
    }
    std::cout << '\n';
}
