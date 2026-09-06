# The full fringe as an inverse-scan diagonal condition

Status: `partial-proof`, fresh independent derivation accepted in scope
after lead audit. Review: `problem1_full_fringe_temporal_diagonal_review.md`;
exact reviewed/current sources are retained in the round-six audit.
The diagonal's incompatibility with bounded activity is `inconclusive`.
Problem 1 remains open. No numerical experiment is admitted or run.

## 0. The question this addresses

The reviewed one-step bridge says Phi(c)=shift^2(b), c_0=3. This loses
one gate bit if the fringe-supplied branch is omitted, and by itself does
not specify the complete actual future fringe. Derive that missing boundary
condition on ONE ORIGINAL code b, without replacing the future by freely
chosen permitted gates. If the proposed construction lost the initial right
half, it would not be a full-fringe growth route. The exact condition below
retains it at every depth; the unresolved task is then a stated compatibility
problem for this condition and bounded anchored activity.

Use the established maps Theta, Phi, g and h from the sparse temporal-code
and gate-bridge notes. A code symbol a=a0+2a1 is a low-to-high bit pair.
For any a in {0,1,2,3}, define an inverse scan I_a by

    (I_a b)_0=a,
    (I_a b)_(t+1)=h((I_a b)_t,b_t),
    h((a0,a1),(r,s))=(r XOR(a0 OR a1),s XOR(a1 OR r)). (1)

The letter a in I_a is an INITIAL SYMBOL, not a u/t branch. The symbol
0 in I_0 records an actual zero right-hand pair at time zero.

## 1. The inverse scan means adjoining an initial spatial pair (`partial-proof`)

The local inversion of g gives Phi I_a b=b. Conversely a code c with
c_0=a and Phi c=b must satisfy the successive equations in (1), and hence
equals I_a b. Combining this with the reviewed conjugacy yields

    Theta(4x+a)=I_a Theta(x),                          (2)

because pi(4x+a)=x and the new low pair is a. This also proves uniqueness
of the complete code, not merely one low residue. For each fixed scan state,
h is a permutation of its input symbol: recover r from the low output bit,
then recover s. The already hand-derived rows, input columns 0,1,2,3, are

    a=0: [0,3,2,1],  a=1: [1,2,3,0],
    a=2: [3,2,1,0],  a=3: [3,2,1,0].                (3)

The boundary is load-bearing: I_0 and I_3 are different scans. No claim
that either one commutes with temporal shift is made.

## 2. Encoding an attached right half exactly (`partial-proof`)

Let r_i(t), i in Z, obey physical Rule 30

    r_i(t+1)=r_(i-1)(t) XOR(r_i(t) OR r_(i+1)(t)).

At time zero encode the center and left half by

    x=sum_(i>=0)r_(-i)(0)2^i,  b=Theta(x).

Encode the initial right half, in PAIRS facing toward the center, by

    a_j=r_(2j)(0)+2r_(2j-1)(0), j>=1.                (4)

Thus these symbols reverse each center-outward right pair. The actual pure
alternating reconstruction has a_j=0 for every j. A general finite initial
right fringe has a_j=0 eventually. No restriction on x is assumed here.

Put W_0=x and W_m=4W_(m-1)+a_m. Then W_m enumerates the original row from
physical position 2m toward the left; its low 2m bits are the reversal of
the first 2m right-fringe cells. Define

    B_m=I_(a_m) ... I_(a_1) b=Theta(W_m), B_0=b,
    C_m=shift^(2m) B_m,
    D_m=(B_m)_(2m)=(C_m)_0.                          (5)

Let X_m=sum_(i>=0)r_(-i)(2m)2^i be the ACTUAL center-and-left row at time
2m, without assuming center periodicity. Then

    X_m=A^(2m)(W_m),     C_m=Theta(X_m).               (6)

Coordinate proof. At time 2m, the center lies 4m bit positions inward
from the right-edge frame whose initial origin was physical position 2m.
Deleting those 4m bits gives pi^(2m) T^(2m)(W_m)=A^(2m)(W_m).
Ignoring initial cells to the right of 2m is valid for EVERY cell in X_m:
the backward cone of r_(-i)(2m) ends at 2m-i<=2m. All cones used for
Theta(X_m)_t end at that same initial cut or farther left. Thus even an
infinite attached right half causes no omitted influence in (6).

Equation (6) alternatively follows bit by bit from the local A rule and
its physical characteristic coordinates. It is a statement about the
original full spacetime, not about a separately reinitialized right fringe.

## 3. Exact alternating-center criterion (`partial-proof`)

For the fixed attached initial right half (a_j),

    r_0(t)=1,0,1,0,... for ALL t>=0
       iff D_m=3 for EVERY m>=0.                    (7)

Necessity: r_0(2m)=1 and r_0(2m+1)=0 give r_-1(2m)=1 by the local rule
at the center. Hence the even-time center-and-left-neighbor pair is 3.
Sufficiency: D_m=3 supplies both those even-row ones. The next center
is 1 XOR(1 OR r_1(2m))=0, regardless of the right neighbor. These
statements cover every even and odd time. No temporal periodicity of
the odd-row neighboring bit or of the u/t schedule is inferred.

For the initial all-zero right half this is the single-code condition

    (I_0^m b)_(2m)=3, EVERY m>=0.                    (8)

The scans in (8) always start at time zero. Replacing shift^(2m) I_0^m
by the m-th iterate of shift^2 I_0 would reset the right fringe after
each two-step block and is not justified.

For a fixed (a_j), these diagonal conditions determine b uniquely.
More generally, the map b -> (D_m)_m is a triangular homeomorphism of
the four-symbol one-sided shift. For m>=1, (I_(a_m)...I_(a_1)b)_k,
k>=m, depends only on b_0,...,b_(k-m) and is a permutation of its LAST
input when earlier inputs are fixed. Prove this by induction on m:
the next scan's final h reads its input at k-1; the scan state at k-1
depends only on earlier inputs. The latest input therefore occurs in
exactly this final permutation, composed with the induction permutation.
At k=2m the latest input is b_m. At m=0, D_0=b_0. Thus any desired
D prefix solves b_0,b_1,... successively and uniquely; the compatible
finite bijections give the infinite homeomorphism. The original right
symbols are fixed parameters throughout, not extra existential choices.

## 4. Recovering the gate bridge without discarding the fringe (`partial-proof`)

Phi commutes with shift and cancels the outermost inverse scan, so (5)
gives the exact identity, WITHOUT any alternating premise,

    Phi C_(m+1)=shift^2 C_m.                          (9)

Under (7) both low symbols are 3, and uniqueness in Section 1 gives

    C_(m+1)=I_3(shift^2 C_m).                         (10)

This recovers the reviewed permitted-step scan. Equation (10) alone
omits the full initial-right-half condition (5),(7); it cannot replace it.

To check the actual gate at any row, let a=r_2(2m)+2r_1(2m) be its
right-hand pair facing toward the center. The next actual code is
shift^2 I_a C_m. If (C_m)_0=3, the first intermediate scan symbol is
h(a,3)=1 for a=0, and h(a,3)=0 for a!=0. Requiring its next symbol
to be 3 forces, by (3),

    (C_m)_1=2 if a=0 (the actual u branch),
    (C_m)_1=1 if a!=0 (the actual t branch).           (11)

These are precisely the permitted spatial residues 7 and 11 modulo16.
Thus the discarded one-bit gate choice is recovered from the actual
right pair; its complete evolution is retained by the fixed-boundary
construction (5), not supplied by an arbitrary permitted branch word.

Hand prefix check for a_j=0 (a local derivation, not a prefix campaign):
D_0=3 gives b_0=3. Then (I_0b)_1=1, and D_1=3 forces b_1=2.
Write c=I_0b, d=I_0c. With those symbols c_0,c_1,c_2=0,1,3 and
c_3=3 XOR b_2; d_0,...,d_3=0,0,3,0. Thus D_2=d_4=h(0,c_3)=3
forces c_3=1 and b_2=2. No additional actual symbols are evaluated.

Scope control: the imported constant-u forced survivor x=5/3 has
b_0=3, b_1=2, and b_2=A^2(x) mod4=(-1/3) mod4=1, because its
forced fixed-point equation gives A^2 x=pi x=-1/3. It follows that
D_2=2, not 3, under the ZERO initial right fringe. Infinite gate
permission and even the correct first actual branch therefore do not
satisfy (8). This is a coordinate check of a known non-actual survivor,
not a new refutation of the already rejected free-schedule route.

## 5. The concrete remaining compatibility question (`inconclusive`)

Use Q(x)=sup_n J_n(x) as in the new anchored finite-entry note. For the
ONE pure alternating survivor with zero initial right half, the unresolved
target can now be stated entirely on its original temporal code:

    (I_0^m b)_(2m)=3 for all m
       implies sup_n sum_(t=0..n-1)1[(Phi^n b)_t!=0]=infinity. (12)

There is no free gate sequence in the premise. The right boundary for I_0
and the spatial deletion Phi act on the SAME original b. The anchored
finite-entry theorem makes the negation an explicit finite-entry alternative:
for some K, x=Theta^(-1)b has A^h_J(K)(x) finite with the proved support
bound. No incompatibility of that alternative with the diagonal is proved.
Rationality of b, by itself, is also insufficient as a proof step here.

For eventual period two, rebase at an actual phase-one row beyond the
preperiod and retain its resulting right symbols a_j. Under a finite-support
hypothesis those symbols are eventually zero, and (7) applies at the new
origin. They need not all be zero. A uniform exclusion for EVERY finite
right fringe would be a sufficient stronger statement; this note does not
identify every such fringe with a reachable onset of the original right-zero
problem. Pure traces, arbitrary eventual traces, and arbitrary finite
right-fringe boundary problems remain distinct quantifiers.

Next work should test a concrete incompatibility between (8) (or its actual
rebased version) and finite entry. Merely evaluating more D, b, J, or gate
prefixes would repeat finite reconstruction and is not admitted here.
