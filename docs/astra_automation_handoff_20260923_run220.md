# Astra automation handoff — run 220

Problem 1 remains OPEN.

## New exact reduction and blocker

Inside a constant-period epoch P, define
\[
\theta_n=a_{n-1}\pmod P,\qquad e_n=d_n(a_{n-1}).
\]
Given the aligned eventual-cycle columns and \((\theta_n,e_n)\), the increment \(\delta_n=a_n-a_{n-1}\) is determined exactly: it is 0 when the entry bit matches the unique periodic defect phase, otherwise it is the distance to the first reset on the lower P-cycle. Hence the next stopping phase is also determined.

But this augmentation does not close. To compute
\[
e_{n+1}=d_{n+1}(a_n)
\]
by evolving across the known interval \([a_{n-1},a_n]\), one additionally needs the look-ahead bit
\[
F_n=d_{n+1}(a_{n-1}).
\]
Adding F_n merely moves the problem outward: the following transition exposes a new bit one level higher. Thus the escaping information in run 219 is precisely a moving one-bit frontier of transient defect ancestry, not an unrecorded cycle phase.

## Do not claim

Do not infer eventual periodicity of preperiod increments from the fixed-P cycle automaton. The cycle columns plus current entry bit determine the current increment but not the next entry bit without fresh frontier information.

## Next target

Study the diagonal/frontier sequence
\[
F_n=d_{n+1}(a_{n-1}).
\]
Try either (1) to derive a bounded-data reconstruction law for F_n from the defect recurrence and stopping condition, or (2) find two realizable common-origin examples with identical bounded cycle/entry state but different F_n, which would establish a genuine nonclosure theorem for bounded-state augmentations of this type.

Detailed note: `proofs/informal/problem1_run220_stopping_curve_frontier_nonclosure.md`.
