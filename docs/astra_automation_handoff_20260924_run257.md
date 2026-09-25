# Astra automation handoff — 2026-09-24 run 257

Problem 1 remains open.

Run 257 eliminates x_9 and x_10 from the final b=1 parity target left by run 256.

Define h_s=x_10(s) XOR alpha_s*x_9(s), g_s=x_8(s) OR x_7(s), with alpha_{s+1}=alpha_s XOR 1 XOR x_8(s). Exact Boolean expansion gives

    h_{s+1} XOR h_s = (1 XOR alpha_s) g_s.

For a 32-block,

    XOR_{even q<32} h_q
      = XOR_{s<30, s mod 4 in {0,1}} (h_{s+1} XOR h_s).

Therefore the run-256 target is equivalent to

    XOR_{s<30, s mod 4 in {0,1}}
      (1 XOR alpha_s)(x_8(s) OR x_7(s)) = 1.

This involves only the closed lower orbit through coordinate 8 plus alpha. Exhaustive enumeration of all 4096 12-bit prefixes confirms it on all 512 b=1 states, with 256 each for a=0 and a=1. Since b=XOR_{s<32}(x_8 OR x_7)=1, the remaining proof target is a lower-orbit weighted parity identity.

Full note: proofs/informal/problem1_run257_upper_coordinate_elimination.md

Next target: exploit the selector s mod 4 in {0,1} via 2-step/4-step telescoping, and prove analytically that the weighted parity is independent of alpha_0=a and equals b=1 on the relevant 32-periodic lower orbit.
