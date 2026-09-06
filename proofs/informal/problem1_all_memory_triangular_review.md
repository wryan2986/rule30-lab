# Explicit bit and circulation steps in the all-memory obstruction

Status: `partial-proof` for these expanded dependencies of
`problem1_all_residue_memory_rigidity.md`. This is a proof audit, not a
new weight search, a broader certificate class, or a Problem 1 solution.

## Scope and disposition of the earlier criticism

The fresh initial Muse report in this round requested explicit proofs of
triangular slice bijection, fiber compatibility and cycle decomposition.
Its followup failed with provider429 before producing a supplementary
file. The lead supplies the essential derivations here. The report's
claim that subtracting a cycle inverts the needed sign is rejected:
the original subtraction has the correct direction, as expanded below.
Calling for an expanded justification is distinct from finding a false
source inference. No old finite controls are rerun for this audit.

The later explicit rational ut cycle also shortens the old closing
residue argument. Keep H (word scanner), A (its endpoint map), and F
(forced update with a birth letter) separate throughout.

## 1. Unit-diagonal slices at every width (`partial-proof`)

Write x_i for bit i of x, with negative-index bits zero. Directly,

    T(x)_i=x_i XOR (x_(i-1) OR x_(i-2)).

U differs from T only at bit0. P has bits
`P(x)_0=x_0 XOR1`, `P(x)_1=x_1 XOR1`, and the same formula as T
at i>=2. Thus for every G in {T,U,P},

    G(x)_i=x_i XOR f_(G,i)(x_0,...,x_(i-1)).        (1)

Consequently G is compatible with reduction modulo every 2^M, and
its first M output bits determine its first M input bits successively.
This proves both congruence preservation and permutation at every width.

For A(x)=T(x)>>2,

    A(x)_i=x_(i+2) XOR (x_(i+1) OR x_i).

Induct on r. In `A^(r+1)(x)_i`, the first term
`A^r(x)_(i+2)` contains x_(i+2r+2) with coefficient one, while the
other two terms use only lower input bits. Therefore

    A^r(x)_i=x_(i+2r) XOR f_(r,i)(x_0,...,x_(i+2r-1)). (2)

Composition with (1) similarly gives

    (A^(r-1)G(x))_i
       =x_(i+2r-2) XOR h_(r,G,i)(x_0,...,x_(i+2r-3)). (3)

These are all-bit inductive identities, not conclusions from the old
small section checks.

Fix x=q0 modulo2^b, and lift uniformly modulo2^(b+2r), where
2r-2>=b. Conditional on all bits below2r, (2) is a unit-diagonal
b-bit map on the free bits at2r,...,2r+b-1. Hence A^r(x) modulo2^b
is uniform. Conditional on the bits below2r-2, (3) at i=0,1 is
a two-bit bijection on the FREE bits at2r-2,2r-1. Thus
`A^(r-1)G(x) mod4` is uniform on four values. It uses no bits
at or above2r, so the transformed prefix is independent of it.

After applying S=(t,u,p,p), the joint law is exactly a uniform
2^b-state prefix and letter probabilities (1/4,1/4,1/2), for EVERY
original q0 and G. The threshold ensures those two bits were not
pinned by q0. This proves the source averaging lemma with its actual
normalization, including the distinction between prefix and letter.

## 2. Positive circulation and the sign (`partial-proof`)

For the source six-pass difference d6, use the graph modulo2^(b+12),
b>=4. Put flow1 on each T and U edge and flow2 on each P edge.
Each generator is a permutation by (1), so this is an everywhere
positive circulation. Conditional on the lower12 input bits, the
upper b bits make A^6(x) uniform by (2). For any fixed input generator,
the lower12-bit choices emit t,u,p respectively1024,1024,2048 times,
by (3) on the decisive bits10,11.

For each transformed prefix residue the total weighted emitted counts
are therefore4096,4096,8192, the same as the original counts. Thus
the circulation has total d6-weight zero for every weight table.

Under universal strict accepted-block descent, every directed cycle
C has d6-weight <=0. Indeed all-width controllability connects the
root to C and C to the accepting residue. Repeating C arbitrarily
many times leaves that residue and its six birth costs fixed. A
positive cycle would eventually make the accepted change positive.
This uses the fixed-age pullback at six ACTUAL gates, not a longer
forced continuation.

Now choose epsilon>0 so that subtracting epsilon copies of the edge
multiplicity vector of C leaves the positive circulation nonnegative.
The remainder is still a circulation. Every finite nonnegative
circulation decomposes into directed cycles: follow positive edges
until a vertex repeats, subtract the smallest edge amount on that
cycle, and repeat; at least one positive edge disappears each time.
All those cycles have weight <=0. Hence

    0-epsilon*weight(C) <= 0,
    weight(C) >= 0.                                 (4)

Together the inequalities give weight(C)=0 for EVERY C. There is
no reversal error. Closing any two paths with a common return path
then proves path independence and d6=psi(source)-psi(destination).

## 3. Pure iteration and lifted-cycle conservation (`partial-proof`)

The identities pi G=A and
`A(4v+d)=G_(S_d)(v)` give

    A(G(x))=G_(S_(G(x) mod4))(A(x)).                 (5)

Both phase roots are fixed by A. Thus iterating the d6 coboundary
along PURE scanner images telescopes to the source equation (6)
at r=6n. No birth letters or additional actual gates appear in this
iteration. Choose n so that2r-2>=b and apply section1's joint law.

For any M>=b, (1) maps the fiber above a residue q bijectively onto
the fiber above G(q): reduction gives containment, and injectivity
plus equal finite cardinalities gives equality. Uniformly lifting
every edge of a base cycle therefore gives a circulation modulo2^M.
This FIBER statement is separate from the joint scanner averaging.

Summing the source pure-scanner coboundary over those lifts cancels
its endpoint terms. The mean transformed cost is

    c=sum_q[omega(q,t)+omega(q,u)+2omega(q,p)]/(4*2^b).

For every base cycle, its ORIGINAL cost consequently equals c times
its length. Strong connectivity gives
`omega(q,g)=c+phi(q)-phi(G_g(q))`. In particular omega=1 gives c=1
and cycle cost equal to cycle length, not zero. The original cost
must not be dropped in this averaging step.

## 4. Explicit requested-memory closure (`partial-proof`)

The independently reviewed note
`problem1_boundary_sum_periodic_tail_probe.md`, sections1--3, proves

    X=-7/127 --u--> Y=-123/127 --t--> X,
    X=50055 mod65536.

This is an exact rational infinite-support cycle. On every permitted
input, pi F=A^2 and F has low pair11, hence F=4A^2+3. Agreement
through b+2 bits implies output agreement through b bits (b>=2),
because A^2 loses at most four and multiplication by4 restores two.

For each b>=4 let a=X modulo2^(b+12). Controllability supplies an
ordinary finite word from either phase whose endpoint x is congruent
to a. These low bits fix the six actual gates ututut, the accepting
class50055, and F^6(x)=X=x modulo2^b. No representative is declared
ordinary merely because it is the least nonnegative residue.

For the rigid weight table above, a word of length n has cost
`cn+phi(root)-phi(endpoint)`. Boundedness below for ALL ordinary
lengths forces c>=0 because phi ranges over finitely many residues.
Six prescribed updates retain the same root and change the length
from n to n+6. On this closed ordinary witness their cost change is

    6c+phi(x)-phi(F^6(x))=6c>=0.

This contradicts universal strict descent, completing the source
argument with explicit bit and closure dependencies. Memories b<4
embed by ignoring extra residue bits, exactly as in the source.

The lower-bound premise is essential: the exact control omega=-1
has cost -n and six-step change -6, so it strictly descends universally
but is not bounded below over word lengths. It does not contradict
the theorem. This is a hand identity, not an additional numerical run.

The quantifiers and exclusions are unchanged: each b, phase and
bounded-below table has SOME finite witness; neither a common witness
nor a length bound is proved. Restricted near-boundary histories,
arbitrary history-word automata and the whole-tail question remain open.

This expanded audit is lead-derived. The explicit rational-cycle dependency
has its own successful Muse review; a fresh external check of this ENTIRE
all-memory argument remains missing. Its provenance and the exact earlier
review correction are retained in
`results/problem1/20260906_all_memory_expanded_audit.json`. No fresh
full-review acceptance or new numerical result is claimed.
