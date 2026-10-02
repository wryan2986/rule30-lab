# Problem 1: finite exact miter for all-period layer affineness

Status: LEMMA WITH PROOF — INDEPENDENTLY CHECKED for the finite reduction.
No computational all-period exclusion is claimed in this note.
Problem 1 remains **OPEN**.

## 1. Fixed-depth graph, with no period cutoff

Fix r>=1. Use the normalized transition T_a on depth r+1 with boundaries
(1,0),(0,1). A product state is (U,V,Z), where U is a depth-r state
with 2r bits and V,Z are two added pairs with two bits each. There are
exactly 2^(2r+4) such states. This is an observer-depth bound, not a
finite bound on the full Rule-30 spatial state or eventual temporal period.

For each label pair (a,b), apply T_a to (U,V) and T_b to (U,Z). Keep
the edge only when their depth-r output states agree. At an upper blind
state all four label pairs are allowed; otherwise only a=b is allowed.
Call an edge bad when U is blind, a=b, and the two added output Y bits
are different. These are the two outgoing gates d_s at the same label.

Attach a parity sheet g=(g_A,g_B,g_time) in GF(2)^3. Each edge adds
(a,b,1). The lifted graph has exactly

    N_r=2^(2r+7)

vertices. Put h=(1,1,0). Sheet translation is a graph automorphism.

A parent participation flag j is present at a vertex when the normalized
pair at upper layer j is not (0,0). An upper raw track is nonzero over
a whole cycle exactly when its flag appears at some time. We require
every j=1,...,r on an admissible cycle, so all earlier unique lifts and
the new extension are in the stated nonzero-parent domain.

The flag identification is exact in every gauge: the two raw half bits
at a phase are X+qY and X+(q+1)Y. They are both zero if and only if
X=Y=0. This pointwise invertible coordinate change holds for every q,
even though the driver determines q.

## 2. Exact counterexample criterion

**Theorem.** H_ext fails at depth r for some even period and complete
odd-label upper fiber with nonzero parents if and only if the lifted
graph has a strongly connected component C such that:

1. C contains a bad edge from (u,0) to (v,g_edge);
2. (u,h) is also in C;
3. for every parent layer j=1,...,r, some vertex in C carries flag j.

### From a fiber counterexample to the graph

By the gate equivalence theorem, failure of H_ext means that some upper
blind phase s has two drivers w,z in its complete odd fiber with the
same label w_s=z_s but unequal outgoing new gates. Their paired cyclic
histories are a cycle in the product graph. Align it at phase s.
Its length is even and both label words are odd, so it lifts from (u,0)
to (u,h). Translate this same path by h to obtain a return from (u,h)
to (u,0). Together they form a closed lifted walk, containing the bad
edge and every nonzero-parent participation flag. All its vertices and
edges lie in one strongly connected component. This proves necessity.

### From the graph to a complete upper fiber

Start with the bad edge in condition 1. Within C, take paths that visit
one witness for each flag in condition 3 and then reach (u,h), using
condition 2. This gives a positive-length product cycle whose length is
even and whose two driver words are odd. Its upper trajectories agree;
each raw parent track is nonzero because of the required flag visits.

The fixed boundary parent is nonzero. Applying odd-driver cyclic
uniqueness layer by layer proves that both histories are exactly the
canonical normalized stacks constructed from their driver words. No
spurious alternative cyclic seeds survive this argument. The two words
therefore belong to the same COMPLETE upper odd-label fiber. At the
bad phase their labels agree and their outgoing gates differ, violating
H_gate and hence H_ext. This proves sufficiency.

At r=4 it is enough to require the last flag for a recovered even-period
odd-driver cycle: the shallow theorem already forces parents 1,2,3
nonzero on every such cycle. Rechecking every flag is still permitted.

## 3. Direct four-word certificate from a bad gate

The two words w,z above must be different: uniqueness rules out different
new histories for the same odd word. Their difference is supported on
upper blind phases and has positive even weight. Thus at least two blind
phases carry different labels, in addition to the bad phase s where they
agree. There are at least three blind phases. Choose any other blind
phase t and put delta=e_s+e_t. The four words

    w, z, w+delta, z+delta

are distinct, odd, and realize the same complete upper orbit. If their
full extension XOR were zero, then the incoming added states, the
outgoing added states, and the affine F_s term would each have XOR zero.
The four gate values would also have XOR zero. The first two gates
already differ, so the last two would differ too. Their labels at s are
a,a,a+1,a+1, giving

    XOR [w_s d_s]=a+(a+1)=1.

This contradicts X_(s+1)=F_s+w_s d_s and the asserted zero full-output
XOR. Thus this particular four-word square is an explicit non-affinity
certificate. No exhaustive enumeration of its whole fiber is required.

## 4. A simpler independently checkable absence certificate

For absence, an independent verifier need not establish that a supplied
partition consists of exact strongly connected components. It suffices
to verify an integer rank rho on ALL N_r lifted vertices satisfying

    rho(target)>=rho(source) on EVERY retained edge.       (1)

For each rank group, verify that conditions 1–3 of Section 2 cannot all
hold, replacing component membership by equal rank. Every actual
counterexample gives the closed lifted walk constructed in Section 2.
Monotonicity (1) forces all ranks on that walk equal, so it would satisfy
all three forbidden rank-group conditions. Their checked absence rules
it out. Merging components can make the certificate harder to satisfy;
it cannot conceal a counterexample.

The exact linked check asks for a bad edge from (u,0) whose endpoints and
(u,h) all have the same rank, together with all parent flags in that
group. A simpler, stronger exclusion check may OR three group flags:
an internal bad edge from any sheet-zero start, any product state's
sheet-zero/sheet-h pair in the group, and parent participation. The
two starts need not coincide in this stronger test. If no group has
all flags, the exact linked obstruction is also absent. Presence of
all OR flags alone is not a constructed counterexample.

A topological rank of the exact component condensation supplies such
rho whenever Section 2 has no eligible component. For r=4 the exact
graph has 32768 vertices; a little-endian uint16 rank per vertex occupies
65536 bytes before base64 encoding. The checker must reconstruct edges
from an independent Rule-30 transition and verify the entire array,
domain, monotonicity, parent flags and forbidden group conditions.
Hashes alone are not an absence proof.

This yields a possible all-period theorem at one fixed observer depth
only after that complete certificate is verified. It does not establish
H_gate at every depth, cross-return transport, bounded reuse of the
original support, or center nonperiodicity.

## 5. Independent logical review

A separately pinned free Space Bunny critic accepted the sheet-translation
necessity, SCC path construction, all-parent participation domain,
four-word contradiction and monotone-rank absence argument. Its comments
requested explicit parity justification for three blind phases and the
raw/normalized zero equivalence; both are supplied above. The mechanical
link between a bad edge's start and its sheet-h copy is now explicit,
including the conservative OR-flag variant. The parent rechecked each
step. This review establishes the reduction's scope, not a particular
computed rank certificate or the full Prize Problem. Its incidental claim
that arbitrary constants on components are automatically monotone was not
accepted: the constants must respect condensation-edge order, or the
monotonicity must be checked directly as required above.

## 6. Projecting a stronger rank certificate to the product graph

**Additional lemma with proof.** Suppose a rank rho on the lifted graph
is nondecreasing on every edge and strictly increasing on every bad edge,
on ALL eight sheets. Define a rank on the unlifted product graph by

    rho_base(P)=max_(g in GF(2)^3) rho(P,g).

It inherits both inequalities. For an edge P->Q with sheet increment h,
choose g attaining the maximum at P. Then

    rho_base(Q)>=rho(Q,g+h)>=rho(P,g)=rho_base(P),

with strict middle inequality if the edge is bad. This proves the lemma.
Conversely any such product-graph rank lifts by ignoring the sheet.

Thus this STRONGER sufficient exclusion can be tested on only
2^(2r+4) product states. If it fails, a bad product cycle may still have
inadmissible parities or zero parents; the full sheet/flag miter remains
necessary for the exact odd-fiber criterion. At r=4 the independently
verified certificate is strict on all bad edges, so the projection lemma
applies. At r=5 a prospective first screen would have 16384 product states,
rather than 131072 lifted vertices. No depth-five run is admitted or
claimed by this observation alone.
