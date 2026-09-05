# Frontier leading blocks with generation age

Status: `partial-proof` for the exact leading-block marginal, periodic-core
classification, dyadic cycle theorem and forced-history identities below.
Finite uniqueness checks are not an all-width uniqueness theorem.
The target is frontier-conditioned boundary exclusion B_all. No invariant
preventing all critical-cut occurrences has yet been proved.

## Strategy and admission

The bit-length-only boundary bound is refuted by the previous 456-bit
counterexample. That integer fails the ordinary frontier test at its fourth
projected prefix. The next question is whether the full generator history
imposes a stronger exact condition on the leading block than plain membership
of that block in a small frontier.

Ranked routes (`heuristic`):

| Rank | Route | All-depth potential | Falsifiability / cost |
| --- | --- | --- | --- |
| 1 | Exact leading-block evolution and dependence on remaining generation count | A necessary frontier invariant with all-depth quantifiers | High / low structural checks |
| 2 | A single attracting cycle at each leading width | Could simplify the invariant to a phase on one cycle, if proved | High / symbolic cycle lifting |
| 3 | Joint signed correlations conditioned on the generator history | Direct nonvanishing if a usable relation is found | Undetermined / high |

Put A(v)=T(v)>>2=(v>>2) XOR ((v>>1) OR v), and pi(v)=v>>2.
Candidate exact marginal, for either phase and all k>=h>=1:

```text
{pi^(k-h)(x): x in O_(a,k)} = A^(k-h)(O_(a,h)).
```

The right side should be nested as the generation age k-h increases, because
the established projection theorem makes A a self-map of each O_(a,h).
Its eventual image is its finite set of periodic points. A local binary
cycle-extension rule should classify these cycles without enumerating all
states: appending bit e below a prefix cycle gives e'=b XOR(c OR e), where
b,c are the prefix's last two bits. A reset, a parity flip, or an identity
return map gives respectively one same-period cycle, one doubled cycle,
or two same-period cycles. The last case must not be silently ruled out.

Muse is asked to independently derive or refute these identities before a
long proof. The specific stronger candidate tested computationally is that
there is only one attracting cycle for each positive leading-one bit width.
Passing a finite check will not prove that candidate or authorize a cap increase.

Admitted computation: symbolic cycle lifting only through bit width 16,
at most 2^16 retained cycle states at a width. Stop the uniqueness test at
its first splitting cycle. Separately construct ordinary frontiers only
through complexity nine to check the exact marginal for every 1<=h<=k<=9
in both phases; determine the stabilized images for h<=8. Compare these
with the corresponding full-width cycle sets. Check the existing named
456-bit counterexample's first rejection only at h=1,...,8. No new forced
schedule or occurrence census. One local CPU, 120 seconds and 1 GiB;
atomic standard-protocol JSON with executed source, base Git, inputs,
hashes, hardware/software, timings and exact limitations.

Failure corrects the proposed quotient or refutes the single-cycle
simplification. Survival permits an exact derivation, with finite cycle
classification explicitly separated from the all-width statements. The
existing gluing obstruction still rules out treating independent fixed
leading and trailing windows as a complete proof of finite-support exclusion.

Additional exact identity to check on the same stored orbit, with no new
integer or schedule input: pi^(2r)(F^r(x))=A^(2r)(pi^r(x)) for every
recorded r=0,...,233. It should follow from pi A=A pi and
pi^2 F_q=A^2 pi, where F_q=Q P pi on a permitted branch. Failure would
correct the proposed coupling between the frontier head clock and forced
steps; a proof would give an all-scale identity, still without controlling
the removed digits. One ordinary generator advances a protected leading
block by A; one forced step advances it by A^2.

The stronger identity found during derivation is pi^r(F^r(x))=A^(2r)(x).
Check it on the same 234 stored states. Also test the constructive
periodic-point membership proof on the same periodic points already covered
by the h<=8 core comparisons; these add neither widths nor frontier levels.
The resulting 45 generator certificates also check the history scanner:
the emitted word must evaluate to A of the original endpoint, and a valid
terminal gate must append the correct forced generator. Failure would
correct the history-level mechanism. This checks no additional endpoint
or return schedule.
The independent source includes the 128 local binary-extension cases
v=0,...,63 and appended bit e=0,1 as a small boundary/bit-order check.

## 1. Exact leading-block dynamics (`partial-proof`)

For every nonnegative integer v and each ordinary generator G in {T,U,P},

```text
pi G(v)=A(v),        pi A(v)=A pi(v).               (1)
```

The first identity follows because G differs from T only in the two
discarded low bits. The second follows directly by shifting each XOR/OR
operand. A preserves positive bit length: its highest bit comes from v in
the OR term and cannot be cancelled by either right-shifted term.

Let H_(a;k,h) be the set of leading phase-width blocks obtained by removing
k-h base-four digits from O_(a,k). Then, exactly,

```text
H_(a;k,h) = A^(k-h)(O_(a,h)),  k>=h>=1.            (2)
```

Proof. At k=h this is the definition. For the next ordinary generation,
apply (1) to each child G(x). Removing its new low digit applies A to x;
commuting A past the remaining projections gives
H_(a;k+1,h)=A(H_(a;k,h)). All generators have the same projected value,
and every parent has a child, so this is equality of sets, not just inclusion.
Induction proves (2), retaining distinct endpoint sets throughout.

The projection theorem in `problem1_period_two_phase_frontier_projection.md`,
pi(O_(a,h+1)) subset O_(a,h), combined
with (1), gives A(O_(a,h)) subset O_(a,h). Hence the images in (2) are
nested with increasing age k-h. Their eventual constant set is exactly
the periodic points of A that lie in O_(a,h). Indeed every periodic point
belongs to every image, while a point in the stabilized finite image has
arbitrarily long predecessors inside a set on which A is surjective, hence
bijective, so it is periodic.

This condition is stronger than merely requiring the leading block to
belong to O_(a,h). For example,

```text
O_(p,3)       = {50,51,52,53,55},
A(O_(p,3))   = {50,51,55},
A^2(O_(p,3)) = {50,55},       50 <-> 55.
```

Thus every p-frontier state of complexity k>=5 has leading six bits 50
or 55. At k=4 they must instead belong to {50,51,55}. The earlier 456-bit
counterexample has leading six bits 52, so its age-225 level-three test
already rejects it. The ordinary unaged test first rejected level four.
This is an all-depth necessary condition; it is not sufficient membership
of an integer whose remaining lower digits are prescribed.

## 2. Binary cycle lifting and dyadic periods (`partial-proof`)

Let A_w denote A on positive integers of bit length w. The one-bit
projection v>>1 also commutes with A. Appending a low bit has the exact
skew-product rule

```text
A(2v+e) = 2A(v) + (b XOR(c OR e)),
b=bit_1(v), c=bit_0(v), e in {0,1}.                (3)
```

Take a least-period L cycle v_0,...,v_(L-1) of A_w. Above it the low
bit obeys e_(t+1)=b_t XOR(c_t OR e_t). Over one complete prefix cycle:

- If some c_t=1, one step forgets the input bit. The return map is
  constant, with one fixed bit. There is exactly one cycle above the
  prefix cycle and its least period is L.
- If every c_t=0, the return map is XOR by the parity of sum_t b_t.
  Odd parity gives one cycle of least period 2L. Even parity gives two
  cycles, each of least period L.

These are all possibilities. Every cycle projects to a cycle, and every
cycle over the chosen prefix intersects the two-point fiber above v_0.
This proves completeness of cycle lifting without enumeration of transient
states. Period claims are exact because projection already has least period L.

At width one the only positive state is the fixed point 1. Repeated
application of (3) shows that every A_w cycle has power-of-two length,
and therefore its length divides 2^(w-1). This does NOT show that there
is only one cycle: the even-parity, no-reset case explicitly allows splitting.

There are 2^(w-1) positive states of width w. Every orbit therefore has
transient at most 2^(w-1)-1. Combining this finite cardinality bound with
the dyadic period theorem gives the all-width functional identity

```text
A_w^(2^w-1) = A_w^(2^(w-1)-1).                   (4)
```

This is a proved uniform bound, not the much smaller transient sizes
observed in the finite checks below.

## 3. The entire periodic core lies in the frontier (`partial-proof`)

**Theorem.** Every periodic point of A of bit length 2h belongs to
O_(p,h), and every periodic point of bit length 2h-1 belongs to O_(u,h).

The key section table, valid for all z>=0, is

```text
A(4z+d) = S_d(z),   S_0=T, S_1=U, S_2=S_3=P.     (5)
```

To derive it, use A(v)=(v>>2) XOR((v>>1) OR v). Digit zero adds no
correction to T(z). Digit one toggles its low bit. Digits two and three
both force the low OR bit to one and the next OR bit to one, giving
T(z) XOR 1 XOR (2 if z is even else 0), which is P(z).

Proof of the theorem. At phase u, h=1 has the only positive width-one
cycle point 1. At phase p, width two has A(2)=3 and A(3)=3, so the only
cycle point is the required root 3. Now let v be a periodic point at
phase complexity h>=2, and choose its predecessor v^- on its A-cycle.
The point z=pi(v^-) is periodic because pi commutes with A. It is positive
and has the phase bit length for complexity h-1, so by induction
z belongs to O_(a,h-1). Write v^-=4z+d. Then

```text
v=A(v^-)=S_d(z),
```

an ordinary generator image of a valid lower frontier point. Hence
v belongs to O_(a,h), proving the induction in both phases.

This proof is constructive: repeatedly take a cycle predecessor, remove
its last two bits, and record S_d. The complexity decreases at every step
until the appropriate root is reached. Reversing the recorded generators
gives an ordinary history of the original periodic point. It need not be
the only history, and no representation count is inferred.

Consequently the stabilized image in Section 1 is precisely

```text
C_(a,h) = Per(A_w),   w=2h for p, w=2h-1 for u.    (6)
```

This is equality with the full positive-width periodic-point set, not just
with the cycle points that happened to be sampled in a frontier. It holds
whether or not the cycle-lifting process ever splits.

In particular, every positive integer of the appropriate bit length enters
O_(a,h) after finitely many A-iterations: it eventually reaches an A-cycle,
and every such cycle lies in that frontier. Once there it stays there.
This does not make the original integer a frontier point; A generally
changes its low bits and its forced schedule.

For a fixed h, all sufficiently large ages in (2) give exactly C_(a,h).
Any cyclic head is realizable as the leading block of some O_(a,k) state
for every k>=h: choose its A-predecessor of length k-h on the cycle and
apply any k-h ordinary generators. This existential head extension does
not preserve a prescribed lower block or a forced-schedule cylinder.

## 4. Forced steps and the full original-width block (`partial-proof`)

For a nonnegative integer x, an actual forced step exists only when x=7
or 11 modulo 16, selecting
Q=U or T respectively. Such an x is 3 modulo 4. By (5),

```text
A(x)=P(pi x),     F(x)=Q(A(x)).
```

Every defined forced output is also 3 modulo 4. Therefore (1) gives the
strong exact identities

```text
pi F(x)=A^2(x),         F(x)=4A^2(x)+3.           (7)
```

By commuting A past pi and inducting over defined steps,

```text
pi^r(F^r(x))=A^(2r)(x).                           (8)
```

Thus the leading block of the original input width, at forced time r,
is exactly its A-orbit at time 2r. The earlier candidate with pi^(2r)
on the left follows by applying pi^r again, but discards more information.
For example 7 gives A^2(7)=6 and F(7)=27; 43 gives A^2(43)=50 and
F(43)=203.

The total map x->4A^2(x)+3 can be evaluated even outside a permitted
branch. Doing so does not make it a valid forced continuation: the mod-16
gate and the admissibility requirements remain essential at every step.
No infinite valid orbit follows from defining that total extension.

The frontier self-map property also shows the limitation of simply
propagating these head tests: if x belongs to O_(a,k), then
A^(2r)(x) belongs to A^r(O_(a,k)) for every r. Rechecking this particular
necessary leading-block condition after a defined forced step adds no
new exclusion by itself. A boundary proof still needs to connect the
head evolution to the discarded digits and the return constraints.

## 5. Exact update of an ordinary generator history (`partial-proof`)

The same identities give a concrete history-level description. For any
ordinary generator G and nonnegative integer v, let d=G(v) mod 4. Then

```text
A(G(v))=S_d(A(v)).                                (9)
```

Indeed apply (5) to G(v), then use pi G(v)=A(v). Since A fixes both
ordinary roots, an ordinary history can be transformed from left to right
into another history of the same length representing A(x).

The scanner remembers the old prefix value modulo four, updates that
residue with the old generator, and emits S_d of the new residue:

| Old residue | Next residues for T,U,P | Emitted generators for T,U,P |
| --- | --- | --- |
| 0 | 0,1,3 | T,U,P |
| 1 | 3,2,2 | P,P,P |
| 2 | 2,3,1 | P,P,U |
| 3 | 1,0,0 | U,T,T |

Start the scanner at residue 3 for the p root and 1 for the u root;
the root itself is retained. The table is a direct reduction of T,U,P
modulo four. Appending the actual forced Q to the transformed history
then represents F(x)=Q(A(x)), provided the branch gate holds.

The four-state scanner alone does not decide that mod-16 gate. One can
instead track the old prefix modulo sixteen, updating it with each original
generator modulo sixteen and emitting the same letter from its residue
modulo four. At the end, residue 7 appends U, residue 11 appends T, and any
other residue has no permitted forced step. This gives an exact sixteen-state
scanner for the history update and its stopping gate.

This is a finite-state scanner on an unbounded history word. The history
grows by one generator per forced step, so it is not a finite-state
endpoint quotient and does not evade the established quotient no-go results.
Different histories of the same endpoint still represent the same A(x)
and, on a defined forced step, the same F(x).
Counting these histories is not counting distinct endpoints and must not
be substituted for the signed-belief mass.

## 6. Bounded verification and independent derivations

The following numerical statements are `finite-exhaustive` on the stated
domains. Symbolic lifting found one cycle at each width 1 through 16:

| Widths | Number of cycles at each width | Least cycle period |
| --- | --- | --- |
| 1–3 | 1 | 1 |
| 4–8 | 1 | 2 |
| 9–16 | 1 | 4 |

There was no splitting cycle in this box. All-width single-cycle uniqueness
remains conjectural and is unnecessary for the periodic-core theorem.
No wider cycle calculation follows from this finite passage.

All 90 leading-block marginal cases for 1<=h<=k<=9 in both phases pass,
as do all 18 frontier self-map checks. All 16 stabilized frontier cores
through h=8 equal their full-width periodic-point sets. Their least
stabilization ages are

| h | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p | 0 | 0 | 2 | 4 | 6 | 8 | 9 | 11 |
| u | 0 | 1 | 2 | 3 | 4 | 7 | 8 | 10 |

Age s means the first equality A^(s+1)(O_h)=A^s(O_h). These small ages
are finite values, not an all-depth linear stabilization bound. On the
named 456-bit integer, the first age-dependent rejection is h=3; its
head 52 disappears after just one image step, while its actual age is 225.

Dewey's primary computation uses the binary return-map classification and
checks every generated cycle transition with packed A and T(v)>>2. It
constructs both phase frontiers with cell-array generators, comparing them
with the packed formulas on 1,728 generator evaluations. The lead's
independent cycle construction instead follows direct high-to-low cell
orbits from the two one-bit extensions of a representative on each prefix
cycle. Those two orbits cover every lifted cycle by the projection theorem;
they do not enumerate all transient states. Independent ordinary frontiers
use the packed generators. The complete frontier sets, cycle lists,
removed image layers, core sets and stabilization ages agree.

The same 234 previously recorded states verify both the strong factorization
(8) and the weaker projected identity. No new forced trajectory was searched
or constructed. The independent core-to-history construction gives 45 exact
generator certificates, one for every periodic point in the 16 checked
cores. All evaluate to their target values. Their scanner updates evaluate
to A of those values; eight have a permitted terminal gate, and all eight
appended histories evaluate to 4A^2(x)+3.

Muse Spark 1.3 Contributor independently derived the head marginal, cycle
extension cases, dyadic periods, periodic-point membership induction,
strong forced factorization and history table without tools. It explicitly
confirmed that the periodic-core theorem requires no extra conjecture.
Fresh reviewer Ramanujan independently approved the core induction and
history-gate distinction; its requested nonnegative-domain clarification
is incorporated. The lead retains responsibility for all theorem scopes.
The same reviewer subsequently approved the completed finite coverage,
source and payload provenance, internal cycle-data linkage, and portable
verification, with no remaining mathematical or provenance correction.

Atomic standard-protocol records are

- `results/problem1/20260905_frontier_head_primary.json`
- `results/problem1/20260905_frontier_head_independent.json`
- `results/problem1/20260905_frontier_head_verification.json`

They include exact inputs, full base Git, executed source, hashes,
hardware/software, timings and limitations. The primary wrapper retains
both original primary run payloads and their complete raw data; its reported
runtime is the sum of those two recorded computations, not a claim about
contiguous elapsed time. The orbit check's original cycle-file input is
recoverable from the embedded head data. Documentation hashes describe
run-time snapshots of evolving notes, not operative data dependencies.

For portable replay, extract an independent or verification `source_text`
to a file outside the checkout and run it from the checkout root, or set
RULE30_REPLAY_ROOT. RULE30_REPLAY_OUTPUT selects its output file. Verification
reads only the three committed records named in its source, checks the
original payload hashes and internal raw-data linkage, and needs no original
temporary files. Primary sources retain their recorded absolute paths.
Replay changes timestamps, timings and base Git provenance.

## 7. Remaining critical-path obligation

The head condition now has an exact dynamical form and an intrinsic periodic
core, with a constructive frontier membership certificate for every core
point. None of this proves the return-conditioned cancellation hyperplane
is avoided, or proves the all-cuts boundary bound B_all.

The proposed first use on dominant-shadow seeds is now completed in
`problem1_cyclic_seed_boundary.md`: the exact aged-seed restriction gives
stronger dominant-empty layers at residual levels1,2. It does not improve
the raw-shadow or occurrence bounds. The subsequent note
`problem1_history_potential_obstruction.md` refutes universal strict
three-return descent for four-state additive history potentials bounded
below on all ordinary histories, via a genuine cycle-circulation witness.
The same witness does not exclude sixteen-state additive potentials.

The longer proof target is the history scanner with its forced append and
mod-16 stopping gate. For a starting ordinary word of complexity k, an
all-depth boundary proof must exclude a three-return occurrence at any
cut c>=k-2 (equivalently, use the existing five critical cuts). The k here
is the original complexity, not the growing history length after forced
steps. Fixed-length cycle classification does not establish termination of
this growing-word process. A proposed potential must respect the exact
scanner update and return language; letter counts or a guessed unique
attractor are not assumed sufficient.

The new theorem permits cycle splitting and avoids making uniqueness a
dependency. Larger cycle or frontier censuses are not the next step.
Adjacent inclusion, B_all, signed nonvanishing, and eventual center periods
of least period at least three remain open.
