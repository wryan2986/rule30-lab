#include <bits/stdc++.h>
using namespace std;

static inline uint32_t broad_child(uint32_t b, uint32_t c) {
    unsigned r = 31u - __builtin_clz(b);
    unsigned a0 = 1u ^ __builtin_parity(c >> r);

    uint32_t D = c ^ b;
    uint32_t M = ~b;

#define STEP(K) do { \
    constexpr uint32_t LO = (uint32_t)((1ULL << (K)) - 1ULL); \
    uint32_t od = D, om = M; \
    D = od ^ (om & (od << (K))); \
    M = (om & LO) | (om & (om << (K)) & ~LO); \
} while (0)

    STEP(1); STEP(2); STEP(4); STEP(8); STEP(16);
#undef STEP

    uint32_t Y = D ^ (M & (a0 ? 0xffffffffu : 0u));
    return (Y << 1) | a0;
}

static uint32_t parse_bits(const string& s) {
    uint32_t x = 0;
    for (size_t i = 0; i < s.size(); ++i)
        if (s[i] == '1') x |= 1u << i;
    return x;
}

static string bits(uint32_t x) {
    string s;
    for (int i = 0; i < 32; ++i) s.push_back('0' + ((x >> i) & 1u));
    return s;
}

static string rotmin(string s) {
    string best = s;
    for (int k = 1; k < 32; ++k) {
        string t = s.substr(k) + s.substr(0, k);
        best = min(best, t);
    }
    return best;
}

static int min_period(const string& s) {
    for (int d : {1, 2, 4, 8, 16, 32}) {
        bool ok = true;
        for (int i = 0; i < 32; ++i)
            if (s[i] != s[i % d]) { ok = false; break; }
        if (ok) return d;
    }
    return 32;
}

static pair<uint32_t,uint32_t> portal(const string& s) {
    uint16_t c = (uint16_t)parse_bits(s);
    uint32_t a = 0;
    int cur = 0;
    for (int i = 0; i < 32; ++i) {
        if (cur) a |= 1u << i;
        cur ^= (c >> (i & 15)) & 1u;
    }
    if (cur) throw runtime_error("portal integration failed");
    return {a, 0};
}

static bool is_rotation(uint32_t x, uint32_t y) {
    for (int k = 0; k < 32; ++k) {
        uint32_t z = k ? ((x >> k) | (x << (32 - k))) : x;
        if (z == y) return true;
    }
    return false;
}

struct Cert {
    int portal_index;
    const char* parent_leaf;
    uint64_t depth;
    const char* raw_target;
    const char* canonical_target;
    int parity;
    int weight;
};

static const array<Cert,16> certs = {{
    {0,"0000010101000101",1420791101ULL,"10110001110101101101011111010011","00011101011011010111110100111011",0,20},
    {1,"0011101111101011",3642025676ULL,"00101001100111010000001001000011","00000010010000110010100110011101",0,12},
    {2,"0101101101111011",1555560444ULL,"11100010010101100101111000010001","00001000111100010010101100101111",1,15},
    {3,"0001010011100101",7470817970ULL,"01111100100011101111110111010110","00011101111110111010110011111001",1,21},
    {4,"0101010110111111",15565342385ULL,"01111010100000101011100000010011","00000010011011110101000001010111",0,14},
    {5,"0000100100100101",105696243ULL,"00000000001001100000010001101101","00000000001001100000010001101101",1,9},
    {6,"0000001001011001",1255920142ULL,"01101110011001100111101000110101","00011010101101110011001100111101",0,18},
    {7,"0010111001100111",1324488168ULL,"01000100010100100010010011101000","00001000100010100100010010011101",1,11},
    {8,"0001010010001111",9124240171ULL,"10101101000100001100101010001000","00001100101010001000101011010001",0,12},
    {9,"0000011101010011",4764407279ULL,"10101111111010000100010000010110","00000101101010111111101000010001",1,15},
    {10,"0010101110101101",8857311844ULL,"11110110001101110000100001000010","00001000010000101111011000110111",0,14},
    {11,"0101111111011111",2846542716ULL,"01001000110110001101110010100100","00010010001101100011011100101001",0,14},
    {12,"0000110110000111",4421569547ULL,"10100101000111011000011100010001","00001110001000110100101000111011",0,14},
    {13,"0001001111001111",65154360ULL,"11001111000010000000100110110100","00000001001101101001100111100001",1,13},
    {14,"0001111001111111",4794122735ULL,"01010000010000000111011010111010","00000001110110101110100101000001",1,13},
    {15,"0010111100111111",4250222543ULL,"11011111111011011010100100011011","00011011110111111110110110101001",1,21}
}};

static bool verify_portal(const Cert& c) {
    auto [a,b] = portal(c.parent_leaf);
    for (uint64_t d = 0; d <= c.depth; ++d) {
        if (a == 0) {
            string raw = bits(b);
            string can = rotmin(raw);
            int par = __builtin_popcount(b) & 1;
            int wt = __builtin_popcount(b);
            int per = min_period(raw);
            cout << "portal=" << c.portal_index
                 << " depth=" << d
                 << " parity=" << par
                 << " weight=" << wt
                 << " period=" << per
                 << " raw=" << raw
                 << " canonical=" << can << "\n";
            return d == c.depth && raw == c.raw_target &&
                   can == c.canonical_target && par == c.parity &&
                   wt == c.weight && per == 32;
        }
        if (d == c.depth) break;
        uint32_t z = broad_child(a,b);
        b = a;
        a = z;
    }
    cerr << "certificate cap reached before zero return for portal "
         << c.portal_index << "\n";
    return false;
}

static int first_reset_low_half(uint32_t x) {
    uint32_t lo = x & 0xffffu;
    return lo ? __builtin_ctz(lo) : 16;
}

static void verify_structural_summary() {
    map<int, vector<pair<int,int>>> groups;
    int odd = 0, even = 0;
    for (const auto& c : certs) {
        auto [x,z] = portal(c.parent_leaf);
        (void)z;

        uint32_t y1 = broad_child(x, 0);
        if (y1 != 0xffffffffu)
            throw runtime_error("first portal lift is not all ones");

        uint32_t y2 = broad_child(y1, x);
        if (!is_rotation(y2, x))
            throw runtime_error("two-lift portal normalization failed");

        groups[first_reset_low_half(x)].push_back({c.portal_index,c.parity});
        if (c.parity) ++odd; else ++even;
    }

    if (odd != 8 || even != 8)
        throw runtime_error("root parity split is not 8/8");

    cout << "root_parity_split odd=" << odd << " even=" << even << "\n";
    for (auto& [r, v] : groups) {
        bool has0=false, has1=false;
        cout << "half_reset=" << r << " portals=";
        for (auto [idx,p] : v) {
            cout << idx << (p ? "O" : "E") << ",";
            has0 |= (p==0);
            has1 |= (p==1);
        }
        cout << " mixed=" << (has0 && has1 ? 1 : 0) << "\n";
    }
}

int main(int argc, char** argv) {
    verify_structural_summary();

    if (argc < 2 || string(argv[1]) == "--list") {
        for (const auto& c : certs)
            cout << c.portal_index << " depth=" << c.depth
                 << " parity=" << (c.parity ? "odd" : "even") << "\n";
        return 0;
    }

    string arg = argv[1];
    if (arg == "--all") {
        atomic<int> failures{0};
        vector<thread> workers;
        for (const auto& c : certs) {
            workers.emplace_back([&c,&failures]{
                if (!verify_portal(c)) ++failures;
            });
        }
        for (auto& t : workers) t.join();
        return failures.load() ? 2 : 0;
    }

    int idx = stoi(arg);
    if (idx < 0 || idx >= 16) return 3;
    return verify_portal(certs[(size_t)idx]) ? 0 : 4;
}
