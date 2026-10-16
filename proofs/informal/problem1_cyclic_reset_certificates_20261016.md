# Cyclic blind-gate resets through depth 23

Date: 2026-10-16. Status: **partial-proof**, computer-assisted at explicitly
fixed spatial depths. **Rule 30 Prize Problem 1 remains OPEN.**

Base repository commit: `c424346e1a6efdf7cdd673efeff4b6578fe830b6`, on
`research/sol-blind-frontier`. This is AI-assisted research, not independently
reviewed human mathematics or a Lean formalization.

## 1. Exact claim and admission

Use the normalized multilift portal and the statement S_r from
`proofs/informal/problem1_all_depth_gate_candidate.md` at the base commit.
A retained product edge consists of two depth-(r+1) stacks whose complete
upper depth-r states and next upper states agree. Labels can differ only
on an upper-blind edge. Such an edge is bad when the labels agree but the
outgoing added Y bits differ.

**Computer-assisted theorem.** For each integer **6 <= r <= 23**, no bad
edge belongs to a directed product cycle. Equivalently, S_r holds at each
of those depths, for **every temporal presentation period**, without any
parity, nonzero-parent, finite-ancestry, or temporal-length restriction.

This extends the previous S4/S5 checkpoint. It is NOT an all-depth theorem,
a proof excluding eventual period two, or a solution of Prize Problem 1.
The range refers to spatial reconstruction depth, NOT to allowed periods.

Admission: test a uniform collision-segment criterion after strengthening
the necessary cyclic common prefix. A genuine failed segment would refute
that criterion. A closed certificate removes the corresponding fixed-depth
gate obstruction. Neither outcome establishes the original-support budget.

## 2. Raw dynamics and a uniform certificate lemma

At layer j put a_j=X_j and b_j=X_j XOR Y_j, with raw boundaries

    (a_-1,b_-1)=(1,1), (a_0,b_0)=(0,1).

Before applying a label, each raw track updates by

    a'_j = a_(j-2) XOR (a_(j-1) OR a_j),
    b'_j = b_(j-2) XOR (b_(j-1) OR b_j).

Label one swaps the two complete outgoing raw tracks; label zero does not.
An upper edge is blind exactly when the outgoing raw words are identical.
Immediately after a blind edge write their common word C, in increasing
layer order. Across two product copies, let d_a,d_b be the differences in
their added raw child cells. On a common-label edge, before the label swap,

    e_a = (1 XOR a_r) d_a,
    e_b = (1 XOR b_r) d_b.                         (1)

The label then swaps e_a,e_b when it swaps the upper tracks. The outgoing
added Y difference is e_a XOR e_b and is independent of that swap.

**First-return certificate lemma.** For every possible postblind C, suppose
there is a set R_C of triples (a,b,d), with d encoding a nonzero raw child
difference pair, satisfying:

1. R_C contains (C,C,d) for d=(1,0),(0,1),(1,1).
2. At a nonblind common-label transition, a nonzero successor difference
   gives a successor triple still in R_C. A zero difference can be discarded.
3. At every blind exit from R_C, equation (1) gives e_a=e_b.

Then S_r holds. The sets need not be finite for the mathematical lemma;
finiteness merely makes the certificate directly checkable.

**Proof.** In a putative bad product cycle, choose the cyclically preceding
upper-blind edge. The child differences immediately after it are arbitrary,
and hence are either zero or covered by condition 1. Until the next blind
edge, the two labels must agree. A zero difference remains zero; otherwise
condition 2 follows the difference within R_C. At that next blind edge,
condition 3 makes the outgoing added Y difference zero, a contradiction.
The argument also covers a cycle with a single blind visit, by wraparound.
No assumption about an odd driver or a unique cyclic child is used. QED.

A certificate need NOT force a reset in a uniformly bounded time. Some of
the nonzero-difference graphs here contain cycles avoiding blind exits.
Forward closure and safe blind exits, not acyclicity, are the assertions.

## 3. A stronger necessary cyclic prefix

The complete upper graphs at depths six and seven are independently
certified using forward-closed sets, not a trusted SCC classification.
For each blind output C, enumerate all blind sources leading to C and
construct a forward-closed upper set containing (C,C). If it excludes a
source, that source cannot lie on a cycle: its blind successor cannot
return to it.

Checking all upper states and both labels establishes the following
necessary common outputs on a cyclic blind history:

    depth six:  011110,
    depth seven: 0111100.                         (2)

Projection of any deeper cyclic blind history to seven layers is again a
cyclic blind history. Thus every depth-r cyclic common row, r>=7, begins
with 0111100. This projection implication is unbounded in r; it does not
assert a reset at all depths.

The prefix checker reads the retained closed sets and regenerates their
edges with a cell-by-cell implementation. It checks 13,656 outgoing edge
memberships. It independently enumerates the entire blind-source domain.

The earlier exact common-image language is retained: its finite words are
accepted by the following DFA, all states accepting except dead state 2.
The start state is 0; columns give the successors on 0 and 1:

    0: 1,2    1: 2,3    2: 2,2    3: 4,5
    4: 4,6    5: 2,1    6: 2,7    7: 4,4.

For this theorem retain only accepted words beginning 0111100. This is a
safe overapproximation: not every retained word has to possess a cyclic
raw predecessor. The checker independently regenerates the words from the
16 raw preimage contexts, without calling the DFA producer.

## 4. An inexpensive common-cone certificate

Let C have length r, and encode its first layer as the low bit. Define

    T(z) = (z << 2) XOR ((z << 1) OR z).

At time t after the common row, every site j>2t is still in the common
causal cone, and both raw tracks there equal the corresponding bit of
T^t(C), regardless of the labels. The disagreement at boundary site zero
propagates to site 2t at time t with value one, for 1<=t<=floor(r/2):
left permutivity preserves the rightmost discrepancy, and a label swap
does not change its XOR. Therefore no new blind output is possible at
those times.

Consequently, if bit r-1 of T^h(C) is one for some

    0 <= h <= floor((r-1)/2),                    (3)

the two last-parent raw bits are both one before any earlier possible
blind return. Equation (1) then erases the child difference on that edge.
For odd r the reset edge can itself be the earliest possible blind edge;
its outgoing Y difference is still zero. This proves the required safe
first-return assertion for C.

The checker recomputes (3) using literal cells and zero boundary values
outside the cone, rather than the producer's packed formula. The zero
boundary is legitimate only because j>2t in the checked cone.

Most allowed words pass (3). Only its exceptions require larger closed
first-return sets. In particular, no full product graph at depth 23 is
constructed.

## 5. Complete finite coverage

At depths 7 through 23, the allowed-word counts are, in order:

    1, 2, 3, 5, 9, 15, 25, 43, 73,
    123, 209, 355, 601, 1019, 1729, 2931, 4969.

All words at depths 7-13, 15, 17, 19, and 20 pass the cone test. The
remaining cases, together with the separate depth-six case, have these
verified closed-set sizes:

| Depth | Common word, first layer first | Nonzero-difference states |
|---:|---|---:|
| 6 | 011110 | 109 |
| 14 | 01111000000000 | 8,957 |
| 14 | 01111001111110 | 7,933 |
| 16 | 0111100000000110 | 13,501 |
| 18 | 011110011000000000 | 33,277 |
| 21 | 011110011101110000110 | 61,437 |
| 22 | 0111100000000000000000 | 74,749 |
| 22 | 0111100000000011100000 | 164,349 |
| 22 | 0111100011100001111110 | 74,749 |
| 22 | 0111100111111001111110 | 179,325 |
| 22 | 0111100111111111111110 | 287,229 |
| 23 | 01111001111100000000110 | 229,373 |

There are 1,134,988 states across these twelve sets. The independent
cell-by-cell checker passed all **2,269,976 segment-edge checks**. Together
with the upper-prefix checks this is **2,283,632 checked edges**. These are
certificate checks, not independent random trials or sampled time steps.

The checker validates both labels, the initial difference cases, discarded
zero differences, all continuing nonzero differences, and safe blind exits.
It also checks contiguous depth coverage, complete exception coverage,
source hashes, and hashes of the serialized certificates.

Adversarial controls: a certificate with an initial difference removed,
whose hashes were correctly recomputed, was rejected. A manifest silently
omitting a claimed depth was also rejected.

## 6. Reproduction and provenance

The standalone standard-library script is
`experiments/problem1_nonperiodicity/certify_cyclic_resets_20261016.py`.

    python3 experiments/problem1_nonperiodicity/certify_cyclic_resets_20261016.py generate
    python3 experiments/problem1_nonperiodicity/certify_cyclic_resets_20261016.py verify --part prefix
    python3 experiments/problem1_nonperiodicity/certify_cyclic_resets_20261016.py verify --part segments

Default output is `results/problem1/20261016_cyclic_resets/`. The generated
manifest records the source hash, full base commit, Python, platform,
machine, processor, CPU count, exact parameters, timings, and raw and
compressed certificate hashes. Writes are atomic. Certificates are sorted
little-endian unsigned 64-bit state identifiers, zlib-compressed. The
supplied downloadable package retains the actual certificates and check
records; the repository source regenerates them locally.

Frozen source SHA256:

    f67bf27a0cdbc549b63cdbf9e9f6089fb358ea7fb1c791791fa9e234efdbfc54

This session's full manifest SHA256:

    ffe944152d31b376d58b8ee0a8d844c45605a0c26eb54dbb3df3a0840d1515cf

Generation and verification used Python 3.13.5. The segment verification
was rerun after freezing the final source and passed. This is an independent
code-path check by the same research agent, not a second human or model
review. The full repository test suite and Lean were not run.

Additional exploratory controls, retained in the download, independently
reproduced the old depth-five product counts and found no bad cyclic edge
in the complete product graphs at depths six through eight. Left-half-only
searches also found no infinite survivor within their finite domains; none
of those searches is used in the theorem.

## 7. What did not close

The cone criterion first needs delayed certificates at depth 14. This is
not a counterexample to S14. Exploration at depth 24 encountered the
400,000-state cap for three exceptional words. Those capped cases have no
conclusion; the certified release deliberately stops at depth 23.

The next useful target is an all-width inductive version of the first-return
certificate lemma for the exact common language with prefix 0111100, or a
real counterexample to that stronger segment assertion. Do not assume that
a finite closure pattern extrapolates or that a nonzero-difference cycle
already violates the lemma.

Even S_r for EVERY r would not by itself finish the prize argument. The
unchanged global gap is transport across returns and period doubling
against ONE ORIGINAL finite-support seed. The repository's sufficient
stronger target remains

    limsup_n [tau(2^n v)-n] = infinity, for every fixed finite v>0.

No such original-support resource or universal termination proof is
established here. No prize submission or sponsor contact was made.

Sources inspected: the base-commit all-depth gate candidate, blind-image
language, cyclic cone, and global support bridge notes; the official Rule
30 prize page; and the September 8, 2026 constant-trace preprint,
https://arxiv.org/html/2609.09431v1 . That preprint excludes eventual
constant traces, not nonconstant eventual periods.
