# Astra automation handoff — 2026-09-24 run 256

Problem 1 remains open.

New result: the one-extra-skew analogue requested by run 255 is now exact. Assuming N-periodicity only through r-3, let b be the N-step skew of coordinate r-2, a the skew of r-1, and A_s the accumulated lower forcing from r-3. Then y_{r-2}=b, y_{r-1}=alpha_s=a XOR b A_s, and the coordinate-r forcing difference is delta_s=alpha_s(1 XOR x_{r-2}) XOR b(1 XOR x_{r-1}) XOR alpha_s b. Consequently E_r(2N;t)=b XOR the XOR of delta_q over even q<N.

At r=11,N=32 this applies unconditionally because the prefix through coordinate 8 closes in 32 steps. Exhaustive enumeration of all 4096 12-bit prefixes verifies E_11(64)=0 universally and verifies the new formula with zero mismatches. The (b,a,E) counts are 3072,512,256,256 for (0,0,0),(0,1,0),(1,0,0),(1,1,0).

On b=1, proving E_11(64)=0 is now equivalent to XOR_even[x_10(q) XOR alpha_q*x_9(q)]=1, with alpha_q=a XOR XOR_{j<q}(1 XOR x_8(j)).

Full note: proofs/informal/problem1_run256_one_extra_skew_defect.md

Next target: prove that final explicit parity identity from 32-periodicity through coordinate 8.