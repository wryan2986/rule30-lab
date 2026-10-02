# Problem 1: reset and full-Y invariance failures, with a weaker repair

Status: FAILED — COUNTEREXAMPLE FOUND for H_reset and general H_Y.
Independent scalar reconstruction and temporal recurrence replay passed.
General H_ext and H_B remain unproved. Problem 1 remains **OPEN**.

## 1. The attempted reset bridge

Fix even p>=2, an odd driver w, and a unique cyclic normalized portal
stack through depth r+1, with all required raw parent tracks nonzero.
At a depth-r blind phase s, every outgoing upper difference D_j(s),
1<=j<=r, is zero. A hidden-label change can inject an X-only difference
at the next layer, at phase s+1, if Y_(r+1)(s+1)=1.

The proposed **H_reset** said: whenever that injection is active, the
depth-r parent encounters a pair (X_r,Y_r)=(1,0) before its first Y_r=1.
Precisely, put

    b=min{j in {1,...,p}: Y_r(s+j)=1},
    b=p+1 if the set is empty,

with phase indices modulo p. The claim was that some j in {1,...,b-1}
has (X_r,Y_r)(s+j)=(1,0).

Such a pair has zero added-layer transfer matrix, so this would erase
the injected X difference before it could create any Y difference.
That explains its relationship to H_Y. This implication mechanism was
not needed for accepting a counterexample to H_reset itself.

## 2. First H_reset failure in the declared search

The first witness in the specified p,r,integer-word,phase order is

    p=10, r=6, w=55,
    w bits LSB-first: 1110110000,
    s=4.

The driver has odd weight five and every raw parent needed through
depth seven is nonzero. Phase s is blind at depth six, and
Y_7(s+1)=1. The depth-six parent trajectory is

| Forward distance j | Phase | (X_6,Y_6) |
|---|---|---|
| 1 | 5 | (0,0) |
| 2 | 6 | (0,0) |
| 3 | 7 | (0,0) |
| 4 | 8 | (0,1) |

Thus b=4 and there is no reset before the first parent Y=1.

The ordered search completed every scope for p=2,4,6,8 and r=1..6,
then p=10, r=1..5, and examined the first 28 odd words at p=10,r=6.
It checked 3,608 driver/depth cases and 2,107 triggered reset predicates,
with no zero-parent exclusions. The p=12,14 scopes were not run after
the witness. This is minimal in the declared search order and bounds,
not a claim of minimum period over all depths.

## 3. Turning the failure into a genuine odd-label-fiber test

The depth-six upper orbit for the base word has only one blind phase,
so its odd fiber is a singleton. H_Y cannot be falsified on that fiber.
Repeat the aligned orbit THREE times instead:

    p=30, r=6,
    W=55+(55<<10)+(55<<20)=57728055.

Its upper orbit has blind phases B={4,14,24}. The fixed nonblind labels
have even weight twelve. Its complete odd fiber is the two-dimensional
cube with exactly four words:

| Integer word | LSB-first driver bits | Weight |
|---|---|---|
| 57728055 | 111011000011101100001110110000 | 15 |
| 57711655 | 111001000011100100001110110000 | 13 |
| 40950823 | 111001000011101100001110010000 | 13 |
| 40934455 | 111011000011100100001110010000 | 13 |

The last three are obtained by flipping one of the three pairs of
blind labels. All four drivers have the SAME complete aligned upper
orbit and a nonzero depth-six parent. This is a four-input construction,
not an enumeration of period-30 words.

Take the two weight-thirteen words 57711655 and 40950823. Their newest
Y_7 histories differ at phases 19 and 29. Therefore **general H_Y is
false** on its stated nonzero-parent, complete odd-fiber domain.
Both words have least period thirty: a repetition count would divide
both thirty and thirteen, whose gcd is one. Restricting the two witness
drivers to full least period does not remove this failure.

The scalar cyclic-child recurrence, tried independently of the packed
implementation, reconstructs all four depth-seven stacks. The original
two-row normalized temporal update closes phasewise on each of them.
Those finite arrays are exact counterexample certificates; no all-depth
extrapolation or first-return parity claim is used.

## 4. What survives, and the precise repair

The four full depth-seven output histories have phasewise XOR zero.
On this exact two-dimensional input cube that proves the extension is
affine. Its rank is two: every old blind phase has outgoing Y_7=1, so
the new blind set is empty and u_7=0, while u_6=2.

At the old blind phases s=4,14,24, every one of the four drivers has

    Y_7(s+1)=1.

All Y differences between these outputs occur among phases 9,19,29,
following nonblind upper phases. Thus the stronger all-phase H_Y fails,
while **H_B**, constant outgoing new difference at each old blind phase,
holds on this fiber. H_B at all fibers remains a conjecture.

An even weaker exact criterion is proved in
`problem1_blind_output_gate_criterion.md`: on any complete upper odd
fiber with nonzero parent, the extension is affine if and only if each
old blind phase's outgoing new difference depends only on that phase's
own label. H_B is its constant-gate special case. The criterion is an
all-depth equivalence, not a proof that the gate condition always holds.

The subsequent independently checked depth-four certificate moves the
first unproved extension depth for the general affine strategy to r=5.
The false H_Y bridge must not be reused. The proven shallow
theorem at r=1,2,3 and the conditional H_Y implication remain valid.

## 5. Reproduction and research relevance

    python3 experiments/problem1_nonperiodicity/check_hidden_label_reset_criterion.py

Atomic record: `results/problem1/20261002_hidden_label_reset_criterion.json`.
It records the stopped ordered search, the four exact targeted inputs,
state and history hashes, independently rebuilt tracks, source hashes,
base commit and resource caps. No p=30 exhaustive search, original
connector traversal, or new computational backend is required.

These failures remove a false sufficient condition without refuting
affine layer transport. A local gate law, even if established at every
depth, would still need transport across zero returns and period doubling
with bounded reuse against the same original finite support.
