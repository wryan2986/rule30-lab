# Sparse temporal codes can escape every activity level

Status: `partial-proof`, independently re-derived and accepted in scope.
The necessity of the transport note's asymptotic density criterion
is `refuted` by the exact family below, conditional only on the stated
proved dependencies. It is still a sufficient criterion. No actual
period-two survivor is constructed or excluded; Problem1 remains open.

The full review is `problem1_activity_sparse_temporal_codes_review.md`.
Exact reviewed/current sources, dependencies and lead disposition are
retained in `results/problem1/20260906_activity_sparse_temporal_codes_review.json`.
No numerical run was used for this proof.

## Decision and scope

Before investing in a density lower bound from the full fringe, test whether
unbounded R actually requires any positive characteristic density d_n^*.
This is a falsifiable all-depth claim, not a numerical density fit. A
counterexample means the density hypothesis is stronger than the desired
growth conclusion and that finite-window transport should remain available.
Failure of the proposed counterexample would reopen its coding or density
argument. No numerical code, survivor, period, or activity census is run.

Use A, pi, V, R and P_n,d_n^* from the staircase and transport notes.
An alphabet symbol in {0,1,2,3} denotes a low-to-high binary pair with
value b_0+2b_1. These symbols are NOT the t/u branch letters.

## 1. A temporal coding of A (`partial-proof`)

Define

    Theta(x)_t=A^t(x) mod4, t>=0.

Then Theta is a computable homeomorphism from Z_2 to
{0,1,2,3}^N, and

    Theta(Ax)=shift(Theta(x)).                        (1)

Proof. Induction on t in the cell rule gives

    bit_i(A^t x)=bit_(i+2t)(x)
                   XOR f_(i,t)(x_i,...,x_(i+2t-1)),   (2)

for a computable Boolean function f; at t=0 the lower part is empty.
At the induction step the highest input appears with coefficient one
only through the upper-cell term. The two OR inputs depend on strictly
lower positions. This is the previously used triangular property of A,
now applied to a complete temporal code.

Given symbols b_0,...,b_(M-1), solve input bits in order: b_t's
low bit determines bit2t once the earlier bits are fixed; its high bit
then determines bit2t+1. Thus the first M symbols biject with the first
2M input bits. The finite bijections are compatible as M increases,
which supplies one unique infinite x for every code b. Both directions
are continuous and computable on finite prefixes. Equation (1) follows
from the definition. This is not Delta, the one-bit growing-diagonal
map, and it asserts no finite-state presentation for Delta or its inverse.

## 2. Spatial deletion becomes a local map on temporal codes (`partial-proof`)

For a=(alpha_0,alpha_1), b=(beta_0,beta_1), define the symbol

    g(a,b)=(r,s),
    r=beta_0 XOR (alpha_0 OR alpha_1),
    s=beta_1 XOR (alpha_1 OR r).

For an infinite code b let

    (Phi b)_t=g(b_t,b_(t+1)).

Then

    Theta(pi x)=Phi(Theta(x)),
    Theta(pi^n x)=Phi^n(Theta(x)).                    (3)

To derive the first identity, write the four low bits of A^t x as
alpha_0,alpha_1,r,s. The next A step has low bits
beta_0=r XOR (alpha_1 OR alpha_0) and
beta_1=s XOR (r OR alpha_1), giving g by inversion. Since pi
commutes with A, the output pair is exactly Theta(pi x)_t.
Iteration proves the second identity.

In particular g(0,0)=0, and the symbol (Phi^n b)_t depends only on
b_t,...,b_(t+n). Therefore

    P_n(t)=1[(Phi^n b)_t !=0], b=Theta(x),             (4)
    P_n(t)<=sum_(j=0..n)1[b_(t+j)!=0].                (5)

The latter is an inequality in nonnegative integers. No nonzero lower
bound or equality of densities follows from it.

For completeness, rationality is preserved by this temporal coding:

    x rational 2-adic iff Theta(x) eventually periodic. (6)

If the spatial tail of x has onset a and period p, A preserves the
finite class of rows whose tail is p-periodic from that same onset:
its output at i uses only i,i+1,i+2. At most 2^(a+p) rows occur,
so the A orbit and the temporal code are eventually periodic.
Conversely if b has temporal onset h and period ell, every Phi^n b
has the same available onset h and period ell, since Phi only looks
forward. Phi acts on the finite set of at most 4^(h+ell) such words.
Thus (Phi^n b)_0 is eventually periodic in n. By (3) these are
precisely the spatial digit pairs of x, proving its rationality.
These are finite-state arguments on GIVEN periodic descriptions;
no periodic descriptions are searched or inferred from a prefix.

## 3. An exact sparse-code counterexample (`partial-proof` / `refuted`)

Take b_t=1 when t=2^k for an integer k>=0, and b_t=0 otherwise,
and set x=Theta^(-1)(b). More generally, prescribe ANY finite code
prefix and use this same sparse rule after that prefix. The resulting
x is computable and irrational by (6): the code has infinitely many
nonzero symbols and arbitrarily long intervening zero runs, so cannot
be eventually periodic. A nonzero eventually periodic word has bounded
zero runs; the eventually-zero case has only finitely many nonzeros.

For every fixed n>=1,

    d_n^*(x)=0.                                      (7)

Indeed an interval of W integer times contains at most
1+floor(log_2 W) powers of two. If it contains m>=1 of them, their
span is at least 2^(m-1)-1, while it is at most W-1. An arbitrary
fixed prefix adds at most its length M to this count, uniformly over
the interval's start. Sum (5) over W consecutive times: each of its
n+1 summands is a translated W-time interval, so

    C_n(a,W) <= (n+1)(M+1+floor(log_2 W))

uniformly in a. Divide by W, take sup_a and then limsup_W at FIXED
n. This proves (7), in exactly the limit order of the transport note.

Nevertheless

    R(x)=infinity.                                   (8)

Suppose otherwise and choose an integer K>=R(x). The reviewed
activity-level theorem says E_K is finite and A(E_K) subset E_K.
Thus the A orbit of x is eventually periodic, and (1) makes b
eventually periodic, a contradiction. This proof uses the existing
finite-level theorem, not absence of a finite numerical cycle.
Equivalently, finite-entry inputs are rational by the reviewed
inverse-tail recursion, whereas this x is irrational.

Hence the assertion

    R(x)=infinity implies some d_n^*(x)>0

is refuted on general Z_2 inputs. In particular neither (7) nor (8)
of the transport note is necessary for activity growth. The values
d_n^*=0 are proved exactly, not estimated from sampled times.

## 4. Finite compatibility and the remaining use of transport

Status: `partial-proof` for the following density-in-cylinders statement.
Every finite binary cylinder contains one of the counterexamples above.
Enlarge its specified bit prefix to an even length 2M if necessary,
convert that prefix to its unique M-symbol Theta prefix, and append the
sparse code. The inverse in Section1 preserves the required input bits.
This also permits matching any given finite observed survivor branch
prefix, by its established finite input-cylinder precision. It does
NOT assert that the extension obeys the actual future fringe or even
that it is an infinite forced survivor. No such equality is tested.

The useful distinction is between a limit at fixed n and a simultaneous
growth of n and the time window. The exact finite inequality

    sum_(s=a+2..a+W+n)V_s
       >= sum_r ceil(C_n(a,W)/(2r+1))

is unaffected by this counterexample. Taking the fixed-n density limit
can lose intermittent events that matter when n and W grow together.
Whether finite-window transport can yield an unbounded lower bound
for the ACTUAL coupled survivor remains `inconclusive`. Do not replace
that question by a wider ray-density experiment or a fixed-prefix
constraint: neither is justified by the counterexample.
