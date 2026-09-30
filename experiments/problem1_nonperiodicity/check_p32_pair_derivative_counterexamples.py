#!/usr/bin/env python3

P16_LEAVES = [
    "0000010101000101","0011101111101011","0101101101111011",
    "0001010011100101","0101010110111111","0000100100100101",
    "0000001001011001","0010111001100111","0001010010001111",
    "0000011101010011","0010101110101101","0101111111011111",
    "0000110110000111","0001001111001111","0001111001111111",
    "0010111100111111",
]

P32_TERMINAL = {
    5:  "00000000001001100000010001101101",
    13: "00000001001101101001100111100001",
}

EXPECTED = {
    5: {
        "0000010011100001",
        "0000011100101101",
    },
    13: {
        "0000000100011101",
        "0001001111110101",
    },
}

def canon(s):
    return min(s[i:] + s[:i] for i in range(len(s)))

def delta2(s, shift):
    t = s[shift:] + s[:shift]
    return "".join(str(int(t[2*j]) ^ int(t[2*j+1]))
                   for j in range(len(t)//2))

def main():
    terminal16 = {canon(x) for x in P16_LEAVES}

    for portal, child in P32_TERMINAL.items():
        outputs = {canon(delta2(child, shift)) for shift in range(32)}
        assert outputs == EXPECTED[portal], (portal, outputs)
        assert outputs.isdisjoint(terminal16), (portal, outputs & terminal16)

        print("portal", portal)
        for x in sorted(outputs):
            print(" ", x, "terminating_p16=false")

    print("pair_xor_period_halving_counterexamples=2")

if __name__ == "__main__":
    main()
