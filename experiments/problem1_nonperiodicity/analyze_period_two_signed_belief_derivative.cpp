#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

using u64 = std::uint64_t;
constexpr int MAXK = 28;
constexpr int CAP = 64;

u64 forward_generator(char g, u64 s) {
    const u64 t = s ^ ((s << 1) | (s << 2));
    if (g == 't') return t;
    if (g == 'u') return t ^ 1;
    if (g == 'p') return t ^ 1 ^ ((s & 1) == 0 ? 2 : 0);
    throw std::runtime_error("unknown generator");
}

std::vector<u64> next_level(const std::vector<u64>& current) {
    std::vector<u64> output;
    output.reserve(current.size() * 3);
    for (u64 state : current) {
        output.push_back(forward_generator('t', state));
        output.push_back(forward_generator('u', state));
        output.push_back(forward_generator('p', state));
    }
    std::sort(output.begin(), output.end());
    output.erase(std::unique(output.begin(), output.end()), output.end());
    return output;
}

bool contains(const std::vector<u64>& values, u64 target) {
    return std::binary_search(values.begin(), values.end(), target);
}

unsigned fiber_mask(
    const std::vector<std::vector<u64>>& levels, int complexity, u64 quotient
) {
    unsigned mask = 0;
    for (int digit = 0; digit < 4; ++digit) {
        if (contains(levels[complexity + 1], 4 * quotient + unsigned(digit))) {
            mask |= 1u << digit;
        }
    }
    return mask;
}

u64 mask_sequence(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 state,
    int depth
) {
    u64 result = 0;
    for (int step = 0; step < depth; ++step) {
        state >>= 2;
        result |= u64(fiber_mask(levels, complexity - 1 - step, state))
            << (4 * step);
    }
    return result;
}

bool dominates(u64 current, u64 shadow, int depth) {
    for (int step = 0; step < depth; ++step) {
        const unsigned a = (current >> (4 * step)) & 15;
        const unsigned b = (shadow >> (4 * step)) & 15;
        if (a & ~b) return false;
    }
    return true;
}

bool synchronized_or_full(u64 current, u64 shadow, int depth) {
    for (int step = 0; step < depth; ++step) {
        const unsigned a = (current >> (4 * step)) & 15;
        const unsigned b = (shadow >> (4 * step)) & 15;
        if (b != 15 && b != a) return false;
    }
    return true;
}

int defect_count(u64 shadow, int depth) {
    int result = 0;
    for (int step = 0; step < depth; ++step) {
        result += ((shadow >> (4 * step)) & 15) != 15;
    }
    return result;
}

int local_signed_factor(unsigned current, unsigned shadow) {
    if (current & ~shadow) return 0;
    return shadow == 15 ? 1 : -1;
}

int local_branching_derivative(unsigned current, unsigned shadow) {
    if (current & ~shadow) return 0;
    if (current == 15) return shadow == 15 ? 1 : 0;
    if (current == 3 || current == 11) {
        return 2 * int((shadow >> 2) & 1) - 1;
    }
    if (current == 12) {
        return 2 * int(shadow & 1) - 1;
    }
    throw std::runtime_error("zero current mask entered relevant derivative");
}

std::string forced_zero_schedule(u64 state) {
    std::string word;
    for (int step = 0; step < CAP; ++step) {
        const u64 residue = state & 15;
        char branch;
        if (residue == 7) branch = 'u';
        else if (residue == 11) branch = 't';
        else return word;
        state = forward_generator(
            branch, forward_generator('p', (state - 3) >> 2)
        );
        word.push_back(branch);
    }
    throw std::runtime_error("schedule cap reached");
}

bool admissible(const std::string& word) {
    return word.find("uu") == std::string::npos
        && word.find("ttttt") == std::string::npos
        && word.find("ututtu") == std::string::npos;
}

struct Occurrence {
    int complexity;
    int cut;
    int depth;
    u64 current;
    u64 residue;
    u64 current_sequence;
    u64 same_cylinder = 0;
    u64 dominant = 0;
    u64 synchronized = 0;
    u64 budget_three = 0;
    int minimum_defect = 999;
    long long signed_mass = 0;
};

std::vector<Occurrence> process_level(
    const std::vector<std::vector<u64>>& levels, int complexity
) {
    std::vector<Occurrence> rows;
    int maximum_depth = 0;
    std::vector<std::unordered_map<u64, std::vector<int>>> lookup(24);

    for (u64 current : levels[complexity]) {
        if ((current & 3) != 3) continue;
        const std::string schedule = forced_zero_schedule(current);
        for (int cut = 0; cut <= static_cast<int>(schedule.size()); ++cut) {
            if (schedule.compare(cut, 6, "ututut") != 0) continue;
            if (!admissible(schedule.substr(0, cut) + "utututu")) continue;
            const int depth = cut + 1;
            const u64 modulus_mask = (u64{1} << (2 * depth)) - 1;
            const int index = rows.size();
            rows.push_back(Occurrence{
                complexity,
                cut,
                depth,
                current,
                current & modulus_mask,
                mask_sequence(levels, complexity, current, depth),
            });
            lookup[depth][current & modulus_mask].push_back(index);
            maximum_depth = std::max(maximum_depth, depth);
        }
    }

    for (u64 shadow : levels[complexity - 1]) {
        u64 state = shadow;
        u64 sequence = 0;
        int defects = 0;
        for (int step = 0; step < maximum_depth; ++step) {
            state >>= 2;
            const unsigned mask = fiber_mask(
                levels, complexity - 2 - step, state
            );
            sequence |= u64(mask) << (4 * step);
            defects += mask != 15;
            const int depth = step + 1;
            const u64 residue = shadow & ((u64{1} << (2 * depth)) - 1);
            const auto found = lookup[depth].find(residue);
            if (found == lookup[depth].end()) continue;
            for (int index : found->second) {
                auto& row = rows[index];
                ++row.same_cylinder;
                if (!dominates(row.current_sequence, sequence, depth)) continue;
                ++row.dominant;
                if (!synchronized_or_full(
                        row.current_sequence, sequence, depth
                    )) {
                    continue;
                }
                ++row.synchronized;
                row.minimum_defect = std::min(row.minimum_defect, defects);
                if (defects <= 3) ++row.budget_three;
                row.signed_mass += (defects & 1) ? -1 : 1;
            }
        }
    }
    return rows;
}

long long direct_signed_mass(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 current,
    int depth
) {
    const u64 modulus_mask = (u64{1} << (2 * depth)) - 1;
    const u64 residue = current & modulus_mask;
    const u64 current_sequence = mask_sequence(levels, complexity, current, depth);
    long long result = 0;
    for (u64 shadow : levels[complexity - 1]) {
        if ((shadow & modulus_mask) != residue) continue;
        const u64 shadow_sequence = mask_sequence(
            levels, complexity - 1, shadow, depth
        );
        if (!dominates(current_sequence, shadow_sequence, depth)) continue;
        result += (defect_count(shadow_sequence, depth) & 1) ? -1 : 1;
    }
    return result;
}

int main() {
    for (unsigned current : {3u, 11u, 12u, 15u}) {
        for (unsigned shadow : {0u, 3u, 11u, 12u, 15u}) {
            if (local_signed_factor(current, shadow)
                != local_branching_derivative(current, shadow)) {
                throw std::runtime_error("local derivative identity failed");
            }
        }
    }

    std::vector<std::vector<u64>> levels(MAXK + 1);
    levels[1] = {1};
    u64 outputs = 1;
    for (int complexity = 2; complexity <= MAXK; ++complexity) {
        levels[complexity] = next_level(levels[complexity - 1]);
        outputs += levels[complexity].size();
    }

    u64 occurrences_27 = 0;
    u64 occurrences_28 = 0;
    u64 dominant_failures = 0;
    u64 synchronized_failures = 0;
    u64 signed_zeros = 0;
    u64 negative_signed = 0;
    u64 majority_failures = 0;
    std::map<int, u64> minimum_defects;
    long long minimum_absolute_signed = std::numeric_limits<long long>::max();
    Occurrence signed_witness{};
    u64 minimum_budget_count = std::numeric_limits<u64>::max();
    Occurrence budget_witness{};

    for (int complexity = 2; complexity <= MAXK; ++complexity) {
        auto rows = process_level(levels, complexity);
        if (complexity <= 27) occurrences_27 += rows.size();
        else occurrences_28 += rows.size();
        for (const auto& row : rows) {
            dominant_failures += row.dominant == 0;
            synchronized_failures += row.dominant - row.synchronized;
            signed_zeros += row.signed_mass == 0;
            negative_signed += row.signed_mass < 0;
            majority_failures += 2 * row.dominant < row.same_cylinder;
            ++minimum_defects[row.minimum_defect];
            const long long absolute = std::llabs(row.signed_mass);
            if (absolute < minimum_absolute_signed) {
                minimum_absolute_signed = absolute;
                signed_witness = row;
            }
            if (row.budget_three < minimum_budget_count) {
                minimum_budget_count = row.budget_three;
                budget_witness = row;
            }
        }
    }

    const long long cancellation = direct_signed_mass(levels, 5, 0x198, 1);

    std::cout << "maximum_complexity=" << MAXK << '\n';
    std::cout << "phase_u_outputs=" << outputs << '\n';
    std::cout << "gap_222_occurrences_through_27=" << occurrences_27 << '\n';
    std::cout << "gap_222_occurrences_at_28=" << occurrences_28 << '\n';
    std::cout << "gap_222_occurrences_total="
              << occurrences_27 + occurrences_28 << '\n';
    std::cout << "dominant_failures=" << dominant_failures << '\n';
    std::cout << "synchronized_failures=" << synchronized_failures << '\n';
    std::cout << "signed_zero_cylinders=" << signed_zeros << '\n';
    std::cout << "negative_signed_cylinders=" << negative_signed << '\n';
    std::cout << "majority_failures=" << majority_failures << '\n';
    for (const auto& [defects, count] : minimum_defects) {
        std::cout << "minimum_defect_" << defects << '=' << count << '\n';
    }
    std::cout << "minimum_absolute_signed_mass="
              << minimum_absolute_signed << '\n';
    std::cout << "minimum_budget_three_count="
              << minimum_budget_count << '\n';
    std::cout << std::hex;
    std::cout << "signed_witness_state=0x" << signed_witness.current << '\n';
    std::cout << "budget_witness_state=0x" << budget_witness.current << '\n';
    std::cout << std::dec;
    std::cout << "signed_witness_complexity=" << signed_witness.complexity
              << " cut=" << signed_witness.cut
              << " depth=" << signed_witness.depth
              << " mass=" << signed_witness.signed_mass << '\n';
    std::cout << "budget_witness_complexity=" << budget_witness.complexity
              << " cut=" << budget_witness.cut
              << " depth=" << budget_witness.depth
              << " budget_count=" << budget_witness.budget_three << '\n';
    std::cout << "nongap_cancellation_complexity_5_state_0x198_depth_1="
              << cancellation << '\n';

    if (occurrences_27 != 2989 || occurrences_28 != 2173
        || dominant_failures != 0 || synchronized_failures != 0
        || signed_zeros != 0 || minimum_defects[0] != 5159
        || minimum_defects[3] != 3 || minimum_absolute_signed != 1
        || minimum_budget_count != 1 || cancellation != 0) {
        throw std::runtime_error("signed-belief totals changed");
    }
}
