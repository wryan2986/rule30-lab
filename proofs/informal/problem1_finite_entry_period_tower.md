# Spatial periods of mortal tails

Status: `partial-proof`, independently re-derived and accepted after lead
audit. Review: `problem1_finite_entry_period_tower_review.md`; exact reviewed
and current sources are retained in the round-six audit. The
full-fringe incompatibility remains `inconclusive`; Problem 1 is open.
No numerical experiment, period enumeration, or inverse-tree search is
proposed or run.

## 0. Route and relevance

The exact full-fringe diagonal must be shown incompatible with finite entry.
The inverse-tail recursion already makes a finite-entry candidate rational,
but its generic period bound allows arbitrary periods up to 4^h. Test
whether the actual two-bit inverse recurrence restricts those tail periods
more strongly. A valid restriction narrows the exact alternative in the
diagonal problem; a failing return-map argument would leave the generic
bound in place. This is an algebraic test of the inverse recurrence, not a
reason to enumerate more candidates or sample a longer actual prefix.

Use A(x)=(x>>2) XOR((x>>1) OR x), and its bi-infinite local rule

    (Av)_i=v_(i+2) XOR(v_(i+1) OR v_i).

A nonzero bi-infinite row is called mortal at height e when A^e v=0
and A^(e-1)v!=0. All spatial periods below mean LEAST positive periods
in individual BINARY CELLS, not pair periods or temporal branch periods.

## 1. Preimages of a periodic row (`partial-proof`)

Solving Av=y from left to right gives

    v_(i+2)=y_i XOR(v_(i+1) OR v_i).

On states s_i=v_i+2v_(i+1), the transition s_i -> s_(i+1) is
f_(y_i), with the following hand-derived tables (columns s=0,1,2,3):

    f_0=[0,2,3,3],    f_1=[2,0,1,1].                  (1)

The low output bit is the previous high bit, and the new high bit is
y_i XOR the OR of the two old bits, which verifies all eight entries.

Let y have spatial period p. At any fixed phase, the p-step return map
F is a deterministic map on four states. A bi-infinite preimage supplies
a bi-infinite sequence of states under F at that phase. Every such state
lies on a CYCLE of F: it has arbitrarily long prehistories, and in a
finite deterministic graph the intersection of all iterated images is
exactly the union of cycles. Consequently every bi-infinite preimage is
periodic, with period dividing ell*p for some cycle length ell<=4.
No nonperiodic choice of backward histories remains: a cycle state has
only its cyclic predecessor within the recurrent set.

There is a sharper bound as soon as y is nonconstant. Then p>=2 and
some phase has y_i=0. Start the return map at that phase. The image of
f_0 is {0,2,3}; BOTH f_0 and f_1 identify the states 2 and 3.
Thus the first TWO transitions have image size at most two, and later
transitions cannot increase image size. F has at most two recurrent
states, so ell is 1 or 2. If q is the least period of the preimage,

    q=p or q=2p, for nonconstant periodic y.           (2)

Indeed q divides ell*p, while p divides q because applying a
translation-commuting local map to a q-periodic row makes the output
q-periodic, and p is its least period. This argument permits two fixed
points or a two-cycle; it does not assume a unique preimage.

The constant rows must be treated separately. For y=0, f_0 has exactly
the fixed cycles {0} and {3}, so the only bi-infinite preimages are the
constant zero and constant one rows. For y=1, f_1 has the single
three-cycle 0->2->1->0 (state3 is transient). Its three phase choices
are exactly the three rotations of the period-three word 001.

## 2. Exact period tower for mortal rows (`partial-proof`)

**Theorem.** Every nonzero bi-infinite row mortal at height e is periodic.
If e=1 its least period is 1 and the row is all ones. If e>=2 its least
period is

    p=3*2^k for an integer 0<=k<=e-2.                 (3)

Proof by induction backwards from the first zero row. The preceding row
is all ones by Section 1 and the definition of first extinction. Its
preimages are precisely the period-three rotations just classified.
Every earlier row maps to a nonconstant periodic row and therefore keeps
or doubles its least period by (2). Periodicity itself is also supplied
at each induction step by the finite return-map argument. No spatial
periodicity of the initial row was assumed in this theorem.

The assertion is NECESSARY, not a claim that every listed k occurs at
every height, that the period doubles at each step, or that the height
is bounded by the period. The six-step witness with initial word50 of
period6 fits (3), but the theorem does not depend on its computation.

There is also a finite counting bound, with spatial phases counted as
DISTINCT rows. A fixed nonconstant periodic output has at most TWO
bi-infinite preimages: each is determined by its cyclic state at the
chosen zero phase, and the return map has at most two such states.
Let S_e be the number of rows with first extinction height e. The constant
cases give S_1=1 and S_2=3. Every preimage of a height-(e-1) row has
height exactly e, so S_e<=2S_(e-1) for e>=3. Hence

    S_e<=3*2^(e-2), e>=2,
    #{v on Z:A^h(v)=0}<=3*2^(h-1)-1, h>=1.          (3a)

The second bound includes the zero row and sums the finite height levels;
at h=1 it is exactly two. This counts all bi-infinite rows, not only
rows of a preselected period, since periodicity was just proved.
No kernel, height level, or list of tail patterns is computed.

## 3. Consequences for the original finite-entry alternative (`partial-proof`)

Let x in Z_2 have A^h(x) finite. The previously reviewed inverse-tail
recursion (applied using A^h=pi^h T^h) proves x has an eventually periodic
binary tail. Extend that tail periodically to a bi-infinite row v.
Because A only uses bits at the current or HIGHER positions, x and v
agree after every fixed number of A steps at all sufficiently high
positions. The periodic row A^h(v) therefore has a zero right tail and
must be zero everywhere. If v=0, x is finite. Otherwise apply (3)
with its first extinction height 1<=e<=h.

Therefore EVERY finite-entry input has least eventual spatial period

    1, or 3*2^k for some k>=0.                        (4)

For a given entry time h>=2 a common (possibly nonleast) eventual period
is

    P_h=3*2^(h-2); set P_0=P_1=1.                    (5)

Every period in (4) allowed by e<=h divides P_h. For h<=1 only period1
occurs. The periodic-tail geometric series then gives an exact common
denominator restriction on the reduced rational description of x:

    denominator(x) divides 2^(P_h)-1.                (6)

The finite initial digit prefix changes the numerator and multiplies the
tail by a power of two; it cannot introduce another odd denominator.
Negative integers and nonnegative integers both have period1 and
denominator1, as required. These restrictions do NOT exclude ordinary
finite inputs, which remain the central obstruction.

Combining with the new anchored theorem, Q(x)<=K supplies h=h_J(K)
and hence the single common tail clock P_h in (5), in addition to its
explicit finite image-support bound. No finite list is computed here.

## 4. The temporal clock is an EXISTING import (`partial-proof`)

The dyadic finite-A cycle theorem was already proved in
`problem1_frontier_head_dynamics.md`, Section 2: positive width B has
cycle length dividing 2^(B-1); zero has period1. It is NOT new progress
in this note and no cycle lifting or catalogue is repeated. The initial
reviewed draft re-derived this clock before the older source was located;
that duplicate derivation is superseded here by the explicit import.

Combining that existing theorem with finite entry says Theta(x) has an
eventual temporal period which is a power of two. This necessary condition
does not make the full inverse-scan diagonal a finite-state system: those
scans adjoin an unbounded number of right-side pairs. The NEW classification
in this note concerns spatial periods of mortal tails, Sections 1-3.

## 5. Remaining use and stopping fence (`inconclusive`)

The fixed full-fringe diagonal must still be separated from the finite
entry class, now known to have the spatial clocks (4) and a dyadic
eventual temporal A clock. No incompatibility between those clocks and
the diagonal has been proved. In particular, the spatial period1 case
includes every finite seed and cannot be discarded by denominator
arguments. No period, denominator, height, prefix, or candidate census
is admitted by this classification.
