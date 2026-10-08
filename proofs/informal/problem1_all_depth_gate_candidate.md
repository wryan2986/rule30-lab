# Blind-gate transport: a short S4/S5 proof and a transient reset counterexample

Status: `partial-proof` relative to Prize Problem 1, which remains **OPEN**.
The later human proof of S4 and S5 applies at every presentation period
and was independently re-derived by the parent researcher. The unrestricted
segment candidate is `refuted`. The all-depth S_r conclusion remains
`inconclusive`.

## Scope and admission

The target is the stronger product-graph statement S_r: at every depth
r>=2, no directed cyclic history of two depth-(r+1) stacks sharing the
complete depth-r upper orbit contains an upper-blind edge with equal
labels and unequal outgoing added Y bits. There are no parity or
nonzero-parent restrictions in S_r.

The proposed bridge was a reset law between successive collisions of the
two raw upper rows. A small exact check refutes its unrestricted version
and separates transient paths from the actual cyclic domain. A second
derivation proves S4/S5 directly from shallow recurrence, independently of
their large finite rank certificates. Neither result proves S_r at all
depths or provides an original-support transport law.

## Raw segment reduction

Write q_(t+1)=q_t+w_t and the raw parent-half bits

    u_t=L_t+q_t M_t,  v_t=L_t+(q_t+1)M_t.

For a common-label segment, differences between two added raw half
histories evolve independently as

    delta z_(t+1)=(1+u_t)delta z_t,
    delta z'_(t+1)=(1+v_t)delta z'_t.

A change of the hidden label at an upper-blind transition swaps the two
new raw child outputs. If their XOR is one, this creates the difference
vector (1,1); otherwise it creates zero. Starting from (1,1), the
outgoing added Y difference after a segment is therefore

    d_0+d_1,
    d_0=product_t(1+u_t), d_1=product_t(1+v_t).

Thus equality of the two last-parent no-reset selectors on each
collision-to-collision segment would annihilate every hidden-label
impulse at the next blind gate. Any surviving seed difference must still
be treated separately on arbitrary product cycles; odd-driver unique
extension removes it on the intended odd nonzero-parent fiber domain.

Failed candidate segment law: after a depth-r upper-blind transition, and up to
and including the next depth-r upper-blind transition, the last raw parent
halves have equal no-reset selectors, for every r>=2 and every intervening
label history. This is stronger than a statement restricted to upper
cyclic histories and is refuted by the exact depth-five transient below.

The postblind common raw upper row is constrained. At all r>=2 its first
two bits are (0,1). Arbitrary equal-start/equal-end raw strips do not
satisfy the proposed law: at r=2, start from equal row (0,0), use alternating
q starting at zero, and the two raw rows reunite after four updates while
the second coordinate of one half remains zero and the other visits one.
The initial row (0,0) cannot occur immediately after a depth-two blind
transition. Any proof must use genuine postblind reachability.

## Exact shallow observation

At r=2 the postblind last parent pair is (1,0), so both halves reset
immediately. At r=3, if the postblind last pair is (0,0), the fixed upper
prefix (0,0),(1,0) forces the following last pair to (1,0). If the
postblind last pair was already (1,0), both resets are immediate. The
next depth-three blind cannot precede this reset. These are direct local
proofs at two depths; they do not yet give a spatial induction.

## Regular-language approach, conditional

Use ordered raw row-pair letters x+2y. A designated-half no-reset segment
is represented by two regular languages R0,R1: the last x coordinate has
remained zero in both; the last y coordinate has never been one in R0 and
has been one at least once in R1. Initially R0 consists of genuine common
postblind words of length at least two ending in zero, and R1 is empty.

For either complementary boundary choice q, the raw simultaneous update
is a deterministic finite radius-two word transducer. Let F be the union
of its two exact image operations. The exact forward updates are

    R0 <- R0 union (F(R0) intersect {last letter 00}),
    R1 <- R1 union (F(R0) intersect {last letter 01})
             union (F(R1) intersect {last x=0}).

Here 01 denotes the ordered last bits x=0,y=1 (alphabet letter two).
A reset-selector counterexample is possible precisely if F(R1) contains
an entirely diagonal word. Intermediate blind transitions with neither
half reset can be traversed; hence this is a safe strengthening of the
consecutive-blind question, rather than an assumption that every return
has both halves reset.

If regular overapproximations R0,R1 contain the initial language, are
closed under these updates, and F(R1) is disjoint from diagonal words,
they certify equality of the reset selectors at all spatial depths.
All three inclusions must be checked exactly. A finite depth sweep is
unnecessary. Exact forward closure currently grows rapidly; a sound
finite-lookahead quotient can merge DFA residual states to an NFA,
which only adds words. Its determinization is an overapproximation. Such
widening is useful only if the resulting languages stabilize and pass
the exact safety/inclusion checks; any spurious bad word is inconclusive.

## Shallow recurrence on all cycles containing a blind phase

The first layer can have only a=(0,0), b=(0,1), c=(1,1) on a cycle.
State(1,0) has no predecessor. Encode the first two pairs by

    u=X_1+2Y_1+4X_2+8Y_2.

Restricting the first layer to a,b,c gives this complete table. The other
four depth-two states have first pair(1,0) and cannot occur on a cycle.

| u | first pair | second pair | T_0(u) | T_1(u) |
|---|---|---|---:|---:|
| 0 | a | (0,0) | 11 | 14 |
| 2 | b | (0,0) | 3 | 2 |
| 3 | c | (0,0) | 4 | 4 |
| 4 | a | (1,0) | 15 | 10 |
| 6 | b | (1,0) | 15 | 10 |
| 7 | c | (1,0) | 12 | 8 |
| 8 | a | (0,1) | 3 | 2 |
| 10 | b | (0,1) | 3 | 2 |
| 11 | c | (0,1) | 12 | 8 |
| 12 | a | (1,1) | 7 | 6 |
| 14 | b | (1,1) | 15 | 10 |
| 15 | c | (1,1) | 4 | 4 |

After excluding first-pair(1,0), state0 has no predecessor, so states11
and14 cannot occur on a cycle either. States6 and8 enter the closed
five-state set {2,3,4,10,15} and cannot return. The only cyclic components
are that five-state set and the extra two-cycle7↔12 using label zero.
The extra component has no blind phase: the only depth-two blind states
are3 and15. Consequently EVERY cyclic upper history containing a blind
phase stays in the five-state component, regardless of driver parity.

Call state4 A, state3 D, and state15 E. In the five-state component E can
only be entered from A. At A the layer-three update is the constant
pair(1,0), independent of its seed and label. Hence every cyclic visit
to E has third pair(1,0). At E the layer-three outgoing difference is
X_3+Y_3=1, so E is never blind through depth three. At D that difference
is1+Y_3. Therefore, at EVERY depth-r blind phase on ANY cyclic upper
history, with r>=3, the first three normalized input pairs must be

    (1,1),(0,0),(x,1), x in {0,1}.

Their numeric depth-three encodings are35 or51. This conclusion requires
cyclicity with a blind phase. It fails on arbitrary transient states and
cannot be inferred merely from the generic common-image language.

## Two more forced ones in the common postblind row

At such a cyclic blind phase choose input gauge q=0. Its first three
ordered raw pairs are(1,0),(0,0),(x,x+1). The common output begins01(1+x).
Equality of the two raw outputs forces its fourth and fifth bits to be
one whenever those layers are present. There are two cases.

If x=1, the third input raw pair is(1,0), and C_3=0. Let the fourth input
raw pair be(a,b). Its outputs are(1,b), so equality forces b=1 and C_4=1.
Write the fifth input raw pair as(c,d). Its outputs are

    1+(a OR c), 1.

Equality forces a=c=0 and C_5=1.

If x=0, the third input raw pair is(0,1), and C_3=1. The fourth outputs
are(a,1), so equality forces a=1 and C_4=1. The fifth outputs are

    1, 1+(b OR d).

Equality forces b=d=0 and C_5=1. Thus every cyclic blind common output
at depth at least five begins01011 or01111. At depth four its fourth
output pair is(1,0); at depth five its fifth output pair is(1,0). The
fourth-layer implication does not require the fifth layer to exist.

## Human proof of S4 and S5 at every period

Fix r=4 or5 and a directed cyclic product history. If its upper projection
has no blind phase, it has no bad edge by definition. Otherwise the
preceding classification applies, and each blind transition is followed
by a shared last-parent pair(L,M)=(1,0).

The added-pair difference on an equal-label transition is

    delta Y'=M delta X+(1+L+M)delta Y,
    delta X'=(1+L)delta X+w delta Y'.

Both rows vanish when(L,M)=(1,0), so the transition immediately following
every blind phase resets the entire added difference to zero. That
following upper phase is nonblind: after a blind transition X_1=0, and
its next D_1=1. Therefore its two labels must agree on a retained edge.

Between this reset and the next upper-blind phase all intervening phases
are nonblind, so the labels agree and equal added pairs remain equal.
At the next blind phase their outgoing added Y values are equal before
either current label is applied. Use the cyclicly preceding blind phase
for every blind visit, including wraparound and a cycle with one blind
visit. This removes arbitrary cyclic seed differences; no odd-driver
uniqueness assumption is used. Thus no bad edge lies on the cycle.

This proves S4 and S5 at EVERY period. The existing gate criterion then
gives the usual all-period odd-fiber affine extensions at those depths.
It is a fixed-depth theorem at two depths, not a spatial induction.

## Refuted unrestricted reset law: exact transient witness at r=5

Start with blind normalized upper state255. Its postblind state is4.
Use segment labels11100. The upper states, including the final common
output, are

    4 → 90 → 162 → 194 → 995 → 340.

The final edge's source995 is blind and the four intermediate sources
are nonblind. Start raw gauge q=0 after the first collision. The two raw
upper rows at the five segment inputs are:

| t | q | raw half A | raw half B | last A | last B |
|---:|---:|---|---|---:|---:|
| 0 | 0 | 01000 | 01000 | 0 | 0 |
| 1 | 1 | 11110 | 00110 | 0 | 0 |
| 2 | 0 | 00000 | 10110 | 0 | 0 |
| 3 | 1 | 10000 | 00010 | 0 | 0 |
| 4 | 1 | 00100 | 10011 | 0 | 1 |

Thus(d_0,d_1)=(1,0). The final common output word is01111, encoded340.
Displayed words are spatial order, first layer first.

This is also a real transient product bad path. At upper255 use the same
initial added pair(0,0) and labels0,1 in the two copies. Its gate is one,
so their new pairs are(1,1),(0,1), creating normalized difference(1,0).
Use common labels1110 on the next four transitions, then common label0
at blind995. The outgoing added Y values on that final edge differ.
Both copies have equal upper outputs at every step. The reproducer checks
the complete six-edge product path using separate raw-row updates.

The path cannot belong to a product cycle. A complete forward-closed
upper set of75 states contains its end340 and excludes its start4 and
source255. The exact set is retained in the JSON, and every outgoing
edge is checked to remain inside it. No continuation from340 can return
to4 or255. A simpler shallow diagnosis is that upper255 has low depth-three
state63=(11,11,11), violating the cyclic blind prefix proved above.

This refutes the unrestricted segment law. It does not refute S5, which
has just been proved, or affine extension on a complete odd cyclic fiber.

## Remaining all-depth status and exact regular-language outcome

The weaker candidate that every collision segment on a CYCLIC upper
history has equal reset selectors remains unproved. Requiring both
selectors zero would dispose of arbitrary cyclic seeds and prove S_r.
Mere equality also permits(1,1), so a surviving seed term must be handled
before claiming S_r. On an odd-label fiber with nonzero parent, a fixed
odd base driver's monodromy erases homogeneous seeds after two aligned
periods. Equal-selector propagation would then annihilate every blind
impulse at later blind gates and prove blind-gate invariance. This is an
all-depth CONDITIONAL implication, not a proof of the selector hypothesis.

The regular initial language was restricted to the cyclicly necessary
first three input pairs above. It represents all spatial widths by exact
local preimage chaining, without a depth cutoff. Exact forward closure
did not stabilize. Completed R0 DFA sizes were12,33,144,676,4445; R1 sizes
were1,1,1,12,18, where a one-state rejecting DFA means empty. The next
image determinization reached the explicit8192 subset-state cap. The
completed images yielded no defect. This is a finite number of temporal
image stages over unbounded spatial words, not an all-time invariant.

Restricted lookahead-two widening produced candidate diagonal word0111
at iteration five. It is spurious by the S4 proof: the abstraction can
shorten words and loses reachability information. Backward exact preimage
closure also grew rapidly and supplied no closed invariant. These
outcomes refute no cyclic statement at any new depth.

## Reproduction, independent controls, and limits

Owned reproducer:

    experiments/problem1_nonperiodicity/explore_all_depth_gate_candidate.py

Final-source retained records:

    results/problem1/20261008_blind_return_segment.json
    results/problem1/20261008_blind_return_regular.json

Exact reproduction commands, using the same 30-second wall cap as both
retained records:

```bash
python3 experiments/problem1_nonperiodicity/explore_all_depth_gate_candidate.py --depth 5 --time-cap 30 --out results/problem1/20261008_blind_return_segment.json
python3 experiments/problem1_nonperiodicity/explore_all_depth_gate_candidate.py --regular --canonical-prefix --iterations 8 --state-cap 8192 --time-cap 30 --out results/problem1/20261008_blind_return_regular.json
```

The first runs at depth five, replays both raw parent halves and the
actual added-copy product, and retains the 75-state non-return certificate.
The second performs the restricted all-width regular-language exploration.
Both include final source hash, full base commit, immutable reference
hash, exact limits/parameters, hardware/software facts, timing, payload
hash, and atomic writes. Small independent raw truth-table controls check
the16-state depth-two table, all its cyclic states by direct reachability,
eight layer-three A resets, and the four depth-five blind sources with
the required shallow prefix. Their status is `finite-exhaustive`; the
all-period result follows from the human proof rather than those counts.

Frozen reproducer SHA256:

    ae47184a179ec98ce2871fc1d97d269ef7eea9e0a8c85ad69465f2873d3efb70

The parent independently confirmed the displayed raw counterexample table,
the non-return certificate, the shallow transition classification, and the
human S4/S5 algebra. This review supports those precise claims; it does
not verify an all-depth selector hypothesis or an inductive regular closure.

No cross-return label transport, bounded-reuse charge on the SAME ORIGINAL
finite support, or Rule30 Prize Problem solution is established. The
all-depth S_r target and Problem1 remain open.
