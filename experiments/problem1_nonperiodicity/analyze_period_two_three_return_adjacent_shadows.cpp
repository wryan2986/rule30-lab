#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

namespace {
using u128 = unsigned __int128;
constexpr int MAXIMUM_COMPLEXITY = 25;
constexpr int SCHEDULE_CAP = 64;
constexpr std::array<int, 4> GAPS{2, 3, 4, 5};

u128 forward_generator(char name, u128 state) {
    const u128 stepped = state ^ ((state << 1) | (state << 2));
    if (name == 't') return stepped;
    if (name == 'u') return stepped ^ 1;
    if (name == 'p') return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    throw std::invalid_argument("unknown generator");
}

int bit_length(std::uint64_t value) {
    return value == 0 ? 0 : 64 - __builtin_clzll(value);
}

struct Schedule {
    std::uint64_t bits = 0;
    std::uint8_t length = 0;
};

Schedule forced_zero_schedule(std::uint64_t initial) {
    u128 state = initial;
    Schedule schedule;
    for (int step = 0; step < SCHEDULE_CAP; ++step) {
        const unsigned residue = static_cast<unsigned>(state & 15);
        char branch;
        if (residue == 7) branch = 'u';
        else if (residue == 11) branch = 't';
        else return schedule;
        state = forward_generator(
            branch,
            forward_generator('p', (state - 3) >> 2)
        );
        schedule.bits = (schedule.bits << 1) | (branch == 'u');
        ++schedule.length;
    }
    throw std::runtime_error("forced schedule reached safety cap");
}

struct PrefixKey {
    std::uint64_t bits;
    std::uint8_t length;
    bool operator==(const PrefixKey& other) const {
        return bits == other.bits && length == other.length;
    }
};

struct PrefixHash {
    std::size_t operator()(const PrefixKey& key) const noexcept {
        std::uint64_t value = key.bits ^ (std::uint64_t{key.length} << 57);
        value ^= value >> 30;
        value *= 0xbf58476d1ce4e5b9ULL;
        value ^= value >> 27;
        value *= 0x94d049bb133111ebULL;
        value ^= value >> 31;
        return static_cast<std::size_t>(value);
    }
};

PrefixKey prefix_key(const Schedule& schedule, int end) {
    return {
        schedule.bits >> (schedule.length - end),
        static_cast<std::uint8_t>(end),
    };
}

std::string decode(std::uint64_t bits, int length) {
    std::string word;
    word.reserve(length);
    for (int index = length - 1; index >= 0; --index) {
        word.push_back(((bits >> index) & 1) ? 'u' : 't');
    }
    return word;
}

bool admissible(const std::string& word) {
    return word.find("uu") == std::string::npos
        && word.find("ttttt") == std::string::npos
        && word.find("ututtu") == std::string::npos;
}

std::string return_extension(
    const std::vector<int>& gaps,
    bool include_final_u
) {
    std::string word = "u";
    for (std::size_t index = 0; index < gaps.size(); ++index) {
        word += std::string(gaps[index] - 1, 't');
        if (index + 1 < gaps.size() || include_final_u) word += 'u';
    }
    return word;
}

struct Pattern {
    std::vector<int> gaps;
    std::string target;
    std::string complete;
};

void build_patterns(
    std::vector<int>& current,
    std::vector<Pattern>& output
) {
    if (current.size() == 3) {
        const std::string target = return_extension(current, false);
        const std::string complete = return_extension(current, true);
        if (admissible(complete)) output.push_back({current, target, complete});
        return;
    }
    for (int gap : GAPS) {
        current.push_back(gap);
        build_patterns(current, output);
        current.pop_back();
    }
}

bool schedule_has_at(
    const Schedule& schedule,
    int cut,
    const std::string& target
) {
    if (cut + static_cast<int>(target.size()) > schedule.length) return false;
    for (int index = 0; index < static_cast<int>(target.size()); ++index) {
        const int shift = schedule.length - 1 - (cut + index);
        const char observed = ((schedule.bits >> shift) & 1) ? 'u' : 't';
        if (observed != target[index]) return false;
    }
    return true;
}

struct Summary {
    std::uint64_t outputs = 0;
    std::uint64_t eligible_outputs = 0;
    std::uint64_t occurrences = 0;
    std::uint64_t shadowed = 0;
    std::uint64_t violations = 0;
    std::uint64_t positive_cut_occurrences = 0;
    std::uint64_t states_with_occurrence = 0;
    int maximum_cut = 0;
};

Summary run_phase(char phase, const std::vector<Pattern>& patterns) {
    std::unordered_set<std::uint64_t> states{phase == 'p' ? 3ULL : 1ULL};
    std::unordered_set<std::uint64_t> previous_states;
    Summary summary;

    std::cout << "phase=" << phase << '\n';
    for (int complexity = 1; complexity <= MAXIMUM_COMPLEXITY; ++complexity) {
        std::unordered_set<PrefixKey, PrefixHash> previous_prefixes;
        if (complexity > 1) {
            previous_prefixes.reserve(previous_states.size() * 2);
            for (std::uint64_t state : previous_states) {
                if ((state & 3) != 3) continue;
                const Schedule schedule = forced_zero_schedule(state);
                for (int end = 0; end <= schedule.length; ++end) {
                    previous_prefixes.insert(prefix_key(schedule, end));
                }
            }
        }

        std::uint64_t level_occurrences = 0;
        std::uint64_t level_violations = 0;
        std::uint64_t level_states_with = 0;
        std::uint64_t level_eligible = 0;

        for (std::uint64_t state : states) {
            const int expected = phase == 'p' ? 2 * complexity : 2 * complexity - 1;
            if (bit_length(state) != expected) {
                throw std::runtime_error("phase frontier bit-length law failed");
            }
            if ((state & 3) != 3) continue;
            ++level_eligible;
            const Schedule schedule = forced_zero_schedule(state);
            bool state_has_occurrence = false;

            for (int cut = 0; cut <= schedule.length; ++cut) {
                const PrefixKey key = prefix_key(schedule, cut);
                const std::string base = decode(key.bits, cut);
                for (const Pattern& pattern : patterns) {
                    if (!schedule_has_at(schedule, cut, pattern.target)) continue;
                    if (!admissible(base + pattern.complete)) continue;
                    state_has_occurrence = true;
                    ++level_occurrences;
                    ++summary.occurrences;
                    if (cut > 0) ++summary.positive_cut_occurrences;
                    summary.maximum_cut = std::max(summary.maximum_cut, cut);
                    if (complexity > 1 && previous_prefixes.count(key)) {
                        ++summary.shadowed;
                    } else {
                        ++level_violations;
                        ++summary.violations;
                    }
                }
            }
            if (state_has_occurrence) {
                ++level_states_with;
                ++summary.states_with_occurrence;
            }
        }

        summary.outputs += states.size();
        summary.eligible_outputs += level_eligible;
        if (level_occurrences || level_violations) {
            std::cout << "level=" << complexity
                      << " outputs=" << states.size()
                      << " eligible=" << level_eligible
                      << " previous_prefixes=" << previous_prefixes.size()
                      << " occurrences=" << level_occurrences
                      << " states_with_occurrence=" << level_states_with
                      << " violations=" << level_violations << '\n';
        }

        if (complexity < MAXIMUM_COMPLEXITY) {
            previous_states = states;
            std::unordered_set<std::uint64_t> next;
            next.reserve(states.size() * 3);
            for (std::uint64_t state : states) {
                const std::uint64_t stepped = state ^ ((state << 1) | (state << 2));
                next.insert(stepped);
                next.insert(stepped ^ 1);
                if ((state & 1) == 0) next.insert(stepped ^ 3);
            }
            states.swap(next);
        }
    }

    std::cout << "phase_outputs_checked=" << summary.outputs << '\n';
    std::cout << "phase_eligible_outputs=" << summary.eligible_outputs << '\n';
    std::cout << "phase_three_return_occurrences=" << summary.occurrences << '\n';
    std::cout << "phase_shadowed_occurrences=" << summary.shadowed << '\n';
    std::cout << "phase_shadow_violations=" << summary.violations << '\n';
    std::cout << "phase_positive_cut_occurrences="
              << summary.positive_cut_occurrences << '\n';
    std::cout << "phase_maximum_cut=" << summary.maximum_cut << '\n';
    std::cout << "phase_states_with_occurrence="
              << summary.states_with_occurrence << '\n';
    return summary;
}
}  // namespace

int main() {
    std::vector<Pattern> patterns;
    std::vector<int> current;
    build_patterns(current, patterns);
    std::cout << "maximum_complexity=" << MAXIMUM_COMPLEXITY << '\n';
    std::cout << "admissible_three_return_patterns=" << patterns.size() << '\n';

    const Summary p = run_phase('p', patterns);
    const Summary u = run_phase('u', patterns);

    const std::uint64_t total_outputs = p.outputs + u.outputs;
    const std::uint64_t total_eligible = p.eligible_outputs + u.eligible_outputs;
    const std::uint64_t total_occurrences = p.occurrences + u.occurrences;
    const std::uint64_t total_shadowed = p.shadowed + u.shadowed;
    const std::uint64_t total_violations = p.violations + u.violations;
    const std::uint64_t total_positive =
        p.positive_cut_occurrences + u.positive_cut_occurrences;

    std::cout << "total_outputs_checked=" << total_outputs << '\n';
    std::cout << "total_eligible_outputs=" << total_eligible << '\n';
    std::cout << "total_three_return_occurrences=" << total_occurrences << '\n';
    std::cout << "total_shadowed_occurrences=" << total_shadowed << '\n';
    std::cout << "total_shadow_violations=" << total_violations << '\n';
    std::cout << "total_positive_cut_occurrences=" << total_positive << '\n';
    std::cout << "maximum_cut=" << std::max(p.maximum_cut, u.maximum_cut) << '\n';

    if (patterns.size() != 56
        || p.occurrences != 1794
        || u.occurrences != 1601
        || total_occurrences != 3395
        || total_shadowed != total_occurrences
        || total_violations != 0
        || total_positive != 898) {
        throw std::runtime_error("unexpected adjacent-shadow census");
    }
    return 0;
}
