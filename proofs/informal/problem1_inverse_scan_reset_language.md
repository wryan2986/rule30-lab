# Reset words and periodic tails of the full inverse scans

Status: `partial-proof`, independently re-derived and accepted after lead
audit. Review: `problem1_inverse_scan_reset_language_review.md`. The
full-fringe/finite-entry incompatibility remains `inconclusive`; Problem 1
is open. No numerical experiment or prefix extension is used here.

## 0. The admitted question

The round-six bottleneck puts a full-fringe diagonal and finite entry on
the same temporal code. Finite entry supplies an eventual temporal period,
but a generic bound on the periods of successive inverse scans says little
about their diagonal values. Test the more precise mechanism: exactly which
input words erase a scan's starting state, and when can an inverse scan
double an eventual period? Synchronization would preserve the old period;
a nonsynchronizing word would identify the exceptional mechanism that must
be retained. Both alternatives change the proposed periodic-tail argument.
This is an all-word algebraic derivation, not a finite word census.

Use Theta, Phi, and I_a from `problem1_full_fringe_temporal_diagonal.md`.
For an input symbol i, let H_i(a)=h(a,i). Reading a finite word
w=w_0...w_(l-1) means the composition

    H_w = H_(w_(l-1)) ... H_(w_0).

Call w a RESET word if H_w is constant on all four starting states. This
is synchronization of a SINGLE scan, not a reset of the physical right
fringe. The full scans always retain their actual initial boundary.

The hand-derived driven maps, in state order 0,1,2,3, are

    H_0=[0,1,3,3], H_1=[3,2,2,2],
    H_2=[2,3,1,1], H_3=[1,0,0,0].                 (1)

These are the columns of the already reviewed h table. Muse's separate
single-scan memo supplies a first bound; the language below gives the
exact alternatives rather than an additional census of that table.

## 1. Exact reset language (`partial-proof`)

**Theorem.** A finite word w fails to reset exactly when

    w belongs to {0,2}* UNION {0,3}* UNION {0,3}*{1,2}. (2)

The empty word is included and is the identity map. The two trailing
letters in the last term are alternatives, not a two-symbol suffix.

One direct proof tracks the IMAGE SET of the four starting states. The
following table lists every nonsingleton image that can occur; a dash
means a singleton. Its entries follow by applying (1) element by element.
Once a singleton occurs it stays a singleton under every later input.

| image before input | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| {0,1,2,3} (empty word) | {0,1,3} | {2,3} | {1,2,3} | {0,1} |
| {0,1,3} | {0,1,3} | {2,3} | {1,2,3} | {0,1} |
| {1,2,3} | {1,3} | - | {1,3} | - |
| {1,3} | {1,3} | - | {1,3} | - |
| {0,1} | {0,1} | {2,3} | {2,3} | {0,1} |
| {2,3} | - | - | - | - |

The paths avoiding a singleton are precisely (2): initial zeros can
continue into only-0/2 inputs, only-0/3 inputs, or an only-0/3 prefix
followed by a FINAL 1 or 2. This proves both necessity and sufficiency
for arbitrary word length by induction on the table paths.

A second check of sufficiency uses invariant pairs. Both H_0,H_2 act
as permutations on {1,3}; both H_0,H_3 act as permutations on {0,1}.
A last H_1 or H_2 sends {0,1} bijectively onto {2,3}. Hence none of
the words on the right of (2) can be constant. In particular every
H_j H_1 is constant, and a 2 followed later by a 3 with only zeros
between already resets. A 3 followed by zeros and then a 2 resets
after ANY one further letter. Order and the last-letter exception matter.

## 2. Exact eventual-period alternatives (`partial-proof`)

Suppose b has LEAST eventual temporal period p, periodic from time T.
Let w be one period of its tail. For ANY a, c=I_a b has least eventual
period q as follows. Counts refer to one least period, not an arbitrary
multiple of it.

| periodic tail of b | eventual states of c | q |
| --- | --- | --- |
| all zero | a constant in {0,1,3} | 1 |
| contained in {0,2}, with a 2 | {1,3} | p if the number of 2s is even; 2p if odd |
| contained in {0,3}, with a 3 | {0,1} | p if the number of 3s is even; 2p if odd |
| contains 1, or contains both 2 and 3 | unique synchronized periodic response | p |

Proof for the last row: w is either a reset word already, or one of the
last-letter exceptions in (2). In the latter case appending the first
letter of the next period resets. Therefore any two driven scan states
coalesce after at most p+1 letters of the periodic tail. Apply this to
states c_T and c_(T+p), driven by identical tails, to obtain period p
from time T+p+1. The response is independent of the incoming state.

For a {0,2} tail with a 2, the first 2 sends every state into {1,2,3};
the next letter sends every state into {1,3}. On that pair a 0 is the
identity and a 2 is a swap. Thus the period return is the identity or
a swap according to the stated parity, after at most p+1 tail letters.
For a {0,3} tail with a 3, the first 3 sends every state into {0,1};
on that pair 0 is the identity and 3 is a swap. Entry takes at most p
tail letters. The all-zero case follows from H_0^2=H_0.

In every case Phi c=b makes p divide q: a period q of c is also a
period of its local image b. This supplies LEAST periods, not just
available periods. If the return on the invariant pair is a swap,
period p is impossible, so q=2p; otherwise q=p. All cases have an
available onset no later than T+p+1. Constant input 1 from state 0
gives 0,3,2,2,..., so the additive p+1 bound is attained at p=1.

Every doubling produces a recurrent output which contains symbol 1.
Indeed the invariant pair is {1,3} or {0,1}, and the odd number of
swaps visits both elements. Consequently the NEXT inverse scan is
synchronizing and cannot double the period. For any sequence of initial
symbols a_j, if B_0=b and B_(m+1)=I_(a_(m+1)) B_m, then

    p_m = p * 2^(d_m),   d_m <= ceil(m/2).           (3)

Here d_m counts doubling steps and no two such steps are adjacent.
This is stronger than merely p_m dividing p*2^m. It is independent of
the initial right symbols and says nothing about diagonal values before
their periodic tails.

## 3. An actual full-fringe consequence (`partial-proof`)

Let (a_j) be ONE fixed initial right half, with a_j=0 eventually, and
let x encode the center and left half. Use the original definitions

    W_m = 4 W_(m-1)+a_m, W_0=x,
    B_m=Theta(W_m), C_m=shift^(2m) B_m=Theta(X_m),
    X_m = actual center-and-left row at time 2m.

Assume FULL: (C_m)_0=3 for every m. Assume also finite entry:
A^h x is finite for some h. Then the following necessary condition holds:

    C_m is NOT purely temporally periodic for infinitely many m. (4)

Equivalently, X_m is not an A-periodic point for infinitely many m.
If tau_A(y) denotes its first entry time onto an A-cycle (finite for
every finite-entry y), this says

    tau_A(W_m) > 2m for infinitely many m.           (5)

For clarity, the equivalences use the FULL temporal code, not a finite
mod-4 shadow: shift^p Theta(X)=Theta(X) implies Theta(A^p X)=Theta(X),
and hence A^p X=X by injectivity. Also every W_m has finite entry at
the SAME h: pi^m W_m=x and pi commutes with A, so
pi^m A^h W_m=A^h x is finite, and restoring m low pairs keeps A^h W_m
finite. A finite A row has a finite orbit state space and hence enters
a cycle. Thus every tau_A(W_m) here is a finite integer.

Proof by contradiction. If every C_m is purely periodic for m>=M,
let p_m be its least period. The exact full-fringe bridge gives

    C_(m+1) = I_3 shift^2 C_m.                       (6)

Since (C_m)_0=3, its period contains 3. If that period uses only
{0,3}, Section 2 makes every inverse scan's eventual symbols lie in
{0,1}. But C_(m+1) is purely periodic and starts with 3: impossible.
The period of C_m must therefore contain 1, or both 2 and 3. It is
the synchronizing case, and p_(m+1)=p_m. All p_m for m>=M equal one p.

Equation (6) is deterministic on the finite set of at most 4^p purely
p-periodic codes. The actual C_m orbit stays in that set, so it is
eventually periodic in m. Since Theta is injective, X_m would therefore
be eventually periodic as well.

Finite entry plus the finite initial right fringe makes the full
physical row finite after a fixed time: for a zero right half this is
A^h x finite iff T^h x finite; changing finitely many initial right
cells changes only finitely many cells at time h. At a sufficiently
late even time X_m is a positive finite integer. The bridge also gives

    pi X_(m+1)=A^2 X_m,  X_(m+1) mod4=3,
    X_(m+1)=4 A^2 X_m+3.                            (7)

A preserves the bit length of a positive finite integer. Thus the
positive finite X_m have bit lengths increasing by EXACTLY two per
block, contradicting eventual repetition. This proof needs no external
width-two theorem. The identities and finite-length fact are imported
from the reviewed gate-bridge and anchored finite-entry notes.

For a zero right half, (5) reads tau_A(4^m x)>2m infinitely often.
For a finite fringe ending at J, W_m=4^(m-J)W_J for m>=J. This
retains the actual fringe; it does not identify all fringes with a
reachable onset of an original right-zero eventually alternating trace.

Scope strengthening: the same reasoning applies to ANY infinite
permitted F orbit with finite entry, using its imported identity
pi^m F^m x=A^(2m)x to obtain eventual finite states. Thus (4) is not
an actual-fringe-only discriminator. Its application to the same W_m
in FULL is exact, but exclusion of the remaining transient alternative
still needs a further argument.

## 4. Remaining hypothesis and stopping fence (`inconclusive`)

The result supplies a concrete way for a bounded-activity full survivor
to evade a periodic-tail argument: its A-cycle entry times must lie
strictly beyond the actual diagonal at infinitely many depths. This is
a proved conditional requirement, not an observed delay or a claim that
such a survivor exists. It differs from comparing 2m with an UPPER bound
on tau_A(W_m), which cannot establish a delay.

A sufficient next hypothesis would be eventual entry by 2m for these
same W_m under FULL. A universal version for every finite-entry x and
every finite fringe would be stronger. Neither is proved. Even a
bound 2m+C with C>0 would not imply (4) fails. No increased prefix,
transient, width, cycle, or activity census is authorized by this note.
