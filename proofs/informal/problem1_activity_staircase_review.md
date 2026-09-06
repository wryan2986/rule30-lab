# Adversarial review: activity staircase bound (Secs 1-5)

Objective: FIND A FATAL FLAW. Result: none found in Secs 1-5; all seams,
quantifiers, and finite-to-infinite steps re-derived by hand below.
Secs 1-5 stay `partial-proof` (lead-derived, independently re-derived
here, no machine check). Sec 6 is out of scope (marked `inconclusive`
there). Problem 1 remains open. No experiment run or admitted census
touched; hand controls only.

Source: proofs/informal/problem1_activity_staircase_bound.md,
SHA256 7b7ba8f6cb378dd84b40b597327d8e3749cecfec4065f7b36603f272cae8ed01.
Base checkpoint f6f062d5f36d6403c8d0de2dce773b60ada4a5d8 per source header.

## 1. Independent derivation, Section by section

Sec 1. A(x) = pi(T(x)) expands bit-wise to
bit_i(Ay) = y_{i+2} XOR (y_{i+1} OR y_i), giving (1) and the displayed
A formula; shift distributes over XOR/OR, verified term by term.
Bit-length nonincrease plus bit_{B-1}(Ay) = 0 XOR (0 OR 1) = 1 gives exact
preservation of length and highest one, hence the top pair (2n,2n+1) holds
a one at every t, and positions >= 2n+2 stay zero. n = 0 case: T^t(x) has
bit length <= 2 + 2t, so bit_{2s} with s >= 1, t <= s-1 always reads past
the top: V_s = 0 at every age, as claimed. Decomposition (2) re-derived
via reviewed pi A = A pi (hence A^r pi^j = pi^j A^r and
bit_0(A^{s-j} pi^j x) = bit_{2j}(A^{s-j} x)); terms j >= n+1 vanish since
pi^{n+1}(x) = 0; all w_j use nonnegative times for s >= n. No flaw.

Sec 2. Rectangle fact re-derived with index ranges: from (1) at i,
u_{i+2}(t) = u_i(t+1) on [tau, tau+L-2]; then (1) at i+1 gives u_{i+3}
on the same shortened interval. Lemma OR-step verified: the staggered
ages make u_{2j}(tau_s+1) and u_{2j+2}(tau_s) the exact LHS and first RHS
term of (1), forcing the adjacent pair to zero. Iteration count exact:
the k-th application (k = 1..n-j) acts on length L-(k-1) >= 2, so the
stated L >= 2 precondition is never violated; one time survives.
tau = S-j-1 >= 0 uses S >= n+1. j = n needs zero iterations and the
contradiction is immediate (top pair zero at tau = S-n-1 >= 0). No flaw.

Sec 3. Packing verified: pairs {n,n+1}, {n-2,n-1}, ... are disjoint with
lengths exactly 1,3,...,2 r_max+1 for r_max = floor((n-1)/2) (checked
n = 1..4 by hand). Sub-blocks start at >= S >= n+1, so the Lemma applies
to each; w_{n+1} = 0 needs s >= n+1, satisfied; dropped w_1 (if any) is
nonnegative. Floor-partition drops only the remainder. (3) to (4): finite
fixed sum, floor(W/L)/W -> 1/L, and sup >= every window mean. The claim
"logarithmic growth with support size, not with age" is accurate and the
text does not overclaim fixed-row age growth. No flaw.

Sec 4. Contrapositive exact: n >= 2g(K)+1 gives
r_max = floor((n-1)/2) >= g(K), contradicting R <= K via (4). g(0) = 0
since H_odd(0) = 1 > 0; bit-length bound 2 matches E_0. Witness interval:
needs pairs down to j = n-2g >= 1, i.e. exactly n >= 2g+1; the average
argument W delta_K > g(K)+1 is equivalent to W_K as defined. Controls
recomputed by hand: 27 has B = 5, n = 2, bound H_odd(0) = 1 <= R = 1;
111 has B = 7, n = 3, bound H_odd(1) = 4/3 <= R = 2; K = 1 gives g = 1,
delta = 1/3, W = 7. All consistent. Sharpness correctly disclaimed. No flaw.

Sec 5. Decomposition import confirmed VERBATIM against effective-levels
Sec 2 (same formula, same s >= h domain, same z = pi^h(y)). The R(z) <= K
step is valid: early terms are bits (nonnegative), so V_r(z) <= V_{h+r}(x)
for every r >= 0 including r = 0. Support seam exact: y = (y mod 2^{2h}) +
2^{2h} z, covering z = 0 and z > 0. Integral estimates rechecked:
decreasing integrand gives H_odd(r) >= (1/2) log(2r+3), hence the stated
exp bounds. Enumeration soundness note: completeness over the finite
candidate set uses unitriangularity of T (unique low-to-high preimage);
this dependency is implicit in the source and is flagged in Sec 4 below
rather than assumed silently. The "proved bound, NOT a census" hedge is
proper. No flaw.

## 2. Falsification attempts (hand)

Tried to break the Lemma at n = 1, where it forces u_2(t) = 1 for all
t >= 1: x = 8 gives orbit 8 -> 14 -> 12 <-> 13 with u_2 = 1 throughout;
x = 4 gives 4 -> 7 -> 6 with u_2 = 1 throughout. Both confirm rather than
refute. Tried to break (3) via 27 (R = 1 forces V_s = 1 eventually under
the window lower bound): consistent, since V_s <= R = 1 squeezes the
average from both sides without contradiction. Tried simultaneous-column
variants of the Lemma: they change the time seams and are different
statements, not counterexamples. No counterexample found.

## 3. Narrow bounded verification: COMPLETED finite scope (two executions)

Two executions of the same 88 admitted cases (8 local + 16 L=2 + 64 L=3;
NO whole-row orbit replay) exist. Run 1 enforced only RLIMIT_AS and
omitted the immutable reference hash; run 2 enforces RLIMIT_AS +
RLIMIT_CPU(120) + wall alarm (120s) with explicit deadline, records the
immutable reference hash, and archives the FULL run-1 record under
superseded_prior_record. Independent implementation:
experiments/problem1_nonperiodicity/check_activity_staircase_independent.py
(direct bit arrays, cell rule upper XOR (middle OR self), stdlib only;
primary script/result never read). Record:
results/problem1/20260906_activity_staircase_independent.json.
Current script hash
991c2bf0af39734eedf0e4e6fcf8d156c27f0080c8b3394031f97cfbc376064d;
current result file hash
2920581ef2371d3301a4fd966bf3b683e829dcf484df1793caa1f1879a61d1b3;
admission hash
f577f80b21ba94576c7b8cd8248f40f801b5e01e75f8f4d9feba871f295fbfa9.
Canonical payload in BOTH runs
98e4468ef1b7f143e767c5d24c66b368876eb9888093562be65fcffbd468666d
(identical: same 88 cases). Run-1 artifacts (script
11837090674e81feb10742fd820610d01e1fcfddf06a5ee2d526c5d24b95624b,
result file
129225255ae1a23bb9f0689a55d4ffeea55e0d9e6e2bddcb43cd39612451f977)
are retained inside the run-2 archive. Counts: local 8/8, rectangle L=2
16/16, rectangle L=3 64/64, status
`finite-exhaustive` for these cones only (premise fires on the zero
cone in each family: 1/1/1 premise-true; conclusions true in 2/4/4).
Correction to the previous wording of this section: the completed
machine check verifies the finite seams; it does NOT promote Secs 1-5
beyond `partial-proof` relative to the prize problem. Verification
status (`finite-exhaustive` in the declared cone domains) and prize
status (`partial-proof`, still conditional on proof plus fresh review
for induction, packing, and limit) are distinct. No enumeration, sweep,
census, or survivor claim follows. The reviewed proof source hash
7b7ba8f6cb378dd84b40b597327d8e3749cecfec4065f7b36603f272cae8ed01
is preserved as stated in the header (pre-citation reconstruction; the
lead archives both source states).

## 4. Exact unresolved issues

1. Decomposition and finite-entry theorem are IMPORTED (reviewed
   elsewhere); fidelity confirmed, not re-proved.
2. Enumeration completeness in Sec 5 relies on T's low-to-high unique
   preimage (unitriangularity: bit_k(Ty) equals y_k XOR a function of
   strictly lower bits, so each y has exactly one preimage). The
   explicit citation sentence has now been added in the current proof
   by the lead; recorded here as discharged at source level. No logic
   gap ever attached to it.
3. Local seam machine checks are COMPLETE (`finite-exhaustive` on the
   admitted 8/16/64 cones; run-2 payload
   98e4468ef1b7f143e767c5d24c66b368876eb9888093562be65fcffbd468666d,
   unchanged from run 1). The all-depth claims of Secs 1-5 (induction,
   packing, harmonic limit) remain proof-based `partial-proof`;
   finite seam agreement does not promote them.
4. Sec 6 correctly marks the actual-survivor step `inconclusive`;
   nothing here bounds V on an infinite survivor or removes the
   finite-input premise.

## Verdict

No fatal flaw, no quantifier mismatch, no finite-to-infinite gap in
Secs 1-5. The staircase zero-propagation mechanism survives adversarial
review as `partial-proof`. The route's value is an explicit support
scale for the bounded alternative; it does not itself grow activity on
any fixed survivor.
