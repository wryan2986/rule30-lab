# Problem 1: exact common-output language of blind transitions

Status: `partial-proof` for the exact spatial language below. Independent
review is recorded separately. This is not an affine-extension theorem or a
solution of Prize Problem 1, which remains **OPEN**.

## 1. Why this is on the active proof path

The corrected depth-five product certificate rules out bad gate edges on
cycles at one observer depth. A possible all-depth proof would show that a
hidden interchange of the two raw child bits cannot change their XOR at the
next blind transition. Such a proof must use the actual common row produced
by the first blind transition: an arbitrary equal pair of rows is a larger
domain.

This note characterizes those common rows at every spatial depth with one
fixed automaton. It does not assert a temporal reset or return property.

## 2. Exact local preimage relation

Use the normalized portal convention from
`problem1_portal_multilift_phase_quotient.md`. Put

    a_j = X_j,    b_j = X_j XOR Y_j,

with raw boundaries

    (a_-1,b_-1)=(1,1),    (a_0,b_0)=(0,1).

The two raw updates are

    a'_j = a_(j-2) XOR (a_(j-1) OR a_j),
    b'_j = b_(j-2) XOR (b_(j-1) OR b_j).

A transition is blind through depth r exactly when a'_j=b'_j for every
1<=j<=r. Denote the common output by C_j. Since all output differences
vanish, the subsequent driver-dependent half swap changes none of these
output bits. Thus C is the common postblind row for either label.

For a spatial scan retain the four-bit context

    (h,h',l,l')=(a_(j-2),b_(j-2),a_(j-1),b_(j-1)).

The next two input bits (x,x') are admissible for output c precisely when

    h XOR (l OR x) = h' XOR (l' OR x') = c.        (1)

The next context is (l,l',x,x'). Start in 1101. Every context is accepting
when a finite scan ends. Equation (1), applied successively, proves that
this 16-context nondeterministic automaton recognizes exactly all finite
common output words. Conversely, each accepting path supplies all input
pairs and hence a blind source. This is an induction at arbitrary r; no
depth bound is used.

## 3. An eight-state deterministic description

Here is an explicit subset construction. Context strings below are written
in the order (h,h',l,l'), not integer display order.

| Subset | Raw contexts | Output 0 | Output 1 | Quotient state |
|---|---|---|---|---|
| A0 | {1101} | A1 | A2 | 0 |
| A1 | {0110,0111} | A2 | A3 | 1 |
| A2 | empty | A2 | A2 | 2 |
| A3 | {1000,1010} | A4 | A5 | 3 |
| A4 | {1000,0010,1010} | A4 | A6 | 4 |
| A5 | {0001} | A2 | A1 | 5 |
| A6 | {0001,1001,1011} | A2 | A7 | 6 |
| A7 | {0100,0110,0101,0111} | A8 | A4 | 7 |
| A8 | {0100,0001,0101} | A8 | A9 | 4 |
| A9 | {0010,0110,0111} | A2 | A10 | 6 |
| A10 | {1000,1010,1001,1011} | A4 | A8 | 7 |

Each entry follows by applying (1) to its listed contexts and taking the
union of possible next contexts. The quotient identifies A4 with A8, A6
with A9, and A7 with A10. Identified states have identical acceptance and
transitions into the same quotient classes, so the quotient preserves the
language by induction on the remaining word length.

The resulting table is therefore an exact all-depth description:

| State | Read 0 | Read 1 | Accepting at finite end? |
|---|---:|---:|---|
| 0, initial | 1 | 2 | yes |
| 1 | 2 | 3 | yes |
| 2, dead | 2 | 2 | no |
| 3 | 4 | 5 | yes |
| 4 | 4 | 6 | yes |
| 5 | 2 | 1 | yes |
| 6 | 2 | 7 | yes |
| 7 | 4 | 4 | yes |

No minimality claim is needed for the proof. The implementation also obtains
eight states by exact Moore minimization.

## 4. Run-length form

Every nondead state has an infinite continuation. Hence the finite language
is the prefix language of the following infinite words:

    01(111)^omega,

or

    01(111)^k 0 v,    k>=0,
    v in {0,110,111}^omega.                       (2)

Here omega means infinite repetition/concatenation, with an arbitrary choice
of the three blocks in the second line. To see (2), the initial 01 reaches
state 3. State 3 can make a 111 loop, or read 0 and enter state 4. At state
4 the return blocks are precisely 0,110,111, and it never returns to state
3. Incomplete return blocks are permitted when taking finite prefixes.

For completeness, an infinite word whose finite prefixes are accepted also
has a consistent infinite raw preimage pair. Its finite raw preimage paths
form a finitely branching tree with a node at every depth. An infinite path
exists by the elementary finite-branching tree lemma. Thus the infinite-word
description concerns actual infinite raw rows, not merely separately chosen
finite witnesses.

Equivalently, a common infinite row begins with one zero. If its first run
of ones ends, that run has length 1 modulo 3. Every later completed
positive run of ones has length 0 or 2 modulo 3. An infinite final run of
ones is also allowed. For finite observations these restrictions apply only
to completed runs, not to an unfinished terminal run.

Immediate consequences include

    C_1=0, C_2=1                    when r>=2,
    C_3=1 implies C_4=1             when r>=4.

Thus the arbitrary equal row 0000 and the row 0110 are not valid depth-four
postblind starts. They cannot be used as counterexamples to a theorem
whose source must be a blind transition.

The language includes 01000... and arbitrarily long zero runs. It supplies
no uniform reset time merely from the length of the visible prefix. In
particular, it does not restore the already refuted claim that every active
child impulse is reset before ever reaching a nonzero parent difference.

## 5. Verification and remaining obligation

Reproducer:

    python3 experiments/problem1_nonperiodicity/analyze_blind_image_language_20261008.py

Atomic record:

    results/problem1/20261008_blind_image_language.json

The record contains all 32 local paired transitions, all 11 reachable
subsets, their quotient map, hashes, full base commit, resource limits,
software/hardware facts, and timing. Independent literal checks compare the
automaton language with every paired input through r=8. The numbers of
distinct output words for r=1,...,8 are

    1,1,2,3,4,7,12,19.

Those finite comparisons corroborate the construction; the arbitrary-depth
claim follows from the local path correspondence and the checked quotient
above.

The unqualified temporal continuation proposed during this session is now
**refuted**: a genuine depth-five postblind row `01000`, followed by labels
`11100`, gives unequal last-parent no-reset products at its next blind
transition. The source is transient in the upper graph. It therefore does
not refute the cyclic gate theorem. See
`problem1_all_depth_gate_candidate.md` for the exact raw replay and the
essential recurrence restriction.

The spatial language (2) remains exact. A cyclic source lies in a smaller
domain, so an all-depth temporal argument must retain its recurrence
constraints. Even an all-depth affine extension theorem would leave the
original-support obstruction across zero returns and period doubling
unresolved.

## 6. Eventually-zero common rows have one finite and one cofinite preimage

There is a further exact distinction between finite observed prefixes and a
complete finite-support common row. Suppose an infinite common output satisfies
`C_j=0` for every `j>=N`, with `N>=1`. Each individual raw row then obeys

    a_(j-2) = a_(j-1) OR a_j,      j>=N.

For the successive two-bit states this zero-output constraint has precisely
the transitions

    00 -> 00,   01 -> no successor,
    10 -> 01,   11 -> 10 or 11.

Only the constant `00` and `11` paths can continue indefinitely. A path
leaving `11` reaches the dead state after two steps. Consequently each raw
row is constant already from index `N-2` onward.

The two constants must be opposite. Otherwise, because `a_0=0` and `b_0=1`,
there would be a rightmost differing input index `k>=0`. At output index
`k+2`, the two left inputs differ and both of the other inputs agree.
Left permutivity of `F(h,l,x)=h XOR (l OR x)` would make those two outputs
differ, contradicting the common output. Thus one raw preimage is eventually
zero and the other eventually one.

Moreover, the ordered raw preimage pair is unique. Once an individual row's
constant tail has been specified, the backward recurrence

    a_(j-2) = C_j XOR (a_(j-1) OR a_j)

determines it uniquely all the way back to index `-1`. There are only two
tail choices. A valid pair uses both, and the boundary values `a_0=0`,
`b_0=1` determine their order. For every eventually-zero infinite word in
(2), existence follows from the finite-branching argument above, so there
is exactly one ordered raw preimage pair satisfying the boundary conditions.

This is a theorem about a complete infinite spatial output. It cannot be
applied merely because a finite observed prefix ends in zeros. It also does
not supply an original-support budget for the actual Rule 30 orbit: the two
raw portal rows need not both be finite-support physical rows.
