# A schedule formula for cost near the original history length

Status: `partial-proof` for the exact all-depth identities below;
`finite-exhaustive` for the separately declared checks; `refuted` for
the unconditional five-position extension. Problem 1 remains open.
Base checkpoint: `db5282b1db51deeae2778123487b2ff2886cdba8`.

## Bottleneck, route selection and admission

Universal descent of W* and of its corrected original-position cost
C_s has been refuted at early cuts. The unresolved restriction concerns
elapsed time comparable to ORIGINAL complexity. The preceding cost
pullback and born-suffix formula retain an unbounded original history
and an unbounded schedule. The present task is to eliminate dependence
on the original representation and phase at the critical cuts, without
asserting descent or occurrence exclusion.

Ranked routes (`heuristic`):

1. Remove a uniformly cost-free initial part of the history, then apply
   the exact endpoint suffix identity. High all-depth plausibility,
   high falsifiability and low proof cost; directly addresses the length
   condition instead of increasing a fixed-age graph.
2. Extend the cost-free part by periodic-core stabilization. Testable
   using existing small cores, but a periodic charged state would refute
   any uniform eventual zero claim at that position.
3. Control changes of the resulting schedule functional over genuine
   returns. Direct relevance to the whole-tail obstruction, but no
   monotonicity mechanism is currently established. Higher research cost.

Choose route1, with route2 as a sharpness test before proof adoption.
Admit the existing ordinary-word range k<=9, both phases, and ages
max(1,n-4)..n+3, where n=k-1. Check the endpoint cost formula, including
the cases n<s where padding contributes. Check head costs at all ages
1..n+3. Use only existing periodic cores through width16 and the named
word pupupt to test the five-position extension. Replays at ages1,5,9
test its period-four cost; Muse additionally checks the named extension
family at age13. These are not a new ordinary-frontier census.

For the same words, follow defined forced steps only through n+4 and
check the schedule formula whenever s+1 actual gates exist. This is an
identity check on a specified word set, not a search for new return
occurrences. A mismatching cost or shared-schedule pair would refute
the proposed formula. The finite passage alone proves no all-depth
statement. Local CPU120seconds and1GiB per run, atomic records with
full Git, source/input hashes, timings and hardware/software facts.

## Definitions and the positional indicator

Use T,U,P,A,pi,H and the forced F from the synchronization and cost-
pullback notes. Here pi(x)=x>>2, A(x)=T(x)>>2, and
S_0=t,S_1=u,S_2=S_3=p. The roots are rho_p=3 and rho_u=1.

Let v=g1...gn be an ordinary history AFTER its fixed root, with prefix
endpoints v0=rho and vi=G_gi(v_(i-1)), endpoint x=vn. Its initial
complexity is k=n+1. Let

    I(z)=1 if z=0 or5 modulo64, and0 otherwise.

Claim status: `partial-proof`. At every scanner age s>=1, the cost of
the ith original position is exactly

    I(A^(s-1)(vi)).                                      (1)

Proof. Put z=A^(s-1)(vi). The exact scanner emits S_(z mod4), and
its preceding prefix is pi(z): pi(vi)=A(v_(i-1)) and pi commutes
with A. The edge weight omega(pi(z) mod16,S_(z mod4)) is1 precisely
when pi(z)=0 mod16 and z=0 mod4, or pi(z)=1 mod16 and z=1 mod4.
These are exactly z=0 and5 modulo64. This establishes (1), including
the necessary one-pass difference between the two prefix ages.

## Four positions always have zero cost (`partial-proof`)

For EVERY ordinary history v and EVERY s>=1, its first min(n,4)
positions in H^s(v) have cost0. In particular

    0 <= C_s(v)=W*(H^s(v)) <= max(n-4,0).                 (2)

It suffices to show that O_(a,j) avoids residues0 and5 modulo64 for
j<=5. Indeed A maps each ordinary frontier into itself by the exact
history scanner. Thus every A^(s-1)(vi), i<=4, stays in the same
charge-free frontier O_(a,i+1), at every age.

The roots and the next two ordinary levels are

    p: {3}, {12,13}, {50,51,52,53,55};
    u: {1}, {6,7}, {24,25,26,27}.

At level4 the exact sets are

    p: {200,201,202,203,204,205,207,220,221,222,223};
    u: {100,101,102,103,104,105,107,110,111}.

They all avoid the charged residues. For level5, the complete preimage
table modulo64 is

| Target | T parent | U parent | P parent |
| --- | --- | --- | --- |
| 0 | 0 | 63 | 63 |
| 5 | 59 | 60 | 58 |

Each generator is a triangular permutation modulo64, so checking these
images gives its unique preimages. Neither phase's level4 residues
contain any listed parent. Hence level5 also avoids0 and5. These exact
finite base sets and the all-depth A-invariance prove the claimed
uniform head property. No conjecture about larger periodic cores is used.

## Endpoint diagonal and exact padding correction (`partial-proof`)

For s>=1 define

    D_s(x)=sum_(d=0..s-1) I(A^(s-1-d)(pi^d(x))).          (3)

For every ordinary history with n<=s+4,

    C_s(v)=D_s(x)-max(s-n-1,0).                          (4)

Proof. Write d=n-i for the distance of an original position from the
right end. When d<=s-1, the endpoint projection identity
pi^d(x)=A^d(vi) converts (1) exactly into the dth term of (3).
If n>s, the omitted n-s positions are among the first four and have
zero cost by (2).

If n<s, the sum (3) extends beyond the original positions. At d=n,
pi^n(x)=rho and A fixes rho, so the extra term is I(rho)=0. At every
d>n, pi^d(x)=0, A(0)=0 and I(0)=1. There are exactly max(s-n-1,0)
such terms. Subtracting them gives (4). This also covers n=0 and
the boundary values s=n,n+1 without a special convention.

Each summand of D_s uses at most2s+4 low bits of x: the projection
uses2d bits, the A iterates lose at most2(s-1-d), and I needs6.
Thus D_s is a function of x modulo2^(2s+4), for each s.

## Schedule determination at and before the critical cut

Claim status: `partial-proof`. Suppose the original endpoint has s+1
OBSERVED forced branches sigma, and n<=s+4. Define functions of this
finite observed word using any nonnegative integer representative q of its exact
input cylinder:

    D(sigma)=D_s(q),
    Psi(sigma)=D_s(q)+beta_s(q).

They are well-defined. The common-branch cylinder has precision2s+4;
both D_s and the born-suffix cost beta_s use only those low bits.
The latter is the established born-suffix schedule theorem.

For the actual prescribed history v_s,

    C_s(v)+max(s-n-1,0)=D(sigma),
    W*(v_s)+max(s-n-1,0)=Psi(sigma).                     (5)

Consequently the normalized costs in (5) agree across different
ordinary endpoints, phases and original lengths satisfying the stated
conditions whenever their observed sigma agrees. This is stronger
than agreement among representations of one endpoint, but does not
assert that their full histories agree.

At s=c=k-5, n=k-1=s+4, so for EVERY k>=6 and either phase the
padding term is0. Both costs are determined by the first k-4 actual
branches alone. This is one cut before the earlier full-history
synchronization statement at c=k-4. It is conditional on those
branches existing and proves neither a return occurrence nor its
exclusion. An unobserved final admissibility letter cannot supply
the extra observed branch required by (5).

## Cancellation into a local boundary sum (`partial-proof`)

Write Psi_s(x)=D_s(x)+beta_s(x) directly for a nonnegative integer with s>=1
defined forced steps; a further gate is not needed for this identity.
Let

    J(y)=I(A(y))+I(pi(y)).

Then

    Psi_s(x)=sum_(t=0..s-2) J(pi^(s-t-2)(F^t(x))).       (6)

For s=1 the sum is empty. Proof: a permitted x has I(x)=0, and its
append cost beta_1 is0, so Psi_1=0. For s>=2, removing the oldest
born letter gives

    beta_s(x)-beta_(s-1)(F(x))=I(A^(s-2)(F(x))).

Indeed that aged letter has predecessor pi(A^(s-2)(F(x)))=A^s(x),
using pi F=A^2. The same term appears with the opposite sign when
splitting D_(s-1)(F(x)) and using pi F=A^2:

    D_s(x)=D_(s-1)(F(x))-I(A^(s-2)(F(x)))
             +I(A(pi^(s-2)(x)))+I(pi^(s-1)(x)).

Adding these equations proves the one-step recurrence with boundary
term J(pi^(s-2)(x)); iteration proves (6).

The function J is nonnegative and depends only on its argument
modulo256. The arguments in (6) still come from the full forced
trajectory at varying projection depths. Thus this is an exact local
boundary sum, not a closed256-state trajectory quotient. Neither
monotonicity over time nor descent over a return block follows from it.
Combining (4) and (6) is an explicit cost formula in the age/length
regime of interest, not a proof of the whole-tail obstruction.

## Sharpness on unrestricted ordinary histories

Claim status: `refuted` for extending the unconditional zero head from
four positions to five, even after an arbitrarily long fixed wait.
The from-zero word pupupt has exact prefixes

    3,12,55,200,891,3205,

and H maps its nonroot word upupt to tptpu. The first four costs are0
and the fifth is1. Moreover

    3205 -> A 3558 -> A 3214 -> A 3564 -> A 3205.

Therefore (1) makes the fifth cost1 at EVERY age s=1 mod4. This
all-age conclusion follows from the exact four-cycle, not from testing
many ages. The cycle was already present in the stored width12 core.

The length condition in (4) also has an all-age counterexample to
the unconditional one-position extension. For every s=1 mod4, take
the original nonroot word

    v=upupt followed by s copies of t,   n=s+5.

Its first four costs vanish, its fifth costs1, and its remaining s
positions are exactly the tail represented by D_s. Hence

    C_s(v)-D_s(x)=1.

For s=1 the rooted word is pupuptt, endpoint14235, C_1=1 andD_1=0.
These histories do not come with the long forced continuation required
by (5). In particular the s=1 example stops after its first forced
step. The counterexample does not rule out a stronger theorem restricted
to sufficiently long admissible forced histories.

## Finite verification and remaining obligation

Claim status: `finite-exhaustive`. Independent cell arithmetic checks
all19,682 ordinary words through k9,157,098 admitted C/D cases and
1,564,800 positional cost identities. All pass, including the exact
padding correction. The same finite word set gives665 eligible forced
cases in43 observed-schedule groups. Three groups contain both phases;
six contain multiple original lengths. The normalized costs and the
boundary sum agree in the declared scope. These counts are finite
evidence, not the proof of the universal quantifiers in (1)--(6).

One early independent pair scan aged both endpoints by s, rather
than the required ages s and s-1. Its claimed eventual zero at the
fifth position was discarded after the exact3205 periodic counterexample
exposed the error. The corrected positional formula is used throughout.

Muse independently checks157,098 C/D cases,901,281 positional indicator
comparisons and273,981 first-four cycle pairs with no failures. Its
named extension-family checks at ages1,5,9,13 give C-D=1; four stored
probe chains check the boundary identity through their terminal observed
age, without requiring a further gate. No finite run proves the all-age
sharpness assertion; that follows from the displayed exact cycle.

An independent adversarial mathematical review accepted (1)--(6) and
the sharpness arguments. Its domain clarification to nonnegative
integers is incorporated. Records are
`results/problem1/20260905_critical_cost_primary.json`,
`results/problem1/20260905_critical_cost_independent.json` and
`results/problem1/20260905_critical_cost_verification.json`.
The portable packed verifier reproduces the complete157,098-row C/D
hash, checks all43 stored schedule groups with their51 endpoint
memberships and51 history examples, and replays23 probe ages including
terminal ages. It also verifies all source, original payload, summary
and input hashes. It does not regenerate the complete665-row forced
hash; Muse's separate C/D agreement is aggregate, not a separate row
hash match.
The primary wrapper retains original executed sources and run records;
its runtime measures packaging. The original sharpness run serialized
integer age keys in its family table. Hash reproduction restores those
keys before sorting; sorting the JSON-loaded string keys would change
the order of age13 relative to5 and9.
No descent or occurrence-cut bound is claimed.

Next (`inconclusive`): seek an exact inequality for the boundary sum
over genuine return blocks, with original length and all observed-gate
requirements fixed. Alternatively strengthen the head argument only
on a proved forced-history domain; unrestricted fifth-position erasure
is refuted. Do not enlarge the ordinary-word or short-schedule box
without a new discriminating hypothesis. B_all, near-boundary return
exclusion, signed nonvanishing and Problem 1 remain open.
