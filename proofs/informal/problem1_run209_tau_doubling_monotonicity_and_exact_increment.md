# Problem 1 run 209 — tau-doubling monotonicity and exact increment law

Status: `partial-proof`. Problem 1 remains OPEN.

This continues the corrected run-193--208 chain.

## 1. Run 208 can be sharpened

Run 207 proved, for every finite q and every k>=0,

    A^k(2q) = 2 A^k(q) XOR d_k,   d_k in {0,1}.

Because d_k occupies only bit zero, this immediately implies the exact projection identity

    floor(A^k(2q)/2) = A^k(q)                                      (1)

for every k.

This gives a universal monotonicity statement for preperiods which was not used in run 208.

## 2. Theorem: tau(2q) >= tau(q)

Let

    s_k = A^k(2q),
    r_k = A^k(q).

Suppose s is periodic from time t. Then for some period P>0,

    s_(k+P) = s_k

for all k>=t. Applying floor(/2) and using (1),

    r_(k+P) = floor(s_(k+P)/2)
            = floor(s_k/2)
            = r_k

for all k>=t. Hence r is periodic from time t. By minimality of tau(q),

    tau(q) <= t.

Taking t=tau(2q) proves

    tau(2q) >= tau(q).                                            (2)

This argument is exact and uses no FULL hypothesis.

## 3. Exact adjacent-tower increment law

Run 208 showed:

- if the eventual r-cycle has no reset, then tau(2q)<=tau(q);
- if it has a reset and the entry defect d_a agrees with the unique periodic lifted defect phase, then tau(2q)<=tau(q);
- if the entry defect is mismatched, then tau(2q)=tau(q)+rho, where rho>=1 is the distance to the first reset.

Combining those inequalities with (2) upgrades the first two cases from `<=` to equality. Therefore the complete law is

    tau(2q)-tau(q) = 0

unless the cycle-entry defect phase is mismatched, and in the mismatch case

    tau(2q)-tau(q) = rho.                                        (3)

In particular,

    tau(2q) > tau(q)

iff the run-208 reset-phase mismatch occurs. There are no negative adjacent increments.

For the shift tower

    q_n = 2^n x,
    a_n = tau(q_n),

we consequently have the exact nonnegative increment law

    a_n-a_(n-1) in {0, rho_n},                                   (4)

with the positive value occurring exactly at a reset-phase mismatch. Thus `a_n` is nondecreasing for every finite x, not merely for a tower arising in a separately assumed FULL configuration.

The late-renewal formula from run 202 remains

    R_(b+n-1) = max(a_n-max(a_(n-1),b+n),0).

Using (4), a positive late renewal is exactly a mismatch index satisfying

    a_(n-1)+rho_n > b+n.                                         (5)

## 4. Strategic correction to the run-208 next target

Run 208 suggested looking for an additional restriction supplied specifically by the FULL/global-front hypothesis on cycle-entry phases or rho_n. There is an important circularity danger here.

The finite-fringe reduction of run 202 is exact for the original finite seed: beyond its rightmost occupied site b, its entire threshold/front tail is already the tower `a_n=tau(2^n x)`. Conversely, an arbitrary finite x can itself be taken as finite initial data (up to the repository's fixed indexing convention). Therefore the tower dynamics are not an auxiliary family unrelated to the Rule-30 problem; they encode the actual far-right front thresholds of finite seeds.

FULL contributes the requirement of infinitely many indices satisfying (5). It does not, merely by being named FULL, supply an independent restriction on the same cycle-entry phases. Any proposed extra FULL phase constraint must be derived from some additional proved spacetime fact and shown not to be just a reformulation of (5).

This matters especially for x=1. The bounded observations from run 208 showing many above-diagonal renewals for x=1 are observations on the canonical single-seed tower itself, not evidence from an irrelevant generic family. They therefore make a generic eventual-mismatch-finiteness lemma particularly implausible, though of course they do not prove infinitude.

## 5. What remains useful

The exact law (3) removes one ambiguity left by run 208: adjacent zero-extension can never make tau decrease. Every plateau is precisely a phase-matched/no-reset lift, and every increase is precisely a mismatch surviving to the first reset.

The unresolved problem is still to control the *above-diagonal* positive increments, not positivity alone:

    a_(n-1)+rho_n > b+n.

A productive next step must therefore introduce genuinely new information beyond the adjacent-tower factor map itself—for example a proved relation between the reset location and the complete finite original ancestry/birth accounting. Merely restating FULL in complete-code or global-front language will not add a constraint.

Dependencies: `problem1_run207_exact_adjacent_tower_defect_automaton.md`, `problem1_run207_cycle_reset_criterion.md`, `problem1_run208_exact_tau_doubling_reset_formula.md`, `problem1_run202_finite_fringe_shift_tower_reduction.md`.