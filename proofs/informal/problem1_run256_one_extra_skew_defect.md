# Problem 1 — run 256: one-extra-skew defect formula

Problem 1 remains open.

Let E_r(N;t) be the run-253 endpoint defect. Assume N is even and the prefix through coordinate r-3 is N-periodic. Put b=x_{r-2}(t+N) XOR x_{r-2}(t), a=x_{r-1}(t+N) XOR x_{r-1}(t), and A_s=XOR_{q<s}(1 XOR x_{r-3}(t+q)). Then block differences satisfy y_{r-2}(s)=b and y_{r-1}(s)=alpha_s=a XOR b A_s.

Writing u_s=x_{r-1}(t+s), w_s=x_{r-2}(t+s), the Rule-30 OR forcing difference is exactly

delta_s = alpha_s(1 XOR w_s) XOR b(1 XOR u_s) XOR alpha_s b.

For even N, summing the y_r recurrence over a block gives

E_r(N;t+N) XOR E_r(N;t) = XOR over even q<N of delta_q.

The endpoint terms cancel even with b nonzero because each contributes the same b. Run 254's dyadic boundary term is now exactly b, hence

E_r(2N;t) = b XOR (XOR over even q<N of delta_q).

This is the exact one-extra-skew analogue requested by run 255.

For r=11,N=32, the prefix through coordinate 8 is 32-periodic for every 12-bit initial prefix, so the theorem applies unconditionally. Exhaustive enumeration of all 4096 prefixes gives E_11(64;0)=0 in every case, with zero mismatches to the formula. The (b,a,E) census is:
(0,0,0): 3072
(0,1,0): 512
(1,0,0): 256
(1,1,0): 256.

Thus the 64-step transport identity is universal at width 11 and does not select a coordinate-10 skew class.

On the important b=1 branch (N=32 divisible by 4), the formula simplifies to

E_11(64) = 1 XOR XOR_{even q<32}[ x_10(q) XOR alpha_q x_9(q) ],

where alpha_q = a XOR XOR_{j<q}(1 XOR x_8(j)).

Therefore proving E_11(64)=0 on the doubling branch is equivalent to the explicit parity identity

XOR_{even q<32}[x_10(q) XOR alpha_q x_9(q)] = 1.

Next target: derive this final parity identity from 32-periodicity through coordinate 8. All upper dependence is now compressed to a,b and the accumulated lower forcing A_q.
