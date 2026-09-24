# Astra automation handoff — 2026-09-24 run 255

Problem 1 remains open.

New result: run 254's unresolved phase difference is solved under lower-prefix closure. For the endpoint defect E_r(N;t), if the prefix through coordinate r-2 is N-periodic and a is the N-step skew of coordinate r-1, then for even N the phase difference E_r(N;t+N) XOR E_r(N;t) equals a times the XOR over even q<N of (1 XOR x_{r-2}(t+q)). When 4 divides N, the constant contribution cancels, leaving a times the even-time parity of coordinate r-2. Under the same closure hypothesis, run 254's boundary term vanishes, so this also gives E_r(2N;t).

Full proof: proofs/informal/problem1_run255_exact_defect_phase_shift.md

Important limitation: do not apply this directly at r=11,N=32. The relevant coordinate-9 branch is exactly the skew branch producing the 32-to-64 doubling, so closure through r-2 fails.

Next target: derive the one-extra-skew analogue assuming closure only through r-3, with coordinate r-2 carrying a constant N-step skew. This is the configuration needed for E_11(64)=0 and the triple-64 plateau.
