# Problem 1 run 206 — exact doubling defect identity for the A-map

Status: `proved structural identity`; Problem 1 remains OPEN.

Continue only the corrected run-193--205 chain. Run 205 showed that an absolute diagonal bound on `tau(2^n x)` is false and that the increment condition `a_n>a_(n-1)` must be used. This note derives an exact one-bit-extension identity for the reviewed scan map.

## Identity

Recall

    A(q) = (q>>2) XOR ((q>>1) OR q).

Write `q_i` for bit `i` of `q`. Then for every finite nonnegative integer `q`,

    A(2q) = 2 A(q) XOR epsilon(q),

where

    epsilon(q) = q_0 XOR q_1 in {0,1}.

### Proof

For output bits `i>=1`, shifting the input by one simply shifts the local Boolean rule by one, so

    bit_i(A(2q)) = bit_(i-1)(A(q)).

Thus `A(2q)` and `2A(q)` agree in every bit `i>=1`. At bit zero,

    bit_0(A(2q))
      = bit_2(2q) XOR (bit_1(2q) OR bit_0(2q))
      = q_1 XOR (q_0 OR 0)
      = q_1 XOR q_0.

Since `bit_0(2A(q))=0`, the claimed identity follows.

Equivalently, doubling commutes with one A-step except for a single possible defect at the newly exposed least-significant cell.

## Exact trajectory consequence

Let `q_k=A^k(q)` and let `Q_k=A^k(2q)`. If

    epsilon(q_j)=0  for 0<=j<r,

then induction gives

    Q_j = 2 q_j  for 0<=j<=r.

Therefore the doubled and undoubled A-orbits remain exact shifted copies until the first time the undoubled orbit has unequal low two bits. At that first time, the only newly injected discrepancy is the least-significant bit.

This is the exact one-bit-extension mechanism requested by the run-205 handoff. It also explains why no global equality `tau(2q)=tau(q)` holds: a low-bit defect can be injected before cycle entry and subsequently propagate through the nonlinear A dynamics.

## Relation to the shift tower

For the run-202 sequence

    a_n = tau(2^n x),

the comparison between levels `n` and `n-1` is therefore not arbitrary. Put `q=2^(n-1)x`. The `n`-level orbit starts as the doubled `(n-1)`-level orbit and can separate from it only at a time `j` for which

    bit_0(A^j q) != bit_1(A^j q).

Because `q` initially has `n-1` trailing zeros, this gives a concrete low-trace event whose timing controls the first possible loss of synchronization between adjacent tower levels.

This is not yet an iff criterion for `a_n>a_(n-1)`: after the first defect, the two finite-state trajectories can resynchronize or enter cycles at unrelated later times. Do not infer an increment theorem without controlling that post-defect evolution.

## Bounded sanity check

For `x=1`, the first large jump in the shift tower occurs from `a_8=2` to `a_9=5`. Taking `q=2^8`, the low-bit defect sequence `epsilon(A^j q)` begins

    0,0,0,0,1,...

so adjacent levels remain exact doubled copies for four A-steps and first separate at the fifth state. This is consistent with the identity and illustrates that the defect timing carries information absent from width alone.

## Consequence / next target

The run-205 increment problem can now be attacked through a precise object: the binary defect trace

    epsilon(A^j(2^(n-1)x)).

A useful next theorem would connect a positive renewal

    a_n > max(a_(n-1), b+n)

to a constrained first-defect or post-defect pattern, then use the existing complete-code / erasing-history machinery to rule out infinitely many such patterns for a finite seed. The immediate missing step is control after the first injected low-bit discrepancy.

Dependencies: `problem1_run202_finite_fringe_shift_tower_reduction.md`, `problem1_run203_shift_tower_renormalization.md`, `problem1_run205_run203_sufficient_bound_refuted.md`, and the reviewed definition of `A`.
