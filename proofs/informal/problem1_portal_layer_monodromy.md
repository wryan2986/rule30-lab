# Problem 1: four return matrices for one normalized portal layer

Status: LEMMA WITH PROOF — INDEPENDENTLY CHECKED at this exact transfer
scope. Review: `problem1_portal_label_transport_review.md`.
Problem 1 remains **OPEN**.

## 1. Admission and exact scope

The fixed-period blind-label charge is finite, but it regenerates across
singleton period doublings. A different candidate is to transport the
individual labels through the next observer layer. That requires the
extension map itself, including its recurrent phase selection.

This note gives that map at every depth. It is affine in the added pair
for a **fixed driver and fixed upper history**. It does not assert affine
dependence on the driver. The latter is a separate falsifiable conjecture.
An incorrect matrix or phase-selection formula would invalidate this
extension mechanism; agreement supplies an exact transfer map to use in
the whole-tail route, without another long connector traversal.

All vector and matrix arithmetic below is over GF(2). Products of Boolean
bits are ordinary products of 0 and 1. Temporal words and all histories
are aligned; no rotation quotient is taken.

Fix an integer p>=1 and a binary p-periodic driver w with

    XOR_(s=0..p-1) w_s = 1.

Fix arbitrary p-periodic pair histories (H_s,K_s) and (L_s,M_s).
In a depth-r normalized portal orbit these are the pairs at layers r-1
and r, where r>=0. For r=0 use the fixed boundary pairs

    (H,K)=(1,0), (L,M)=(0,1).

The theorem is valid even without assuming the arbitrary upper histories
satisfy the portal recurrence. Thus it applies, in particular, whenever
they are taken from an actual p-cyclic upper stack. No finite-support,
least-period, dyadic-period, or even-p assumption is required.

The added pair V_s=(X_s,Y_s)^T evolves by the exact quotient law

    F_s = H_s + L_s + (1+L_s)X_s,
    D_s = K_s + M_s + M_s X_s + (1+L_s+M_s)Y_s,
    V_(s+1) = (F_s+w_s D_s, D_s)^T.                 (1)

This is the next-layer specialization of the polynomial recurrence in
`problem1_portal_multilift_phase_quotient.md`.

## 2. The explicit affine transfer

Equation (1) is V_(s+1)=A_s V_s+b_s, where

    A_s = [[1+L_s+w_s M_s, w_s(1+L_s+M_s)],
           [M_s,             1+L_s+M_s]],
    b_s = (H_s+L_s+w_s(K_s+M_s), K_s+M_s)^T.        (2)

Compose one aligned driver period, in chronological order, to obtain

    V_p = A V_0+b,
    A=A_(p-1)...A_0.                               (3)

The vector b is obtained by starting V_0=0 and applying (1) for p steps.
All hypotheses repeat after p steps, so the same affine map is used on
each subsequent period.

Put q_0=0 and q_(s+1)=q_s+w_s. Odd parity gives q_p=1. Define the two
raw parent-half histories over the first p phases by

    u_s=L_s+q_s M_s,
    v_s=L_s+(q_s+1)M_s,
    d_0=product_(s=0..p-1)(1+u_s),
    d_1=product_(s=0..p-1)(1+v_s).                 (4)

The products indicate whether the respective half contains no reset.

**Theorem.** The matrix in (3) is exactly

    A = [[d_1,       d_1],
         [d_0+d_1,   d_1]].                        (5)

Consequently its only four possibilities are

    0, N_0=[[0,0],[1,0]], N_1=[[1,1],[1,1]],
    G=[[1,1],[0,1]].                               (6)

### Proof from the two raw scalar recurrences

At phase s undo the normalization by writing the two child-half bits as

    z_s=X_s+q_s Y_s,
    z'_s=X_s+(q_s+1)Y_s.

The corresponding higher parent bits are

    h_s=H_s+q_s K_s, h'_s=H_s+(q_s+1)K_s.

The original scalar Rule-30 lift laws are independently

    z_(s+1)=h_s+(u_s OR z_s),
    z'_(s+1)=h'_s+(v_s OR z'_s).                   (7)

Substitute OR(a,b)=a+(1+a)b. Renormalizing the two outputs with
q_(s+1)=q_s+w_s gives (1). This checks the direction of the phase
normalization rather than treating q_s as the driver label.

Each scalar recurrence has linear coefficient 1+u_s or 1+v_s. Thus its
one-period linear part in raw half coordinates is diag(d_0,d_1).
Let

    C=[[1,0],[1,1]], S=[[0,1],[1,0]].

At phase zero the raw coordinates are C V_0. At phase p, q_p=1 swaps
the halves before applying C to recover the normalized coordinates.
Therefore

    A = C S diag(d_0,d_1) C.

Multiplication gives (5). Each d_i is either zero or one, yielding (6).
The affine forcing does not enter this linear calculation. This proves
the theorem for arbitrary p-periodic upper histories and hence for all
valid upper stacks. A different initial gauge conjugates the matrices by
G and exchanges the two half selectors; it does not change the four-matrix
classification or the conclusions below.

## 3. Unique extension and exact synchronization alternative

The raw parent track is nonzero when at least one u_s or v_s is one.
This is equivalent to at least one pair (L_s,M_s) being nonzero, and to
d_0 d_1=0. Formula (5) gives

    A^2 = d_0 d_1 I.

Hence for a nonzero raw parent track, A^2=0 and I+A is its own inverse.
There is exactly one p-cyclic added pair, whose initial state is

    V_*=(I+A)b=b+Ab.                               (8)

Indeed the fixed-point equation for (3) is (I+A)V_*=b, and substitution
also verifies A V_*+b=V_* directly. Two iterations of (3) send **every**
initial pair to b+Ab, proving synchronization after at most 2p updates.

The matrix specifies the sharper alternatives. If both raw halves contain
a reset, d_0=d_1=0: A=0 and every seed synchronizes after one p-step
return. If exactly one half contains a reset, A is N_0 or N_1: after one
return there are exactly two different possible outputs, and all seeds
synchronize after the second return. This is a statement at the aligned
period boundaries; an earlier update may already synchronize particular
seeds. No uniform-in-depth transient bound for the entire stack follows.

For a valid upper stack, the fixed pair together with its p successive
updates is the unique cyclic extension. At odd driver parity the raw
halves exchange after p phases, so this is exactly one full 2p-periodic
scalar child track. This recovers the unique recurrent one-bit child
through the normalized coordinates, with the closed formula (8).

## 4. Zero parent track and the obstruction to the next extension

If the entire raw parent track is zero, L_s=M_s=0 at every phase. Then
d_0=d_1=1 and A=G. The fixed-point equation is

    (I+G)V=b, i.e. (Y,0)^T=(b_X,b_Y)^T.

Thus:

* b_Y=1: no p-cyclic normalized extension exists;
* b_Y=0: exactly two initial pairs exist, Y=b_X and X arbitrary.

For completeness the obstruction can be read from the higher track.
In (7) the scalar responses now integrate h_s and h'_s. Their constant
terms over p steps are their respective XOR sums. The final half swap
gives

    b_X=XOR_s [H_s+(q_s+1)K_s],
    b_Y=XOR_s K_s.                                 (9)

For a valid stack, XOR_s K_s is precisely the parity of the higher raw
track at the (H,K) layer over its full 2p phases. Therefore the first
alternative is the
usual odd-parity zero-track portal obstruction; the second gives the two
complementary scalar integrations. These are the correct boundary cases,
not limits of the nonzero-parent formula (8).

Odd driver parity is essential. For p=1, w_0=0 and the r=0 boundary
pairs, the one-step matrix is [[1,0],[1,0]], whose square is itself and
is nonzero. The half swap used in (5) is absent. This finite control
does not challenge the odd-driver theorem.

## 5. What this does and does not transport

The exact extension map is: compose (2), determine the two half-reset
selectors (4), and use (8) for a nonzero parent. At a zero parent use (9)
and the two-case fixed-point test instead. This applies at arbitrary
observer depth and retains the aligned driver history.

It does not replace that history by a few scalar charges. In particular
A_s contains the products w_s M_s and w_s(1+L_s+M_s). Even when an upper
orbit is held fixed and several driver labels are free at blind phases,
composing these matrices can multiply the free labels with the previously
transported pair. The fact that (1) is affine in V is not a proof that
V_* or its entire orbit is affine in w.

The next test is therefore exact: on one fixed aligned blind-label cube,
does the map to the next observer orbit have vanishing second finite
differences? A four-word parallelogram with a nonzero phasewise output
XOR refutes that claim. Independently, the first-zero-return parity can
be tested as an affine function on the same cube. Neither statement is
proved by the four-matrix theorem.

The prize obstruction still requires an original-support resource with
bounded reuse across physical restarts and period doublings. A local
recurrent phase formula supplies neither that resource nor a positive
residence-ledger contribution.

## 6. Verification

Finite verifier:

    python3 experiments/problem1_nonperiodicity/check_portal_layer_monodromy.py

Its declared finite controls compare the polynomial update, explicit
matrix composition and two separate raw scalar half updates. The proof
above establishes the all-period statement; the finite record is not an
extrapolation argument. The review disposition and exact check counts are
recorded in the companion review. The verifier checks 25,104 matrix
compositions and 100,416 seed returns by two independent coordinate
methods, with 987,808 raw updates. It covers all upper-pair histories for
p=1,2,3 and every parent history with four constant higher histories for
p=4. Its zero-track controls include 146 cases with no cyclic extension
and 178 with two. The named even-driver control verifies that the odd
hypothesis is needed.
