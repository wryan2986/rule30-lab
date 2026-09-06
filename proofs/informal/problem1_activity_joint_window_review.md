# Adversarial review: joint windows with the original time seam (Secs 1-3)

Objective: FIND A FATAL FLAW. Result: none found; all seams
re-derived by hand below. Secs 1-2 stay `partial-proof`; Sec 3 is
correctly `inconclusive`. Problem 1 remains open. No experiment run
or admitted. This is a corollary assembling reviewed imports, not a
new compactness proof.

Source: proofs/informal/problem1_activity_joint_window_target.md,
SHA256 e82ecbf6d0a20df7eaaf941e17918cd554159609fa4841d4f29bbe0b49b2b867.
Reviewed-source hashes retained this round: staircase bound
7b7ba8f6cb378dd84b40b597327d8e3749cecfec4065f7b36603f272cae8ed01,
transport e71bf3f9aade2d2ae397c642f9dfb2d2297f3d63ee438904e4f92ec2380a42c9,
sparse codes d28e7f942e6a7380e7f3fb9927e9f3ce09d5c05be703284811768161bcbffbb3,
gate bridge (corrected)
34b9626da27a665c0541328735ba74bb95e4ffb9c5b511d117bb60d7209786ac.

## 1. Independent derivation

Sec 1. The a >= 0 extension verified exactly where it could break:
for a selected pair (j,j+1), every assigned occurrence sits at age
s >= a+j+1 >= j+1 (using a >= 0), so both indices lie in {1..s} and
the pair's terms are legitimate V_s summands -- no w_j(s<j) is ever
formed. Per age s, the pairs active there have disjoint index sets of
valid terms, so their sum is at most V_s; each pair's own interval
lies inside the common [a+2,a+W+n]. Hence pair counts sum below the
full V sum without asserting any index exists at the common
interval's earliest age. The source states exactly this. No flaw.

Sec 2. Anchored count checked: [2,2n] holds 2n-1 ages, all within
0..2n, giving (2). The sup_n J_n H_n/n condition implies R = infinity
via the n/(2n-1) >= 1/2 factor; limsup J_n/n > 0 suffices since H_n
diverges on every unbounded subsequence. Bound (4) rechecked: A^h =
pi^h T^h imported; A preserves finite bit length imported; bitlen(z)
<= 4g+2 kills pair (2n,2n+1) for n >= 2g+1 at all t >= h regardless
of bit-length parity, so J_n <= h there and J_n <= n <= 2g below;
K = 0 gives h = g = 0 with all J_n vanishing. No periodicity
inferred, no converse claimed, finite-entry compactness imported not
redone. The sparse fixed-n counterexample correctly leaves these
joint limits undecided. No flaw.

Sec 3. Target scope verified: gate-bridge citation matches the
corrected bridge (downward shift, no depth-zero pullback); J_n's
finite-cone observation is fenced against prefix campaigns; future
experiments require falsifiable full-fringe consequences. No flaw.

## 2. Falsification attempts (hand)

Tried forcing an undefined w_j(s<j) at the common interval's early
edge (a = 0, s = 2, large j): fails, each pair counts only its own
valid interval. Tried breaking (4) with odd bit length: fails, the
pair bound is parity-free. Tried deriving bounded-R from bounded-J:
fails by design, disclaimed in the source. No counterexample found.

## 3. Dependencies and exact issues

1. Reviewed imports (fidelity confirmed, not re-proved): transport
   counting bound and limit order; finite-entry decomposition with
   R(z) <= K; staircase support bitlen(z) <= 4g+2; A^h = pi^h T^h;
   harmonic divergence.
2. No machine content; nothing to verify computationally.
3. Remaining target `inconclusive` as marked: unbounded J_n or
   unbounded finite window averages for ONE FIXED ACTUAL survivor
   with the full fringe retained.

## Verdict

No fatal flaw in Secs 1-3. The a = 0 extension and the anchored
weaker sufficient condition survive as `partial-proof` corollaries;
the actual-survivor mechanism is still the bottleneck.
