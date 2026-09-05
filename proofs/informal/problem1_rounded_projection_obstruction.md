# Rounded projection and the first schedule change

Status: `partial-proof`, exact all-depth identities and obstruction with
independent derivation and adversarial review. The proposed projection
descent is `refuted` in the precise domains below. Finite checks are
separately labelled. B_all and Problem 1 remain open.

## Strategy and admission

The ordinary projection x>>2 lowers frontier complexity, but a continuing
x is 7 or 11 modulo 16, so its projection is 1 or 2 modulo 4 and cannot
itself continue. The natural repair is

```text
R(x)=(x>>2) OR 3 = 4 floor(x/16)+3.
```

For x=16h+4d+3 this deletes the digit d and keeps the fixed root digit 3.
For finite x>=16 it lowers bit length by exactly two. The question is
whether this repaired projection can support an induction from an admissible
three-return state to a smaller ordinary frontier.

Route ranking (`heuristic`):

| Rank | Route | Plausibility / all-depth potential | Falsifiability / cost |
| --- | --- | --- | --- |
| 1 | Exact rounded-projection coupling to the forced map | High for a local identity / tests a natural descent | High / low |
| 2 | Delete a generator from an ordinary representation to construct a shadow | Unknown / could prove adjacent inclusion | High on named witnesses / medium |
| 3 | Preserve full endpoint correlations across unequal-gap returns | Unknown / could prove signed nonvanishing | Medium until specified / high |

Candidate exact table, using the established F and generator conventions:

```text
first two forced letters   x mod64   R(x) mod16
ut                         7          3 (stops)
uu                        23          7 (u)
tt                        43         11 (t)
tu                        59         15 (stops)
```

Candidate intertwining: if the first two letters agree, then
`F(R(x))=R(F(x))`. Candidate consequence: if the first change of letter
occurs after an initial constant run a^ell, the COMPLETE forced schedule
of R(x) is exactly a^(ell-1), followed by a stop.

In particular, an admissible prefix containing three returns has a first
change and forbids uu and ttttt. Thus its rounded projection would have
either an empty schedule or at most three t's, and no three-return occurrence.
This would refute a rounded-projection descent on the genuine occurrence
domain; it would not refute B_all or other projections.

Frontier refinement to check: for k>=3, put z=x>>2 and h=x>>4. Both are
ordinary ancestors. If x starts with t, z mod4=2 and the five-mask theorem
forces 4h+3=R(x) to belong to the lower frontier. If x starts with u,
membership instead depends on whether the fiber over h contains digit 3.
Thus loss of the return schedule must be distinguished from loss of frontier
membership.

Admitted finite checks: exactly x=4,...,4095 with the already used k+14
observed horizons; test the two-letter table, the equal-letter identity, and
every observed first-change consequence. For a first change after ell
letters, observing ell branches of R(x) suffices to check the predicted
ell-1 branches and terminal state. Also replay the 19 historical occurrence
rows embedded in `results/problem1/20260905_canonical_return_rows.json`,
in their existing complexity/phase/state/cut/gap order. Select the first
row whose original schedule starts with t as an explicit lower-frontier
example, with membership certified from the established mask theorem.
No new frontier enumeration or search-box extension. Both outcomes change
the proof architecture: a failed identity corrects the proposed coupling;
a valid obstruction eliminates this descent and isolates what must replace it.
One local CPU, 120 seconds, 1 GiB; atomic JSON, exact parameters, full Git
commit, timings, hashes, embedded source, hardware/software and limitations.
Ask for independent derivation and review before adopting the all-depth claim.

## 1. Two-letter table (`partial-proof`)

The exact renewal identities are

```text
F(16h+7)  = 4 P(U(h))+3,
F(16h+11) = 4 U(P(h))+3.                           (1)
```

Modulo 4, P acts by `P(h)=3-h`, while U has output residues 1,2,3,0
on input residues 0,1,2,3, respectively. Hence P U has residues 2,1,0,3,
and U P has residues 0,3,2,1. A successor's normalized quotient must have
residue 1 or 2 for another branch, selecting u or t respectively. This
gives exactly the four rows in the admission table, as an all-depth residue
identity. The hand representatives are

```text
7 -> 27       (ut),       R(7)=3,
23 -> 103     (uu),       R(23)=7,
43 -> 203     (tt),       R(43)=11,
59 -> 215     (tu),       R(59)=15.
```

For the first row the second arrow would be 27->111; for the second,
103->403. These outputs have terminal residues 15 and 3, respectively.
No conclusion about further branches is needed for the two-letter table.

## 2. Exact coupling on equal letters (`partial-proof`)

The generator-blind projection identity says, for any G in {T,P,U},

```text
G(4h+1)>>2=U(h),
G(4h+2)>>2=P(h).                                 (2)
```

If x has prefix uu, write x=64h+23. Then R(x)=16h+7, so
`F(R(x))=4 P(U(h))+3`. Applying (1) at x gives

```text
R(F(x)) = 4 floor(P(U(4h+1))/4)+3.
```

The intermediate U(4h+1) has residue 2 modulo 4 and quotient U(h).
Equation (2) therefore makes this expression `4 P(U(h))+3` also.

If x has prefix tt, write x=64h+43. Its rounded projection is 16h+11.
Now P(4h+2) has residue 1 and quotient P(h), giving

```text
R(F(x)) = 4 floor(U(P(4h+2))/4)+3
        = 4 U(P(h))+3 = F(R(x)).                  (3)
```

In both cases R(x) takes the same first letter as x. If the first two
letters differ, the table instead says R(x) has residue 3 or 15 modulo 16,
and has NO continuing branch. Extending (3) to those cases would silently
apply F outside its domain.

## 3. The first change determines the entire projected schedule

**Theorem (`partial-proof`).** Let the forced schedule of x
begin a^ell b, with ell>=1 and a!=b. Then its rounded projection has the
complete forced schedule

```text
sigma(R(x)) = a^(ell-1).                          (4)
```

Proof. For the first ell-1 states, the next two original letters agree.
Iterating (3) follows the projected orbit through R(F^(ell-1)(x)), with
ell-1 copies of a emitted. At that state the original pair is ab. The
mixed-letter row of the table forces the projected state to stop. This
also covers ell=1, when the projected word is empty.

Suppose x has any full-domain three-return occurrence: its observed prefix
is admissible and contains a u followed by t. Thus its initial constant run
ends before this prefix ends. If it starts with u, uu is forbidden and
ell=1. If it starts with t, ttttt is forbidden and 1<=ell<=4. Consequently

```text
sigma(R(x)) is empty or one of t, tt, ttt.         (5)
```

In particular R(x) has no three-return occurrence at ANY cut. This is an
all-depth obstruction on the genuine full occurrence domain, including
unequal gaps and positive cuts. It does not rely on the unobserved final u
being realized and does not assume global admissibility after the occurrence.
It refutes this proposed descent mechanism, not the desired boundary bound.

For adjacent inclusion the lower state is only required to follow the base
word w of length c, not the three-return continuation. Thus loss of the
continuation alone must not be overinterpreted. If c>0 and the original
schedule starts with u, R(x) has no branch and fails that base prefix. If
the original schedule starts with t^ell u, its first u is at ell and every
occurrence cut is at least ell; the projected word has length ell-1<c.
Therefore R(x) is not even a base-prefix witness for ANY positive-cut
occurrence. At c=0 the base word is empty; these arguments do not exclude
R(x) as an adjacent cylinder witness when it belongs to the lower frontier.

## 4. Frontier membership is a separate issue (`partial-proof`)

Let x be in O_(a,k), k>=3, with a permitted first branch. Put
z=x>>2 and h=x>>4. The ordinary projection theorem gives z in O_(a,k-1)
and h in O_(a,k-2). The fiber over h at level k-1 contains z's digit.

For a first t, z mod4=2. The established digit pairing property
`4h+2 in O => 4h+3 in O` proves

```text
R(x) belongs to O_(a,k-1).                        (6)
```

For a first u, z mod4=1. The five-mask theorem allows precisely 0011,
1011,1111 for that nonempty fiber, and R(x) belongs to it if and only if
the mask is 1011 or 1111. Thus membership is not unconditional in this case.

For a state additionally satisfying Section 3's full three-return hypothesis,
statement (5) applies regardless of R(x)'s frontier membership. In particular,
even when (6) supplies a genuine lower frontier state, it loses all three-return
occurrences. This separates failure of schedule inheritance from failure of
ordinary membership.
The k>=3 restriction avoids the singleton-level exception where rounding
can change the phase; every historical three-return row is well above it.

The first starting-t example in the existing 19-row order is

```text
x = 0x642fdfb in O_(u,14),
z = x>>2 = 0x190bf7e in O_(u,13),
R(x) = 0x190bf7f in O_(u,13).
```

The recorded observed prefix is `tututut`, with c=1 and gaps (2,2,2).
Digit-2 pairing proves the last membership from the middle one. But R(x)
is 15 modulo 16, so it stops immediately and fails the base prefix `t`.
This is an explicit `refuted` universal projected-witness claim on a genuine
occurrence, not a boundary violation or a new frontier census. The row's
original ordinary membership is a previously verified premise.

## 5. Infinite-survivor intersection (`partial-proof`)

Extend R to x in Z_2 with x=3 modulo 4 by writing x=16h+r, where r is
the least residue modulo 16, and setting R(x)=4h+3. The residue and section
proofs above apply unchanged. Let K be the set of all infinite zero survivors
from `problem1_period_two_schedule_coding.md`.

If x in K has a nonconstant schedule, it has a first change at a finite
position, and (4) implies R(x) is not in K. Constant schedules have the
already established unique survivors 1/3 (t) and 5/3 (u). Directly,

```text
R(1/3)=4*(-2/3)+3=1/3,
R(5/3)=4*(-1/3)+3=5/3.
```

The two rational fixed points and their forced schedules were proved in
`problem1_period_two_2adic_zero_countermodels.md`. Uniqueness here is for
the entire constant schedule, as supplied by coding; uniqueness only among
fixed points would not by itself exclude a nonfixed constant-schedule orbit.
Thus

```text
K intersect R^(-1)(K) = {1/3,5/3},
R(K) intersect K       = {1/3,5/3}.               (7)
```

For K_adm consisting of survivors whose entire schedules avoid uu, ttttt,
and ututtu, neither constant schedule is admissible. Therefore
`R(K_adm) intersect K` is empty; more sharply every projected schedule has
length at most three by (5). No nonempty subset of K_adm can be preserved
by R. This is a no-go for this root-preserving digit deletion as a support
descent. It does not establish that K_adm lacks finite integers, and it does
not obstruct invariants under F or different maps.

## Next distinct construction, not an established witness

Subsequent checkpoint: this construction has now been tested and both its
nonnegativity and conditional lower-membership gates are `refuted`; see
`problem1_conjugated_projection_test.md` for exact genuine-domain
counterexamples and the independent 19-row replay. That replay also checks
lower membership for all 14 cut-zero labels, which was not checked in the
original rounded-projection pass below.

The obstruction leaves a more targeted candidate. For an occurrence with
base word w of length c, first evolve to X=F^c(x), project that tail to
R(X), and pull back through the inverse branches for w:

```text
y = B_w(R(F^c(x))),  B_q(z)=4 P^(-1)(Q^(-1)(z))+3.
```

The inverse-branch composition B_w is outer-to-inner in schedule order,
as in the coding theorem. This candidate preserves the base schedule by
construction in Z_2. Neither ordinary finiteness nor membership in the
lower frontier follows. It may therefore be useless as an ordinary shadow.
A future targeted check on the existing occurrences would discriminate
this construction without enlarging a census. No such check has been run
in this pass, and no claim of dominant membership is made.

## Verification and remaining scope

The fixed x=4,...,4095 box had 64 examples of each initial two-letter row,
260 equal-pair coupling checks, 267 mixed-pair stopping checks, and 171
observed first changes. All passed. The original schedules in this box
were observed through termination; none reached k+14 branches. General
first-change cases need not be admissible and can project to runs of u's;
the sharper at-most-three-t bound is only claimed under Section 3's full
occurrence hypothesis.

All 19 historical occurrence labels were replayed through their exact
observed wE(g), with the final u only tested for admissibility. Their
complete projected schedules were empty in 18 cases and `t` in one. The
five positive-cut rows all failed their base prefix. No lower-frontier
membership claim was computationally tested for the 14 cut-zero rows.

The lead independently regenerated all original and projected orbits using
cell arrays, P as the odd section of T, and explicit deletion of the second
base-four digit. Every count and named replay agrees. These are
`finite-exhaustive` statements only in the declared finite sets. Atomic
standard-protocol records, with executed source and exact provenance, are

- `results/problem1/20260905_rounded_projection_primary.json`
- `results/problem1/20260905_rounded_projection_independent.json`

The normalized primary record retains source, parameters, counts, original
stream/artifact hashes and historical witnesses instead of duplicating all
4,092 generic per-input rows. Every omitted orbit was independently replayed.

Muse Spark 1.3 Contributor (Dirac) terminated with a provider tool-routing
error: it emitted an undeclared client tool. It supplied no completed result.
Default contributor Dewey implemented the bounded check and independently
derived the finite-integer identities. Fresh reviewer Ramanujan (agent
`01a07268-b1d6-71a1-a172-cf280de01cee`) adversarially checked Sections 1–5,
including the Z_2 intersection. Its scope clarification in Section 4 is
incorporated: ordinary membership plus one branch alone does not imply the
three-return hypothesis. It also independently accepted the positive-cut
base-prefix obstruction and the cut-zero exception.

This closes the direct rounded-projection descent, including for unequal
return gaps, without proving B_all or signed nonvanishing. The distinct
inverse-branch construction was untested in this pass and is now refuted
in the subsequent checkpoint linked above. General
eventual center periods of least period >=3 remain unhandled.
