# Adjacent-level shadows for three-return phase plateaus

Status: exact all-depth reduction of a three-return zero-penalty plateau to an
adjacent-complexity prefix-language failure, plus a complete finite census
through phase complexity 25 showing no such failure. The census is not an
all-depth proof of the required language inclusion.

## 1. Prefix cylinders and the indexing convention

For phase `a in {p,u}`, let `O_(a,k)` be the ordinary outputs of exact phase
complexity `k`.

Every survivor state is `3 mod 4`. A schedule prefix

```text
w = q_0 q_1 ... q_(L-1)
```

corresponds to a survivor cylinder of depth `L+1`: modulo `4^(L+1)` the state
sees exactly the branches `q_0,...,q_(L-1)`, while branch `q_L` is still
invisible.

Define the phase prefix language

\[
P_{a,k}=\{w:\text{some }x\in O_{a,k}\text{ follows the forced zero schedule }w\}.
\]

Equivalently, `w in P_(a,k)` exactly when the depth-`L+1` survivor cylinder for
`w` intersects `O_(a,k)`.

The minimum phase complexity of the cylinder is

\[
\kappa_a(w)=\min\{k:w\in P_{a,k}\}.
\]

This convention avoids the recurring off-by-one error: a word of length `L`
uses a modulus with `L+1` base-four digits because the low digit `3` is fixed
before any schedule branch becomes visible.

## 2. Three-return continuations

Let

\[
g=(r_0,r_1,r_2),\qquad r_i\in\{2,3,4,5\}.
\]

The visible part of three consecutive returns is

\[
E(g)=u t^{r_0-1}u t^{r_1-1}u t^{r_2-1}.
\]

Its length is

\[
B=r_0+r_1+r_2.
\]

The final `u` at the third successor return is invisible at the deepest
cylinder, but the complete local schedule

\[
\widehat E(g)=E(g)u
\]

must still avoid the already-proved forbidden factors

```text
uu
ttttt
ututtu
```

There are exactly 56 admissible gap triples after these exclusions.

Define

\[
T_{a,k}=\{w:\exists x\in O_{a,k},\ \exists g,
\text{ the forced schedule of }x\text{ begins }wE(g),
\text{ and }w\widehat E(g)\text{ is admissible}\}.
\]

Thus `T_(a,k)` records every base prefix that has a three-return continuation at
complexity `k`, whether or not that prefix is minimal at `k`.

## 3. Exact adjacent-shadow reduction

Assume three consecutive return penalties vanish from the base prefix `w` at
phase complexity `k`. Then the same ordinary state witnesses the base cylinder
and all three deeper return cylinders, so

\[
w\in T_{a,k}.
\]

Because `k` is the minimum complexity of the base cylinder,

\[
\kappa_a(w)=k.
\]

In particular,

\[
w\notin P_{a,k-1}.
\]

Therefore every three-return zero-penalty plateau produces a failure of the
adjacent-level inclusion

\[
\boxed{T_{a,k}\subseteq P_{a,k-1}.}
\]

Consequently, the all-depth statement

\[
\boxed{
T_{a,k}\subseteq P_{a,k-1}
\quad\text{for every phase and every }k\ge2
}
\]

is sufficient to prove that every three consecutive returns contain a positive
phase penalty.

This inclusion is stronger than logically necessary. Its failure need not itself
produce a plateau, because the same prefix could occur at complexity `k-2` or
lower while skipping `k-1`. The exact implication used here is only

\[
\text{three-return plateau}\Longrightarrow
T_{a,k}\not\subseteq P_{a,k-1}.
\]

## 4. Why the adjacent shadow is useful

A generic lower-complexity witness would already contradict minimality. The
adjacent shadow is sharper: every observed three-return occurrence at complexity
`k` has a witness in the same base cylinder at complexity exactly `k-1`.

For a state `x` whose continuation begins after a cut of length `L`, the base
cylinder has depth `L+1`. A shadow is any

\[
y\in O_{a,k-1}
\]

with

\[
y\equiv x\pmod{4^{L+1}}.
\]

Equivalently, the forced schedule of `y` begins with the same length-`L` base
prefix. The shadow need not be the ordinary projection `x >> 2`; direct
projection generally changes the low survivor cylinder. The finite data show
that the required shadow is a different phase-frontier state.

This converts the remaining all-depth problem from minimizer enumeration into a
language inclusion between two adjacent phase levels.

## 5. Python reference campaign

The Python analyzer constructs exact phase frontiers and, at each complexity,
builds the complete set of survivor prefixes realized one level earlier. It then
checks every:

- ordinary output congruent to `3 mod 4`;
- schedule cut, including positive cuts inside a longer forced schedule;
- admissible three-return gap triple.

For each occurrence it tests whether the base prefix belongs to the preceding
complexity's prefix language.

Default complexity 16 results:

```text
phase-p occurrences:              8
phase-u occurrences:             11
total occurrences:               19
positive-cut occurrences:         5
shadow violations:                0
maximum cut:                       2
```

Full controlled complexity 20 results:

```text
phase-p occurrences:            117
phase-u occurrences:             93
total occurrences:              210
positive-cut occurrences:        58
shadow violations:                0
maximum cut:                       4
```

Certificates:

```text
K=16:
66675662be4c8a43ca13eb0995549c0596819c3aba9d7693fbc8df121cea36f9

K=20:
05b8559842204a24e94595b39fa03dc2a5806295ad1756712d35130285056324
```

## 6. Independent complexity-25 census

The C++ analyzer independently exhausts both phase frontiers through complexity
25. Unlike the earlier candidate census, it does not discard nonminimal
occurrences. It checks the adjacent shadow for every occurrence.

```text
phase-p outputs checked:              9,118,715
phase-u outputs checked:              7,745,997
total outputs checked:               16,864,712
eligible outputs, x = 3 mod 4:         4,831,012

phase-p three-return occurrences:          1,794
phase-u three-return occurrences:          1,601
total three-return occurrences:            3,395
positive-cut occurrences:                    898
states containing an occurrence:           2,856
maximum positive cut:                           9
adjacent-shadow violations:                     0
```

Every one of the 3,395 occurrences has a same-cylinder witness exactly one phase
level lower.

Controlled run evidence:

```text
output SHA256:
a4068a2e2e66915bc5ea1cf12faa41b6c27e2d72cc0f226f126c8d59f0f94d8d

runtime: about 3.3 seconds
peak resident memory: about 403,512 KiB
```

## 7. Research consequence

PR #36 showed that no minimum-complexity state through level 25 sustains three
zero return penalties. The present result explains the stronger local reason
seen throughout the same range: every three-return-bearing state is shadowed in
its base cylinder at the immediately preceding phase level.

The next proof target is no longer a shortest-path or minimizer problem. It is
the all-depth prefix-language inclusion

\[
T_{a,k}\subseteq P_{a,k-1}.
\]

A successful continuation should derive this inclusion from the recursive
phase-frontier lift relation, likely by constructing a finite shadow transducer
that reads the base survivor prefix while preserving a one-level complexity
offset.

## 8. Scientific boundary

The reduction from a plateau to an adjacent-shadow failure is exact at every
depth. The verified shadow inclusion is finite through phase complexity 25.

This result does not yet prove the all-depth inclusion. It therefore does not
prove phase-complexity divergence, exclude eventual center period two, or solve
Rule 30 center nonperiodicity.
