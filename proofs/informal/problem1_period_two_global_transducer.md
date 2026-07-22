# Whole-word transducer for the period-two inverse lift

Status: exact all-word transducer reformulation, complete classification of
single-letter additive cocycles, and one finite counterexample to a short
branch-language shortcut. These are partial structural and no-go results. They
do not exclude period two and do not solve Rule 30 center nonperiodicity.

## 1. Accumulated inverse word

For the alternating temporal trace, let `G_m` be the accumulated inverse word
in the generators `t,p,u` after `m` base-4 blocks. The established recurrence
is

\[
G_{m+1}=(G_m)|_{11}\,p\,q_m,
\qquad q_m\in\{t,u\}.
\]

The next spatial bit pair is

\[
e_m=G_m(11).
\]

The alternating inverse lift has finite ordinary support exactly when
`e_m=00` for every sufficiently large `m`. Unlike a fixed-depth portrait,
computing `(G_m)|_11` acts across the complete growing word and therefore
bridges the free middle identified by the frontier-gluing theorem.

## 2. Four-state right-to-left transducer

Scan a word from its innermost, rightmost generator toward its outermost,
leftmost generator. The scan state is the image of the input pair `11` under
the suffix already scanned. Hence the state set is

\[
Q=\{00,01,10,11\}.
\]

For a generator `a` and incoming pair `v`, the emitted letter is the section
`a|_v`, while the successor scan state is `a(v)`. The complete table is

| incoming pair | input `t` | input `p` | input `u` |
|---|---|---|---|
| `00` | `t / 00` | `p / 11` | `p / 11` |
| `01` | `p / 01` | `u / 10` | `u / 10` |
| `10` | `p / 11` | `p / 01` | `t / 00` |
| `11` | `u / 10` | `t / 00` | `p / 01` |

Each entry is `output letter / successor pair`.

If the scan of a complete word `G` begins in state `v`, its output word is
exactly `G|_v` and its terminal state is exactly `G(v)`. In particular, the
period-two recurrence is one pass of this transducer beginning in `11`,
followed by the two boundary letters `p q_m`.

This is an all-word identity. The analyzer exhausts short words only as an
independent implementation cross-check.

## 3. No single-letter additive bridge

A natural attempt is to assign weights `a_t,a_p,a_u` to letters and a potential
`V_s` to each scan state so that every transducer edge satisfies

\[
a_{\rm in}-a_{\rm out}=V_{\rm next}-V_{\rm current}. \tag{1}
\]

Summing (1) across the entire word would telescope the growing middle and
leave only the two scan boundaries. It would therefore be precisely the kind
of global bridge unavailable to separated-front tests.

The twelve edge equations have seven unknowns. Exact rational row reduction
gives

\[
a_t=a_p=a_u
\]

and

\[
V_{00}=V_{01}=V_{10}=V_{11}.
\]

The solution space has dimension two: one multiple of total word length and
one irrelevant constant potential. Thus:

> **Additive-cocycle no-go.** There is no nontrivial single-letter weighted
> count whose change under the whole-word transducer telescopes to its scan
> boundaries.

This theorem does not exclude nonlinear statistics, growing-memory cocycles,
or quantities coupling the transducer to the exact autonomous fringe.

## 4. The three known forbidden branch words are insufficient

The exact moving-fringe language is known to forbid

```text
uu
ttttt
ututtu
```

at every position. Those exclusions substantially reduce the compatible
schedule space, but they are not a complete substitute for the autonomous
fringe recurrence.

Consider the finite branch word

```text
ttttututtttuttttututtttutututttuttuttutu
```

It avoids all three forbidden factors. Starting from `G_0=id` and applying the
exact whole-word recurrence, the output pairs at indices 30 through 39 are all
`00`. The corresponding leading-`t` runs are

```text
0,1,2,3,4,5,6,7,8,9.
```

Therefore the short forbidden language alone permits ten consecutive zero
pairs. The word is **not** claimed to occur in the exact zero-tail fringe
orbit; it is a counterexample only to replacing that orbit by the three-word
subshift.

## 5. Consequence for the critical path

The growing-middle path has now eliminated three broad shortcut classes:

1. fixed separated low and high windows, by the frontier-gluing theorem;
2. single-letter additive cocycles, by the complete edge-equation
   classification above; and
3. use of only the currently known short forbidden schedule words, by the
   explicit forty-branch counterexample.

The next admissible object must retain the exact autonomous fringe state while
using the whole-word transducer. A natural formulation is a coupled two-row
tile system:

- one row is the right fringe under its autonomous two-step Rule 30 map;
- the other is the accumulated inverse word under the four-state scan;
- the low fringe pair supplies the boundary letter `q_m`; and
- the terminal transducer state is the spatial output pair.

A successful invariant must be nonlinear, use growing memory, or telescope a
quantity across this *coupled* system rather than across either row alone.

## 6. Executable certificate

The exact table, short-word cross-checks, additive linear system, and finite
branch-language counterexample are implemented in

```text
experiments/problem1_nonperiodicity/analyze_period_two_global_transducer.py
```
