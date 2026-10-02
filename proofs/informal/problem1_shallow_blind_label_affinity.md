# Problem 1: exact linear transport of shallow hidden labels

Status: LEMMA WITH PROOF — INDEPENDENTLY CHECKED for extension depths
r=1,2,3 and for Section 7's conditional all-depth lemma. Independent
review and finite-evidence dispositions are recorded in
`problem1_portal_label_transport_review.md`.
The all-depth extension conjecture and endpoint-parity conjecture remain
unproved. Problem 1 remains **OPEN**.

## 1. Two falsifiable transport candidates

Fix even p>=2, an odd-parity aligned binary driver w of presentation
length p, and the normalized portal stack with boundaries

    (X_-1,Y_-1)=(1,0), (X_0,Y_0)=(0,1).

Use the exact transitions T_w from `problem1_cyclic_blind_cone_bound.md`.
Let R=(R_s)_(s mod p) be a realizable depth-r cyclic stack orbit. A phase
is blind when T_0(R_s)=T_1(R_s). The nonempty odd-label fiber C_R fixes
the nonblind labels and allows the blind labels subject to one parity
equation. For k blind phases its dimension is max(k-1,0); when k=0
the fiber is a singleton if the forced labels are odd. The driver labels
need not have the least period of the unlabeled state orbit.

An extension is taken only while the last raw parent track is nonzero,
so every member of C_R has a unique next cyclic layer. Earlier zero
tracks end the unique connector. This domain condition is common to the
whole fiber, because the raw track is zero exactly when its normalized
pair is (0,0) at every phase. It is not a selection of an arbitrary
nonaffine subset of C_R.

**H_ext (CONJECTURE at general r).** For every such R, the map E_r from
C_R to its full aligned depth-(r+1) orbit is affine over GF(2).
Equivalently, every four drivers in C_R with XOR zero have extension
orbits with phasewise XOR zero. No rotation canonicalization is used.

**H_endpoint (CONJECTURE).** On each nonempty C_R for which the depth-r
orbit exists, the parity f_p(w) of the portal's first returned zero target
is an affine function of the driver labels.

For H_endpoint, integrate ww at length 2p with initial bit zero. Oddness
gives an antiperiodic, nonzero integration x. The connector starts at
(x,0), so the existing boundary-return theorem proves a finite first
return for EVERY odd w. No finite-core ancestry assumption is needed
for well-definedness. Endpoint parity is independent of temporal phase.
The normalized observer's depth r is counted after the universal two
lifts; it is not the imported certificate's original connector depth.

Either conjecture, if true, would provide an algebraic label transport
law in place of a fitted scalar charge. A counterexample would require
nonlinear transport even with the complete upper observer held fixed.
Neither conjecture by itself gives bounded reuse of the original support.

## 2. The shallow theorem

**Theorem.** At r=1,2,3, H_ext holds for every even p>=2 and every odd
driver on the stated domain. In fact all odd drivers have unique layers
through depth four. Within a fixed depth-r fiber:

* at r=1 the next orbit is constant;
* at r=2 each free label can change only the new X coordinate at the
  immediately following phase;
* at r=3 each free label can change only the new X coordinate at the
  following two phases, and its effect is erased before any next free label.

The newest Y history is constant on each of these fibers. So is the
depth-(r+1) blind phase set. Writing u_j=max(k_j-1,0), the affine
extension has rank exactly u_r-u_(r+1).

This theorem concerns three observer extensions at ALL periods, not all
observer depths and not eventual center nonperiodicity.

## 3. The five-state upper orbit and the first extension

The first layer has the three recurrent states

    a=(0,0), b=(0,1), c=(1,1),

with a,b --0--> c, a,b --1--> b, and c --0/1--> a.
These follow directly from

    Y_1(s+1)=1+X_1(s),
    X_1(s+1)=(1+w_s)(1+X_1(s)).

The pair (1,0) cannot occur on a cycle, because a predecessor with X_1=0
has output Y_1=1, and one with X_1=1 has output X_1=0. A cycle cannot
consist only of a. Thus the first raw track is nonzero.

Use the existing depth-two states, ordered as (X_1,Y_1,X_2,Y_2):

    A=(0,0,1,0), B=(0,1,0,0), C=(0,1,0,1),
    D=(1,1,0,0), E=(1,1,1,1).

Their transition table, verified directly from the quotient rule, is

    A --0--> E, A --1--> C,
    B,C --0--> D, B,C --1--> B,
    D,E --0/1--> A.                                (1)

A depth-two orbit can be decoded from the current and preceding
first-layer states, without reading any hidden label:

    current a                         -> A,
    current b, previous a / b         -> C / B,
    current c, previous a / b         -> E / D.     (2)

The first-layer table lists all possible predecessor types used in (2).
Checking (1) shows that (2) constructs a cyclic depth-two realization for
every realizing driver. The nonzero-parent uniqueness theorem in
`problem1_portal_layer_monodromy.md` makes it the unique realization.
Hence E_1 is constant on C_R. First-layer blind phases are exactly c;
depth-two blind phases are exactly D,E. Thus B_2=B_1 as well.

The second raw track cannot be identically zero for an odd driver of
even length. Such an orbit would use only B,D. State D exits to A,
so the entire cycle would be B with w_s=1 at every phase. Its weight
p is even, contradicting the driver parity. Thus the next layer exists
uniquely at every phase.

## 4. A blind depth-two label is isolated by a reset

Fix an aligned depth-two orbit and its odd label fiber. Only phases in
D,E carry free labels. At state A the layer-three formula is simply

    V_3(s+1)=(1,0),                               (3)

independent of its previous pair and of w_s. Every free phase is
followed by A, by (1). If any free phase exists, the cycle therefore
contains a reset (3). The incoming V_3 at a free phase s is fixed by
the latest preceding A reset and the intervening forced labels: any
intervening free phase would itself be followed by a later A. This
argument uses cyclic preceding times and also covers the wraparound.

At phase s the incoming pair is consequently independent of ALL free
labels. Equation (1) of the monodromy note changes its output only by

    (w_s D_3(s),0).

The next phase is A and erases this effect by (3). Therefore different
hidden labels have disjoint output positions s+1, and E_2 is affine.
The new Y history is constant. The coefficient D_3(s) at each old blind
phase is also constant, so the new blind phase set is fixed on the fiber.
When there are no free labels, C_R is a singleton and these assertions
hold directly.

For the next step, note that E can only be entered from A with label
zero. Its incoming third pair is (1,0) by (3), so at E

    D_3=X_3+Y_3=1.                                (4)

Thus E is NEVER blind at depth three. Every depth-three blind phase has
upper state D and third pair (x,1), with x in {0,1}, because at D
D_3=1+Y_3.

The third raw track is nonzero. If it vanished at every phase, its next
pair equations would require (X_1,Y_1)=(X_2,Y_2) throughout the upper
orbit. The only states in (1) with that equality are C,E, and neither
has a successor in {C,E}. This contradicts cyclicity. Hence depth four
also has a unique extension.

## 5. A blind depth-three label is erased before the next one

Fix a depth-three orbit and its odd label fiber. At a free phase s the
upper depth-two state is D and V_3(s)=(x,1), by Section 4. The following
two upper configurations are fixed:

    at s+1: upper state A, V_3=(1+x,0),
    at s+2: upper state E or C, V_3=(1,0).          (5)

The first line uses the blind output D_3=0 and F_3=1+x. The second uses
the reset (3). Which state E or C occurs is decided by the forced label
at s+1; that phase has first-layer state a and is nonblind.

At s+2, equation (4) excludes blindness if the upper state is E; if it
is C, its first layer is b and already nonblind. In either case s+2
is nonblind at depth three. Phase s+1 is likewise nonblind. Thus the
next free phase cannot occur before s+3.

For the layer-four linear update at s+2, its parent pair (L,M) is
(1,0). Both rows of its matrix in the monodromy note are zero.
It therefore erases every incoming V_4; its forced label and fixed
higher pair determine its output completely. This reset precedes the
next possible free phase. The same cyclic latest-reset argument as in
Section 4 makes the incoming V_4 at EVERY free phase independent of
all free labels.

Its label influence at s+1 is (w_s D_4(s),0), with constant coefficient
D_4(s). At s+1 the parent pair is (1+x,0), so an X-only difference
is multiplied by x and produces no Y difference. Thus it can affect
s+2 only by (x w_s D_4(s),0), and the reset at s+2 erases it at s+3.
These supports are disjoint for different free phases, including cyclic
wraparound. This proves E_3 affine, with invariant newest Y history.
Again a singleton odd fiber needs no free-phase argument.

At each free phase its incoming pair and coefficient D_4(s) are fixed,
so its survival as a deeper blind phase is independent of the free labels.
That proves invariance of the depth-four blind set on the fiber.

## 6. Exact rank

For any realized full extension orbit, its label fiber is exactly the odd
affine cube prescribed by its blind phases. Within the old fiber the
deeper blind set is now fixed. Hence every nonempty fiber of the proved
affine extension has dimension u_(r+1). Its domain has dimension u_r,
and rank-nullity gives rank u_r-u_(r+1), including the singleton cases.

## 7. An all-depth sufficient reduction

The finite tests also check a stronger, simpler candidate:

**H_Y (CONJECTURE at general r).** For every aligned upper orbit and
odd-label fiber in Section 1's nonzero-parent domain, the newest
half-difference history Y_(r+1)(s) is independent of the driver in C_R.

**Conditional lemma, at EVERY r>=1.** H_Y for one fiber implies H_ext
for that fiber, a fixed deeper blind set, and rank u_r-u_(r+1).

Proof. Write the common newest history as y_s. Its pair equations give

    M_s X_s = y_(s+1)+K_s+M_s+(1+L_s+M_s)y_s,
    X_(s+1) = H_s+L_s+(1+L_s)X_s+w_s y_(s+1).     (6)

The first equation contains no varying driver. If M_a=1 at some phase,
it fixes X_a independently of w. The second equation, propagated for
one whole cyclic period from a, then makes every X_s an affine function
of w. If M_s=0 throughout, nonzero parent means L_a=1 somewhere. At
that phase the second equation instead supplies the affine initial value
X_(a+1)=H_a+1+w_a y_(a+1); propagate around the cycle from there.
These two cases exhaust the nonzero-parent domain. Existence of each
cyclic extension supplies consistency at wraparound, rather than assuming
an arbitrary recurrent seed. This proves affine dependence of the full
extension orbit. A phase survives as blind exactly when it was already
blind and y_(s+1)=0, independent of w. Section 6 then gives the rank.

Thus the proposed all-depth linear transport can be attacked using the
simpler two-driver test of H_Y: equal complete upper orbits, but different
new Y histories. A failure would refute H_Y, while H_ext could still hold
with nonconstant affine Y. The implication is not asserted in reverse.

## 8. Remaining obstruction and finite evidence

At r>=4 neither label isolation nor affineness has been proved here.
The four-matrix fixed-driver theorem remains valid there, but multiplying
driver-dependent matrices is not automatically linear in the free labels.
This is the smallest unresolved extension depth for this particular
transport strategy. H_Y is proved at r=1,2,3 above and is a sufficient
all-depth target by Section 7. The separate endpoint-parity conjecture is not a
corollary of any shallow extension theorem.

The companion finite checker tests exactly declared driver cubes and
extension depths; survival beyond the proof's r<=3 scope remains
FINITE EVIDENCE ONLY. A complete Prize Problem argument still needs
transport across period changes and bounded reuse against the same
original finite support.

Reproduce the finite checks:

    python3 experiments/problem1_nonperiodicity/check_blind_fiber_endpoint_affinity.py

No first-witness center campaign, additional p32 connector traversal, or
infinite FULL assumption is used in this note.
