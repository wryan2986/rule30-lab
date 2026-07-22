# Problem 1: depth-independent sideways invariants

Status date: 2026-07-21

## Result in one sentence

The search found an exact depth-independent four-forbidden-block subshift for
adjacent temporal columns and an all-period exclusion theorem for the stronger
model in which both starting columns are exactly cyclic. It did **not** bridge
the transient, potentially nonperiodic right-neighbor column forced by the
actual zero right half-line, so it does not prove Rule 30 center
nonperiodicity.

The implementation is
[`search_sideways_invariants.py`](../experiments/problem1_nonperiodicity/search_sideways_invariants.py).
It emits deterministic JSON, performs no writes, and stops before crossing any
configured linear-system, truth-table, image-state, or cyclic-state cap.

## Sideways dynamics as a second-order cellular automaton

Let (A_t) be a temporal column and (B_t) its right neighbor. One step to
the left produces (L_t), with

\[
L_t=A_{t+1}\mathbin{\mathsf{xor}}(A_t\mathbin{\mathsf{or}}B_t),
\qquad (A,B)\longmapsto(L,A).
\]

A pair symbol is encoded by the integer

\[
s_t=A_t+2B_t\in\{0,1,2,3\}.
\]

This representation makes three distinct notions of “depth-independent”
precise:

1. a local density whose sum is conserved for arbitrarily many leftward
   steps;
2. a finite summary with an autonomous update that can be iterated without
   increasing its temporal window; or
3. an invariant set of a fixed-period finite model that is closed for
   infinitely many leftward steps.

The searches below test these notions separately. None silently substitutes a
fixed temporal width for the semi-infinite reconstruction problem.

## Exact local GF(2) parity search

For phase period (r) and density width (w), the search considers every
Boolean density

\[
q_i(s_t,\ldots,s_{t+w-1}),\qquad i=t\bmod r.
\]

It asks whether the XOR sum of this density around a cyclic temporal word is
preserved by one sideways step. This is not checked by sampling cycle lengths.
The program solves the exact de Bruijn coboundary equations

\[
q_i(\text{old})+q_i(\text{new})
=h_i(\text{prefix})+h_{i+1}(\text{suffix})
\]

over GF(2) on every length-(w+1) pair-symbol block. The right side telescopes
on every cycle. Therefore every solution is conserved for every compatible
cycle length and arbitrarily many leftward steps. The bounded part of the
claim is the selected density width and phase period, not the evolution depth.

The default run solved all 12 systems with (1\le r\le4) and
(1\le w\le3). Exact results were:

| Phase period (r) | Width (w) | Equations | Unknowns | Conserved-density rank | Trivial rank | Quotient rank |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 16 | 8 | 1 | 1 | 0 |
| 1 | 2 | 64 | 32 | 4 | 4 | 0 |
| 1 | 3 | 256 | 128 | 16 | 16 | 0 |
| 2 | 1 | 32 | 16 | 2 | 2 | 0 |
| 2 | 2 | 128 | 64 | 8 | 8 | 0 |
| 2 | 3 | 512 | 256 | 32 | 32 | 0 |
| 3 | 1 | 48 | 24 | 3 | 3 | 0 |
| 3 | 2 | 192 | 96 | 12 | 12 | 0 |
| 3 | 3 | 768 | 384 | 48 | 48 | 0 |
| 4 | 1 | 64 | 32 | 4 | 4 | 0 |
| 4 | 2 | 256 | 128 | 16 | 16 | 0 |
| 4 | 3 | 1,024 | 512 | 64 | 64 | 0 |

“Trivial” here means a phase constant or a temporal coboundary whose cyclic
sum is state-independent or identically zero. Thus the search found no
nontrivial local parity invariant in this ansatz. This is an exact exhaustive
negative result for the stated 12 finite-dimensional spaces, not evidence
that wider, integer-valued, nonlinear non-additive, or nonlocal invariants do
not exist.

Each system records SHA-256 hashes of its canonically ordered equation matrix,
conserved-density basis, and trivial-density basis. An identity-map positive
control has quotient rank 3 at width one, while the width-one density (q=A)
has the explicit negative-control cycle

```text
old pair symbol [1] -> new pair symbol [2], total 1 -> 0.
```

## Exact image subshift: a positive invariant structure

Writing an output pair symbol as ((L_t,A_t)), eliminate the old (B_t) from
the local equation. Two adjacent output symbols are possible exactly when

\[
A_t=0
\quad\text{or}\quad
L_t=1\mathbin{\mathsf{xor}}A_{t+1}.
\]

Under the integer encoding above, the four forbidden adjacent symbol pairs
are

```text
(2,0), (2,1), (3,2), (3,3).
```

This is an exact shift of finite type with 12 allowed edges. Every one of the
four symbols has exactly three incoming edges, so the number of admissible
width-(w) words is

\[
4\cdot3^{w-1}.
\]

The implementation independently enumerated every old window and both unseen
right extensions through width 8. Direct images equaled the local-constraint
language exactly, with counts

```text
4, 12, 36, 108, 324, 972, 2916, 8748.
```

The local derivation—not the width-8 enumeration—makes the four-block
exclusion depth-independent: after every sideways step, the new adjacent
column pair belongs to the same subshift.

This explains the exhaustive Boolean-summary result. At width two there are
32 closed one-bit predicates: two constants, 15 nonempty predicates supported
on subsets of the four forbidden blocks, and their 15 nonconstant complements.
Every nonconstant predicate becomes constant after one step. No persistent
nonconstant summary was found among:

- all affine one-bit summaries through width 5; or
- all Boolean one-bit summaries through width 2.

The subshift is real structure, but it does not yet separate the desired
initial condition. If two adjacent reconstructed initial bits are both zero,
their time-zero pair symbol has high bit zero, making the constraint vacuous.

## Why a raw bounded temporal window is not a state

There is a minimal exact obstruction at every width (w\ge1). Take a visible
pair window with every (A) and (B) bit zero. Consider two extensions that
differ only in the unseen bit (A_{t+w}). Their current visible windows are
identical, but their next windows differ at (L_{t+w-1}).

Therefore a complete width-(w) next window cannot be computed from the
complete width-(w) current window. One more temporal bit is needed after each
leftward step. This proves that the obvious lossless state size is not
depth-independent. It does not rule out a lossy quotient; that is why the
separate affine and Boolean quotient searches were performed.

## Infinite-depth fixed-period cycle certificates

For a fixed temporal period (p), the cyclic-pair model has (2^{2p}) states.
The exact transition wraps (A_{p}) to (A_0). Starting with the safe
predicate (A_0=0), the program repeatedly removes any state whose successor
is not safe. The fixed point is the greatest set whose orbit keeps (A_0=0)
for infinitely many leftward steps; this is stronger than a finite-horizon
orbit check.

For every (1\le p\le8), the greatest forever-safe set contained only the
all-zero state, and no state with center bit (A_0=1) had a successor in that
set:

| (p) | States | Forever-safe states | Maximum first nonzero-left depth from (A_0=1) |
|---:|---:|---:|---:|
| 1 | 4 | 1 | 2 |
| 2 | 16 | 1 | 2 |
| 3 | 64 | 1 | 5 |
| 4 | 256 | 1 | 7 |
| 5 | 1,024 | 1 | 6 |
| 6 | 4,096 | 1 | 7 |
| 7 | 16,384 | 1 | 10 |
| 8 | 65,536 | 1 | 12 |

The JSON contains canonical hashes of every successor table, greatest-safe
membership vector, removal-round certificate, and ordered first-witness list.

There is also a short all-period proof for this stronger model. Assume the
center and its right neighbor are both exactly (p)-cyclic. Every column
reconstructed to the left is then (p)-cyclic. If (x_0(0)=1) and every
initial cell to its left is zero, then after one forward step the left half has
a single leading one at (x_{-1}(1)). The left edge propagates at unit speed,
so

\[
x_{-p}(p)=1.
\]

But (p)-cyclicity of that reconstructed column gives

\[
x_{-p}(p)=x_{-p}(0)=0,
\]

a contradiction. The finite fixed-point searches are independent bounded
checks of this conditional argument.

## Why the conditional theorem does not solve Problem 1

An eventually periodic center trace constrains only (x_0(t)). The actual
right neighbor (x_1(t)) is generated by a semi-infinite zero right half under
that boundary. It can have a transient, a different eventual period, or no
known eventual period at all. Periodic forcing of an infinite-state system
does not imply a periodic response.

Consequently, the pair ((x_0,x_1)) need not be one of the cyclic states above,
and the all-period conditional theorem cannot be applied. This is the precise
missing bridge—not merely an untested larger period.

The strongest next theoretical target is therefore one of:

1. control the forced right-neighbor transient under an eventually periodic
   center boundary;
2. extend the four-block image subshift with a monotone potential or forbidden
   cycle that remains meaningful across transient seams; or
3. find a wider or non-additive finite quotient with a persistent distinction,
   then prove that its state is determined despite the unseen temporal bit.

## Follow-up: first witnesses collapse to prefix disagreement

The subsequent causal/permutivity proof in
[`problem1_sideways_prefix_equivalence.md`](../proofs/informal/problem1_sideways_prefix_equivalence.md)
clarifies what the existing finite first-witness searches measure. For any
finite proposed trace with the required `c0=1`, the first nonzero reconstructed
left depth is exactly the first index at which that trace differs from the
true single-cell center prefix. An exhaustive cross-check covered all 262,142
binary traces through every horizon 0 through 16, with no disagreement, while
the proof is horizon-independent.

Thus first-witness histograms are exact certificates but not independent
structural evidence. The genuinely stronger sideways target is to prove that
an eventually periodic proposal reconstructs a left tail with infinitely many
ones (or at least a tail that is not eventually zero). The finite equivalence
does not settle that statement.

## Reproduction

Run the focused tests:

```bash
cd /home/wryan/rule30-lab
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest \
  -p no:cacheprovider tests/python/test_sideways_invariant_search.py -q
```

Current result:

```text
10 passed in 2.00s
```

Emit the default deterministic JSON:

```bash
cd /home/wryan/rule30-lab
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/search_sideways_invariants.py \
  > /tmp/sideways-invariants-default.json
sha256sum /tmp/sideways-invariants-default.json
```

With the implementation bytes documented here, the formatted JSON is 51,754
bytes and has SHA-256

```text
cf11013c9e10bde388b5ff2791ff8466217be0e79f3245ec4f2b757c48038906
```

The measured default run took 3.08 seconds and 36,216 KiB peak RSS on the
documented local WSL environment. Runtime is descriptive; the JSON itself
contains no timestamp or timing field and is deterministic.

Raise caps explicitly. For example, a request whose Boolean truth-table family
or cyclic state space exceeds its configured cap fails before enumeration.
No output from this script should be labeled a proof of Rule 30 center
nonperiodicity.
