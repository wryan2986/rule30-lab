# Problem 1: blind-visit rank and finite-basin ambiguity collapse

Status: exact observer theorem plus exact finite-basin censuses. Problem 1
remains OPEN.

## 1. Exact ambiguity cube of an unlabeled quotient orbit

Fix stack depth r.  Let

    R_0,R_1,...,R_(p-1)

be one aligned cyclic state orbit of the normalized quotient M_r, and suppose
it is realizable by at least one binary driver w.

At phase s there are only two candidate transitions,

    T_0(R_s), T_1(R_s).

If R_s is nonblind, these two states are distinct, so the prescribed next
state R_(s+1) determines w_s uniquely.

If R_s is blind, the two transitions coincide, so either value of w_s gives
the same next state.

Therefore, if the orbit contains exactly k blind phases, then

    boxed:
    exactly 2^k aligned binary driver words realize the same unlabeled orbit.

The choices at distinct blind phases are independent.

After imposing odd driver parity:

* if k=0, there is either zero or one odd realization;
* if k>=1, exactly 2^(k-1) odd realizations remain.

For an actually observed odd driver define

    k_r(w) = number of blind phases in its M_r orbit,

and

    u_r(w) = max(k_r(w)-1,0).

Then u_r is exactly the GF(2) dimension of the remaining aligned odd-driver
ambiguity after observing the entire unlabeled M_r orbit.

This is a stronger interpretation of "blind state": it is literally one
unresolved driver bit.

## 2. Blind sets are nested with observer depth

The projective maps satisfy

    pi_r T_w^(r+1) = T_w^r pi_r.

Hence, if an (r+1)-layer state is blind, its r-layer projection is also
blind.  For every fixed driver and temporal phase,

    blind at depth r+1 => blind at depth r.

Thus the blind phase sets satisfy

    B_(r+1)(w) subset B_r(w),

and

    k_(r+1)(w) <= k_r(w),
    u_(r+1)(w) <= u_r(w).

Each temporal phase therefore has a well-defined visibility depth: it stays
blind for an initial spatial interval and, once visible, can never become
blind again.

The extension bit Q+ from run 23 identifies the exact exit event from this
nested filtration:

    Q+=0 -> the phase remains blind one more layer,
    Q+=1 -> the phase becomes visible at the new layer.

This converts hidden-label transport into a monotone rank filtration rather
than an ever-growing opaque stack.

## 3. Complete period-16 terminating set versus the ambient odd language

For the complete set of sixteen terminating p16 leaves, the maximum k_r over
all leaves is

| r | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| max k_r on p16 leaves | 8 | 8 | 4 | 2 | 1 | 1 | 1 | 1 |

Therefore every terminating p16 leaf has

    u_r=0

by depth

    boxed: r=5.

In other words, its complete unlabeled M_5 orbit plus the known odd parity
already determines the aligned driver uniquely among ALL possible labelings
of that same state orbit.

For comparison, exhaustive enumeration of all 2,048 odd p16 necklaces gives

| r | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| max k_r on all odd p16 necklaces | 8 | 8 | 4 | 2 | 2 | 2 | 2 | 1 |

So the ambient odd language does not reach u_r=0 uniformly until r=8.

This is an exact finite demonstration of the finite-basin restriction we were
looking for: terminating ancestry collapses hidden-label ambiguity three
layers earlier than oddness alone at period 16.

It is distinct from the run-22 root-separation statement.  At r=4 the sixteen
terminating leaves already have sixteen distinct quotient orbits, but one of
those leaf orbits still has k=2 and therefore admits an alternative odd
labeling outside the terminating leaf set.  Run 24 measures ambiguity against
the whole aligned driver cube, not merely collisions inside the finite leaf
set.

## 4. Certified period-32 terminating leaves

Combining the exact singleton roots, the exact portal-10 descendants, the
complete portal-11 component, and other certified descendant leaves currently
gives 36 distinct terminating p32 necklaces.

This is only a certified subset because the full p32 tree is not complete.

On these 36 leaves the maximum blind counts are

| r | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| max k_r | 14 | 14 | 6 | 3 | 3 | 2 | 1 | 1 | 1 | 0 |

Thus every currently certified p32 leaf has odd-label ambiguity rank zero by

    r=7,

and every one is completely nonblind by

    r=10.

The 36 certified p32 leaves also have pairwise distinct M_1 unlabeled orbits.
That striking shallow separation is finite evidence only; it is not asserted
for the unknown remaining p32 leaves.

## 5. Candidate finite-support charge

The nested blind sets suggest a more precise resource than raw observer state
count.

For phase s define its visibility depth nu_s as the number of initial stack
depths for which it remains blind.  Then exactly

    k_r = #{s : nu_s >= r}.

Therefore

    sum_r k_r = sum_s nu_s

whenever the quantities are finite.

After using the one global odd-parity constraint for free, u_r=max(k_r-1,0)
is the exact unresolved-label dimension.  A possible non-telescoping charge is

    sum_r u_r.

Unlike connector length or the signed residence ledger, this quantity counts
how long independent hidden driver bits remain unresolved in the spatial
extension tower.

No support bound is proved here.  Raw local states have arbitrarily long blind
towers by run 23, so any bound on this charge must use finite-core/root-basin
ancestry.  But the complete p16 comparison shows that such ancestry genuinely
reduces the rank filtration, rather than merely reducing a convenient sample.

## 6. Next target

The next proof-relevant question is now concrete:

> Can sum_r u_r, or the visibility depths nu_s that generate it, be charged
> to a finite resource of the original survivor / portal ancestry?

The eight-state blind automaton from run 23 gives the local spatial evolution;
run 24 identifies exactly what has to be bounded globally.

A successful charging theorem need not reconstruct the whole projective stack.
It only needs to bound persistence of more than one simultaneously blind
driver bit.

Reproducer:

    experiments/problem1_nonperiodicity/analyze_blind_visit_rank.py

Atomic record:

    results/problem1/20261002_blind_visit_rank.json

Dependencies:

    problem1_blind_label_extension_delay.md
    problem1_portal_multilift_phase_quotient.md
    problem1_p16_zero_return_graph_complete.md
    problem1_period32_portal11_complete.md
