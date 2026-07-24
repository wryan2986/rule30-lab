#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {
using u128 = unsigned __int128;
constexpr int MAXIMUM_COMPLEXITY = 25;
constexpr int SCHEDULE_CAP = 48;
constexpr std::array<int, 4> GAPS{2, 3, 4, 5};
constexpr uint64_t KNOWN_STATE = 0x1bcd3a7b3fdfbULL;

u128 forward_generator(char name, u128 state) {
    const u128 stepped = state ^ ((state << 1) | (state << 2));
    if (name == 't') return stepped;
    if (name == 'u') return stepped ^ 1;
    if (name == 'p') return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    throw std::invalid_argument("unknown generator");
}

int bit_length(uint64_t value) {
    return value == 0 ? 0 : 64 - __builtin_clzll(value);
}

struct Schedule {
    uint64_t bits = 0;
    uint8_t length = 0;
};

Schedule forced_zero_schedule(uint64_t initial) {
    u128 state = initial;
    Schedule schedule;
    for (int step = 0; step < SCHEDULE_CAP; ++step) {
        const unsigned residue = static_cast<unsigned>(state & 15);
        char branch;
        if (residue == 7) branch = 'u';
        else if (residue == 11) branch = 't';
        else return schedule;
        const u128 tail = (state - 3) >> 2;
        state = forward_generator(branch, forward_generator('p', tail));
        schedule.bits = (schedule.bits << 1) | (branch == 'u' ? 1 : 0);
        ++schedule.length;
    }
    throw std::runtime_error("forced zero schedule reached cap");
}

struct PrefixKey {
    uint64_t bits;
    uint8_t length;
    bool operator==(const PrefixKey& other) const {
        return bits == other.bits && length == other.length;
    }
};
struct PrefixHash {
    std::size_t operator()(const PrefixKey& key) const {
        uint64_t x = key.bits ^ (uint64_t{key.length} << 57);
        x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL;
        x ^= x >> 27; x *= 0x94d049bb133111ebULL;
        x ^= x >> 31;
        return static_cast<std::size_t>(x);
    }
};

PrefixKey prefix_key(const Schedule& schedule, int end) {
    return {schedule.bits >> (schedule.length - end), static_cast<uint8_t>(end)};
}

std::string decode_prefix(uint64_t bits, int length) {
    std::string word;
    word.reserve(length);
    for (int i = length - 1; i >= 0; --i) {
        word.push_back(((bits >> i) & 1) ? 'u' : 't');
    }
    return word;
}

bool locally_admissible(const std::string& word) {
    return word.find("uu") == std::string::npos
        && word.find("ttttt") == std::string::npos
        && word.find("ututtu") == std::string::npos;
}

std::string target_extension(int first_gap, int second_gap) {
    return std::string("u") + std::string(first_gap - 1, 't')
        + "u" + std::string(second_gap - 1, 't');
}

bool schedule_has_at(
    const Schedule& schedule,
    int cut,
    const std::string& extension
) {
    if (cut + static_cast<int>(extension.size()) > schedule.length) return false;
    for (int i = 0; i < static_cast<int>(extension.size()); ++i) {
        const int index = cut + i;
        const int shift = schedule.length - 1 - index;
        const char observed = ((schedule.bits >> shift) & 1) ? 'u' : 't';
        if (observed != extension[i]) return false;
    }
    return true;
}

struct Candidate {
    char phase;
    int complexity;
    uint64_t state;
    int cut;
    std::string base;
    int first_gap;
    int second_gap;
    std::string full_word;
};

struct PhaseSummary {
    uint64_t outputs_checked = 0;
    uint64_t eligible_outputs = 0;
    uint64_t candidates = 0;
    int maximum_schedule = 0;
    std::vector<Candidate> examples;
};

PhaseSummary run_phase(char phase) {
    std::unordered_set<uint64_t> states;
    states.insert(phase == 'p' ? 3 : 1);
    std::unordered_map<PrefixKey, uint8_t, PrefixHash> minimum;
    PhaseSummary summary;

    std::cout << "phase=" << phase << '\n';
    for (int complexity = 1; complexity <= MAXIMUM_COMPLEXITY; ++complexity) {
        std::vector<std::pair<uint64_t, Schedule>> rows;
        rows.reserve(states.size());
        const int expected = phase == 'p' ? 2 * complexity : 2 * complexity - 1;
        for (uint64_t state : states) {
            if (bit_length(state) != expected) {
                throw std::runtime_error("frontier bit-length law failed");
            }
            if ((state & 3) != 3) continue;
            const Schedule schedule = forced_zero_schedule(state);
            rows.emplace_back(state, schedule);
            summary.maximum_schedule = std::max(
                summary.maximum_schedule, static_cast<int>(schedule.length)
            );
            for (int end = 0; end <= schedule.length; ++end) {
                minimum.emplace(prefix_key(schedule, end), complexity);
            }
        }

        uint64_t level_candidates = 0;
        for (const auto& [state, schedule] : rows) {
            for (int cut = 0; cut <= schedule.length; ++cut) {
                const PrefixKey base_key = prefix_key(schedule, cut);
                if (minimum.at(base_key) != complexity) continue;
                const std::string base = decode_prefix(base_key.bits, cut);
                for (int first_gap : GAPS) {
                    for (int second_gap : GAPS) {
                        const std::string extension =
                            target_extension(first_gap, second_gap);
                        const std::string complete = base + extension + 'u';
                        if (!locally_admissible(complete)) continue;
                        if (!schedule_has_at(schedule, cut, extension)) continue;
                        ++level_candidates;
                        ++summary.candidates;
                        if (summary.examples.size() < 8) {
                            summary.examples.push_back({
                                phase, complexity, state, cut, base,
                                first_gap, second_gap, complete,
                            });
                        }
                    }
                }
            }
        }

        summary.outputs_checked += states.size();
        summary.eligible_outputs += rows.size();
        std::cout << "level=" << complexity
                  << " distinct_outputs=" << states.size()
                  << " eligible_outputs=" << rows.size()
                  << " two_return_zero_candidates=" << level_candidates
                  << '\n';

        if (complexity != MAXIMUM_COMPLEXITY) {
            std::unordered_set<uint64_t> next;
            next.reserve(states.size() * 3);
            for (uint64_t state : states) {
                const uint64_t stepped = state ^ ((state << 1) | (state << 2));
                next.insert(stepped);
                next.insert(stepped ^ 1);
                if ((state & 1) == 0) next.insert(stepped ^ 3);
            }
            states.swap(next);
        }
    }

    std::cout << "phase_outputs_checked=" << summary.outputs_checked << '\n';
    std::cout << "phase_eligible_outputs=" << summary.eligible_outputs << '\n';
    std::cout << "phase_maximum_complete_zero_schedule_length="
              << summary.maximum_schedule << '\n';
    std::cout << "phase_two_return_zero_candidates=" << summary.candidates << '\n';
    for (const Candidate& row : summary.examples) {
        std::cout << "candidate phase=" << row.phase
                  << " complexity=" << row.complexity
                  << " state=" << row.state
                  << " cut=" << row.cut
                  << " base=" << row.base
                  << " gaps=" << row.first_gap << ',' << row.second_gap
                  << " complete_word=" << row.full_word << '\n';
    }
    return summary;
}
}  // namespace

int main() {
    std::cout << "maximum_complexity=" << MAXIMUM_COMPLEXITY << '\n';
    std::cout << "schedule_cap=" << SCHEDULE_CAP << '\n';
    const PhaseSummary p = run_phase('p');
    const PhaseSummary u = run_phase('u');
    std::cout << "total_distinct_phase_outputs_checked="
              << p.outputs_checked + u.outputs_checked << '\n';
    std::cout << "total_eligible_outputs="
              << p.eligible_outputs + u.eligible_outputs << '\n';
    std::cout << "total_two_return_zero_candidates="
              << p.candidates + u.candidates << '\n';
    if (u.examples.empty() || u.examples.front().state != KNOWN_STATE) {
        throw std::runtime_error("expected complexity-25 counterexample not found first");
    }
    return 0;
}
