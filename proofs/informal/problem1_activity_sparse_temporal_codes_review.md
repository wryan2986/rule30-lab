# Adversarial review: sparse temporal codes (Secs 1-4)

Objective: FIND A FATAL FLAW. Result: none found; all identities,
counting bounds, and limit orders re-derived by hand below. Secs 1-4
stay `partial-proof`. The file refutes only the NECESSITY of the
transport density criterion on general inputs; sufficiency stands and
no actual survivor claim is made. Problem 1 remains open. No machine
code or experiment run: the 16-symbol-pair g identity is re-derived
from two direct cell equations by hand, which suffices.

Source: proofs/informal/problem1_activity_sparse_temporal_codes.md,
SHA256 d28e7f942e6a7380e7f3fb9927e9f3ce09d5c05be703284811768161bcbffbb3.

## 1. Independent derivation

Sec 1. Triangular identity (2) re-proved: bit_i(Ay) XOR y_{i+2} uses
only lower bits, and the induction step's OR terms sit strictly below
the new top bit, so the top input bit keeps coefficient one. Decoding
order confirmed: b_t's low bit fixes x_{2t} given earlier bits, its
high bit then fixes x_{2t+1}. First-M-symbols biject first-2M-bits
compatibly, giving a clopen cylinder correspondence, i.e. a genuine
homeomorphism with shift conjugacy (1). The triangular Boolean fact is
an IMPORT (same shape as the staircase lemma); the complete temporal
code, its inversion, and the conjugacy are NEW and clearly separate.
The Delta disclaimer is accurate. No flaw.

Sec 2. g re-derived from the two low-bit cell equations: with A^t x
low bits (alpha_0, alpha_1, r, s), the next step gives
beta_0 = r XOR (alpha_1 OR alpha_0) and
beta_1 = s XOR (r OR alpha_1); inversion yields exactly the stated r
and s, using OR-symmetry for the first. Commutation A^t pi^n =
pi^n A^t gives (Phi^n b)_t = (u_{2n}(t), u_{2n+1}(t)), hence the exact
equality (4). Inequality (5) holds by contrapositive with g(0,0) = 0:
an all-zero length-(n+1) window maps to zero. Density honesty kept: no
lower bound or equality claimed. Rationality (6) verified both ways:
forward via at most 2^{a+p} tail-periodic rows; converse via Phi as a
self-map of at most 4^{h+ell} onset-h period-ell words, whose n-orbit
is exactly the spatial digit pairs. Both arguments consume GIVEN
periodic descriptions; nothing is inferred from a prefix. No flaw.

Sec 3. Sparse family verified: powers-of-two indicator has infinitely
many ones and unbounded zero gaps, hence irrational by (6) (both
eventually-periodic cases excluded). Density bound rechecked: m powers
in a W-window are consecutive, span 2^k(2^{m-1}-1) >= 2^{m-1}-1 with
k >= 0, so m <= 1+log_2 W uniformly in the window start; prefix adds
at most M. Summed (5) gives C_n <= (n+1)(M+1+floor log_2 W), and the
fixed-n sup_a-then-limsup order yields (7) exactly. Unbounded activity
(8) follows from reviewed finite E_K plus A-invariance: a bounded
orbit in a finite set is eventually periodic, contradicting the code
via (1). The refutation target is precisely the necessity implication
on general 2-adic inputs, and its scope is correctly fenced off from
any actual-survivor statement. No flaw.

Sec 4. Cylinder extension verified: even-length enlargement stays
inside the cylinder, Theta-prefix bijection preserves the bits, sparse
tail keeps irrationality and density bounds. Observed-branch matching
rests on the established finite input-cylinder precision (import).
Non-assertions explicit: no future-fringe obedience, no forced
survivor, no equality test. The fixed-n versus joint (n,W) growth
distinction is accurate commentary, and (5) of the transport note is
untouched. Remaining actual-survivor use correctly `inconclusive`.
No flaw.

## 2. Falsification attempts (hand)

Tried breaking the decoding order via OR-nonlinearity: fails, only
XOR-with-top-bit plus lower dependence is used. Tried a uniform
window-start counterexample to the log bound: fails by the span
argument with k >= 0. Tried making E_K-invariance circular with the
code: fails, invariance is an imported reviewed theorem and the
contradiction flows one way. Tried promoting the family to an actual
survivor objection: fails, Sec 4 forbids exactly this. No
counterexample found.

## 3. Dependencies and exact issues

1. Reviewed imports (fidelity confirmed, not re-proved): A triangular
   cell shape; pi-A commutation; finite E_K with A-invariance;
   finite input-cylinder precision; odd-harmonic divergence.
2. No machine verification needed or run; the only finite content is
   the 16-pair g inversion re-derived above by hand.
3. Open and correctly fenced: density strictness on general inputs was
   decided HERE (necessity refuted); what remains unproved is the
   actual full-fringe / joint-window hypothesis for the coupled
   survivor (`inconclusive`). A-trace conjugacy explorations beyond
   this verdict belong to the lead's parallel track.

## Verdict

No fatal flaw in Secs 1-4. The sparse-code refutation of density
necessity survives as `partial-proof`; transport sufficiency and the
finite-window inequality are unaffected, and the actual-survivor
question is exactly where it was.
