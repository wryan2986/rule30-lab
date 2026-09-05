# Finite-integer schedule repetition and boundary subclasses

Status: `partial-proof`, exact all-depth bounds and support criterion with
independent derivation and adversarial proof review. Candidates A–D below
record the admission made before computation; their proofs follow in
Sections 1–4. Finite checks are separately labelled. Problem 1 and B_all
remain open.

## Strategy and admission

The bit-length-only boundary test did not refute its candidate, but had weak
coverage. Do not enlarge that box. Instead combine the exact forced-branch
congruence with the degree law to control repeated words on a finite orbit.

Ranked routes (`heuristic`):

| Rank | Route | Plausibility / all-depth potential | Falsifiability / cost |
| --- | --- | --- | --- |
| 1 | Low-bit agreement versus degree at two orbit times | High / exact repetition bound and restricted boundary cases | High / low |
| 2 | Spatial recurrence for periodic auxiliary survivors | Medium / support constraints, not arbitrary schedules | High for fixed period / medium |
| 3 | Frontier-specific correlation invariant at the five critical cuts | Unknown / full B_all | Unknown until specified / high |

Use the existing forward maps T,P,U and forced F, with residue 7 selecting
u, residue 11 selecting t, and all other residues stopping. Let
`x_j=F^j(x)`, `s=bitlen(x)`, `k=ceil(s/2)>=2`, for x a positive finite
integer. No ordinary-frontier membership or language admissibility is assumed
unless explicitly stated.

Candidate A: if 0<=i<j and the observed schedule tails at i and j agree for
r branches, then `r<=k+j-2`.

Candidate B: if an observed prefix of length n has period p>=1 in the finite
word sense (`q_l=q_(l+p)` whenever both positions are present), then
`n<=k+2p-2`.

Candidate C: if the prefix through a three-return occurrence at c is
p-periodic and its gaps are (p,p,2), then `c<=k-4`. Here 2<=p<=5 and the
whole prefix, not merely the local return motif, must be periodic. For a
p-periodic suffix beginning at m<=c, the proposed bound is instead
`c<=k+2m-4`. These are restricted statements, not B_all for arbitrary words.

More generally Candidate B would give
`c<=k+2p-B-2` whenever the prefix through an occurrence of observed motif
length B is p-periodic. If `B>=2p+1`, this discharges B_all for that occurrence.
For a periodic suffix starting at m, replace the bound by
`c<=k+2m+2p-B-2`. These algebraic consequences are included in the same
finite check on existing observations, without enlarging the input set.

Candidate D (support criterion): for any observed periodic factor of length
n, period p, beginning at position m, the excess `n-m-2p` is at most k-2.
Consequently an infinite schedule with unbounded such excess cannot code a
nonnegative finite integer. In particular, unbounded prefix excess n-2p
would suffice, even when the auxiliary schedule is not eventually periodic.
This does NOT assert that the actual moving-fringe schedule has that property.
Testing D uses only factors of the same already admitted finite words.

Admitted finite check: reuse exactly x=4,...,4095 and the k+14 observed
horizons already checked, with no frontier census or larger input box.
Check every observed repeated-tail pair and every period of every observed
prefix. Search for the first violating x and report equality cases, if any.
Check the stated boundary subclass only when its full-prefix hypothesis is
verified. One local CPU, 120 seconds, 1 GiB; atomic JSON, embedded executed
source, full Git commit, parameters, timings, hashes, hardware/software and
limitations. Also request an independent derivation or counterexample to
each lemma, with special attention to the finite terminal-state congruence.

A counterexample kills or corrects this proposed size/congruence argument.
If it survives, attempt a proof from those two exact identities and identify
precisely which boundary cases it discharges. Finite survival alone will not
be used to establish any all-depth bound.

Additional scope check admitted before execution: test the short-period
certificate on exactly the 15 canonical motifs (already contained in the
previous finite word box). This distinguishes an adequate universal
certificate from one structurally limited to a subset of return labels.
No new frontier inputs or schedule census are added.

## 1. Finite common-prefix congruence (`partial-proof`)

This step does not assume that either finite state has an infinite survivor
continuation. Every permitted step has input and output 3 modulo 4. For
residue 7, z=x>>2 is 1 modulo 4, P(z) is 2 modulo 4, and U(P(z)) is 3
modulo 4. For residue 11, those residues are respectively 2, 1, and 3
using T at the last step.

Each of T,P,U preserves the exact 2-adic valuation of the difference of
distinct inputs: the output bit at the first differing position is the
input bit there, toggled only by identical lower-bit data. Consequently,
for distinct a,b in a common permitted branch cylinder,

```text
v2(F(a)-F(b)) = v2(a-b)-2.                         (1)
```

If a,b follow r common branches, the two states after those branches are
both 3 modulo 4, even if either stops there. Pulling that congruence back
through (1) gives

```text
a = b modulo 2^(2r+2).                            (2)
```

For r=0 this is asserted only for a,b already known to be 3 modulo 4.
For r>=1 their permitted first branch supplies this condition. Identical
inputs cause no problem for the congruence; (1) itself is stated for distinct
inputs. This finite version is consistent with the infinite-survivor coding
in `problem1_period_two_schedule_coding.md`, but does not invoke uniqueness
of infinite future schedules to obtain a statement about terminated words.

## 2. Repetition versus integer size (`partial-proof`)

**Theorem.** Let x be a positive finite integer, s=bitlen(x), k=ceil(s/2)>=2.
Suppose its forced orbit is defined through time j, 0<=i<j, and its schedule
tails at i,j share r observed branches. Then

```text
r <= k+j-2.                                      (3)
```

Proof. The exact degree law gives `bitlen(x_l)=s+2l`. Thus x_j>x_i and

```text
0 < x_j-x_i < 2^(s+2j).
```

There has been at least one permitted step, so all states relevant to the
r=0 case are 3 modulo 4 as well. By (2), the positive difference is divisible
by `2^(2r+2)`. Therefore `2r+2<s+2j`, or

```text
r <= floor((s+2j-3)/2) = k+j-2.
```

This proves the theorem for all finite orbit segments, with no language
admissibility or ordinary-frontier assumption.

**Periodic-prefix corollary.** If an observed prefix of length n has period
p>=1, then

```text
n <= k+2p-2.                                     (4)
```

For n<=p this is immediate since k>=2. For n>p, its tails at 0 and p agree
for n-p branches. Apply (3) with i=0,j=p,r=n-p. A finite word need not
contain an integral number of periods, and no branch after its end is used.

## 3. Restricted boundary exclusion (`partial-proof`)

Consider a full-domain three-return occurrence at cut c with observed motif
length B. If the WHOLE prefix of length c+B is p-periodic, (4) gives

```text
c <= k+2p-B-2.                                   (5)
```

If `B>=2p+1`, this yields `c<=k-3`, precisely the required B_all bound for
this occurrence. In particular, for gaps (p,p,2), B=2p+2, so

```text
c <= k-4.                                       (6)
```

**Exact scope obstruction (`partial-proof`).** If the
whole observed prefix is p-periodic and B>=2p+1, its symbols at c, c+p,
and c+2p are all u. But E(g) has exactly three u's. These must therefore
be its three u positions, forcing r0=r1=p. Thus for canonical triples the
certificate can cover only (2,2,2), (3,3,2), (4,4,2), and (5,5,2), and
cannot cover the other 11 labels under any choice of p. Even for those four
labels, periodicity of the entire preceding prefix is an additional
requirement. This is a limitation of this sufficient certificate, not a
refutation of B_all for the remaining labels.

For example, the known p/k15/0x37b38787/cut0 canonical occurrence has
gaps (2,4,2), observed motif `ututttut`, length 8 and least finite-word
period 6. It is outside the certificate. Its occurrence and canonical
replacement are already recorded in
`results/problem1/20260905_canonical_return_rows.json`;
it is not a new frontier search or a boundary violation.

This proves an all-depth subclass of the boundary exclusion even without
ordinary-frontier membership. It does not prove B_all for arbitrary return
prefixes. The motif alone has no control over periodicity of the preceding
word. The final appended u still need only be admissible, not observed.

If periodicity begins only at position m<=c, use the state x_m of complexity
k+m and a periodic observed factor of length c+B-m. Then instead

```text
c <= k+2m+2p-B-2,                                (7)
```

which for gaps (p,p,2) is `c<=k+2m-4`. The two appearances of m are
essential: shifting the origin increases the state complexity and shortens
the observed word. Dropping either one would falsely improve the bound.

## 4. A support certificate beyond periodic schedules

For an infinite branch schedule q, define

```text
R(q) = sup { n-m-2p : m>=0, n>=1, p>=1,
                       q[m:m+n] has finite-word period p }.
```

The supremum is over integers and may be infinite. Periods p>n can be
included or omitted without changing the supremum, since p=n gives a
larger value for the same factor.

Restricting to m+n<=N defines a finite-prefix maximum R_N for N>=1.
The admissible set of factors grows with N, so R_N is nondecreasing. The
proof below bounds every R_N by k-2 for a schedule from a finite integer.
Thus this is a monotone schedule statistic coupled to an exact support-size
bound, not merely a statement that the raw integer degree increases.

**Theorem (`partial-proof`).** If q is the forced infinite
schedule of a positive finite integer of complexity k, then

```text
R(q) <= k-2.                                    (8)
```

Proof. Apply (4) at the factor's starting state x_m, of complexity k+m.
It gives `n<=k+m+2p-2`, hence the displayed bound on every term of the
supremum. Therefore `R(q)=infinity` excludes every nonnegative finite
integer survivor. Integers of bit length at most two, including zero,
have no permitted branch, so none is an omitted exception.

The exact coding theorem supplies a unique 2-adic survivor Phi(q) for every
infinite q. Thus `R(q)=infinity` implies that Phi(q) has infinitely many
nonzero binary digits. Every eventually periodic q satisfies the criterion
by fixing m,p and letting n grow; this recovers the earlier exclusion but
does not require eventual periodicity. Unbounded prefix excess n-2p alone
is already sufficient by taking m=0.

No unbounded-excess assertion is made about the actual moving-fringe
schedule. A long observed periodic prefix supplies only a finite lower
bound on hypothetical input complexity. It cannot settle finite support
without an all-depth repetition argument. The old seven-block approximation
that fails at block 153 is not revived as a periodicity claim.

## 5. Explicit aperiodic admissible example (`partial-proof`)

To test whether (8) covers more than the old eventual-periodicity theorem,
set A=`uttt`, B=`utttt`, and define W_0=A, W_(h+1)=W_h^3 B. Let q be the
unique infinite word having every W_h as a prefix. All u-to-u gaps are 4
or 5, so q avoids uu, ttttt, and ututtu. The prefix W_h^3 has length
3|W_h| and period |W_h|, giving excess |W_h|, which tends to infinity.

In the gap alphabet, write a=4 and b=5. The corresponding prefixes obey
w_0=a, w_(h+1)=w_h^3 b. Their terminal run of b's has length h, and their
number of a's is 3^h. The limit has unbounded b-runs and infinitely many
a's, so it is not eventually periodic. Eventual periodicity of q would
force eventual periodicity of its u-gap sequence, a contradiction.
The last encoded gap in w_h closes at the u immediately following W_h in
the infinite word; no extra u is silently included in the finite word W_h.

Thus this explicitly aperiodic admissible word is excluded from finite
integer support by (8). It is an auxiliary construction, not the actual
moving fringe and not a solution of Problem 1. Admitted hand/finite check:
W_0,...,W_4 only, verifying the recursion, word admissibility, cubic prefixes,
gap counts and terminal runs. This fixed construction is not a new census.

## Verification status

The primary same-box check completed without violations: 2,186 tail pairs,
1,391 prefix-period instances, and 2,964 periodic-factor instances. No
equality case occurred. Boundary-subclass coverage is only the already-known
x903 occurrence; it cannot establish the general result. The proofs above
use exact congruence and size arguments instead. Positive-m occurrence
cases are absent from this box and are not claimed computationally covered.

The lead independently regenerated every orbit with cell arrays and the
odd-section definition of P, checked all 2,186 actual difference valuations
(including r=0), and reproduced all period-case counts using word tiling.
The 568 comparisons with r>0 include terminal-endpoint cases. The constructed
W_0,...,W_4 have lengths 4,17,56,173,524 and pass the admitted word/gap checks.
The separate 15-motif scope check gives exactly the four diagonal labels
allowed by the obstruction in Section 3; `ututttut` has least period 6.
These are `finite-exhaustive` claims in the stated boxes only.

Atomic standard-protocol records with full executed source, hashes and
provenance are:

- `results/problem1/20260905_finite_schedule_repetition_primary.json`
- `results/problem1/20260905_finite_schedule_repetition_independent.json`

Muse Spark 1.3 Contributor (Curie) terminated with provider HTTP 429 and
supplied no completed check. Default reviewer Dewey implemented the bounded
check and independently derived the congruence/size argument for A–D.
Fresh reviewer Averroes (agent `01a07243-5af4-7a53-8e77-49c2cd82b497`)
adversarially reviewed Sections 1–5 and found no fatal gap. Its requested
clarification of the final encoded gap in W_h is included above. It checked
the proof and dependency scope, not a census. The source coding theorem's
existence of a survivor is sufficient for Section 4; uniqueness is not
needed for the exclusion argument.
The same reviewer independently accepted the subsequent four-label scope
obstruction, explicitly checking that it applies to every possible period,
not only the least period. The other 11 labels have r0!=r1.

Neither reviewer nor the lead inferred unbounded repetition excess for the
actual fringe from this example or the old seven-block finite approximation.
The new criterion needs that separately established all-depth premise to
apply to a physical alternating trace. Nonperiodic prefixes outside the
restricted Section 3 certificate still leave B_all unresolved. General
eventual periods of least period >=3 are unhandled by this note.
