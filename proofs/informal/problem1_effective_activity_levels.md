# Effective finite activity levels and rational activity profiles

Status: `partial-proof`, lead-derived and checked with fresh independent
review accepted in scope. Full derivations, including the exact error
constant and oracle-encoding distinction, are retained in
`problem1_effective_activity_levels_review.md` and
`results/problem1/20260906_effective_activity_levels_review.json`.
The archive preserves the exact reviewed pre-status-update source.
This note makes the bounded-activity alternative effective; it does not
prove unbounded activity on an actual survivor or solve Problem 1.

## Route after the return counterexample

The finite-level theorem gives a proper activity record, but its proposed
return nonincrease is refuted even on a stored genuine prescribed block.
Do not repair that claim by a new return census or a fitted compensation.
Two materially different remaining routes are (`heuristic`):

1. Make the finite levels EFFECTIVELY finite, retaining exact rational
   candidates and identifying the remaining infinite equality test.
   This has a concrete all-depth goal with a compactness proof to audit.
2. Prove fixed-survivor age growth from the full fringe-coupled history.
   This remains the main unresolved growth obligation; no new invariant
   that establishes it has been found here.

Route1 is addressed only by proof. No E_K list, graph, spatial period,
schedule, mortality tree, or other numerical census is computed or
admitted. An effective finite level would remove the nonconstructive
size bound as a separate obstacle; it would not decide whether a listed
candidate equals the actual infinite survivor.

Use T, A, pi, V_s, R and E_K from the finite-level note, with N
including zero. A rational 2-adic means a rational number with odd
denominator, equivalently an eventually periodic binary digit stream.
The equivalence follows by summing the repeating geometric series;
conversely exact long division has finitely many remainder states.

## 1. Finite entry supplies an effective rational input (`partial-proof`)

For h>=0 and y in N there is a unique x=T^(-h)(y) in Z_2, by
unit triangularity of T. At position i the h-step rule has the form

    bit_i(T^h x)=x_i XOR H_h(x_(i-2h),...,x_(i-1)),       (1)

where negative-index input bits are zero. The Boolean function H_h
is computable by h local updates. Coefficient one on x_i follows
inductively: every other input to the final update depends on bits
strictly below i. Thus (1) computes the digits x_i successively.

Let B=bitlen(y). For i>=B the output digit is zero, so the successive
2h-bit windows of x follow one autonomous deterministic map on
2^(2h) states. A state repeats after at most 2^(2h) transitions before
the next repeated state is identified. This gives a computable eventual
spatial onset a and period p of x. For example the nonsharp bounds
a<=B+2^(2h) and p<=2^(2h) suffice; for h=0 use the zero tail of y
with period1 directly. No finite-prefix truncation is mistaken for a
certificate: the repeating finite recursion is proved first.

The resulting rational description is exact. Applying T a fixed
number t of times preserves the spatial period p beyond a+2t, since
the complete input cone at those positions lies in the periodic tail.

## 2. Exact finite-entry decomposition (`partial-proof`)

If y=T^h(x) is finite, set z=pi^h(y), also finite. For every s>=h,

    V_s(x)=sum_(t=0..h-1) bit_(2s)(T^t(x))
                 + V_(s-h)(z).                         (2)

For h=0 the first sum is empty. Split the defining temporal sum at
h. Its late part is sum_(u=0..s-h-1) bit_(2s)(T^u(y)). By the
A-diagonal formula it equals

    sum_(u=0..s-h-1) bit_0(A^u(pi^(s-u)(y)))
      = V_(s-h)(pi^h(y)).

No commutation of pi with T is used. The case s=h has empty late
sum V_0=0, so there is no negative age.

For any finite z, put n=max(ceil(bitlen(z)/2)-1,0). Once r>=n,

    V_r(z)=sum_(d=1..n) bit_0(A^(r-d)(pi^d(z))).        (3)

Terms with d>n vanish because pi^(n+1)z=0; if n=0 the sum is empty
and V_r(z)=0 at every r. At r=n initialize the n components
A^(n-d)(pi^d(z)); subsequent r increments apply A componentwise.
Each component has bounded finite bit length, since

    A(v)=(v>>2) XOR ((v>>1) OR v)

cannot increase bit length. This finite vector therefore has a
computable transient and a computable closed cycle. Directly evaluate
r<n; the cycle decides all remaining ages, exactly as in the named
return certificate but now as an all-input termination argument.

In (2), each of the h early terms is eventually spatially periodic
as a function of s, with period dividing p/gcd(p,2). The second term
is eventually periodic by (3). Their finite sum is eventually periodic,
with a computable onset and period (take a common multiple and maximum
of the separately computed data). Its direct finite prefix and one
complete cycle compute R(x) exactly. In particular membership

    T^(-h)(y) in E_K

is decidable for any supplied h,y,K, without assuming an unverified
uniform spatial support bound or a guessed time period.

Hand scope controls for the NEW decomposition (no numerical rerun):
T(-1)=1 gives h=1,z=0 and V_s(-1)=1 for s>=1. The already
established T(-1/7)=-1,T^2(-1/7)=1 give h=2,z=0 and, for s>=2,
V_s(-1/7)=1+indicator_(3 divides s), since its initial bits repeat
100 from low to high. These infinite inputs satisfy the decomposition;
finite entry is not replaced by initial finite support.

## 3. A computable finite list E_K (`partial-proof`)

Fix K, and compute h=h_V(K) by exact rational harmonic sums. Put
L=K+h. For each y in N, let x_y=T^(-h)(y), B_y=bitlen(y), and
form the computable binary cylinder

    C_y = x_y + 2^(B_y+4L+4) Z_2.                      (4)

The corrected isolation lemma applies even if x_y is not in E_K:

    C_y intersect E_K subset {x_y}.                     (5)

Indeed if x' in that intersection differed from x_y, T^h(x') would
differ from finite y first at a>=B_y+4L+4. Its record is at most
K+h=L by the time-translation bound, contradicting isolation. No
prior membership decision for x_y is needed for (5).

Every x in E_K equals x_y for y=T^h(x) in N, by uniform finite
entry. Consequently the cylinders C_y cover E_K. Compactness supplies
a finite subcover, hence some b such that

    E_K subset U_b = union_(0<=y<2^b) C_y.              (6)

For N>=0 write

    P_N = {x:V_s(x)<=K for 0<=s<=N}.

This is a clopen finite-cylinder set: every V_s uses only the input
bits through 2s. The P_N decrease to E_K. For the fixed b in (6),
some finite N satisfies P_N subset U_b. Otherwise the nonempty
compact sets P_N minus U_b would be nested and would have a point
in E_K minus U_b, contradicting (6).

Here is a terminating algorithm, not a performed experiment. At stages
m=1,2,... set b=N=m, compute U_m and P_m, and test P_m subset U_m
by inspecting their common finite binary refinement. This is a finite
Boolean calculation at each stage; precision

    max(2m+1, m+4L+4)

suffices. Monotonicity of U_m and P_m guarantees eventual success
once m exceeds the b,N just proved to exist. At that stage (5) gives

    E_K subset {T^(-h)(y):0<=y<2^m}.

Use Section2 to decide each candidate's actual R<=K, and retain
exactly the successful rational descriptions. This outputs E_K in
finite time. Its runtime and output size have no useful bound here.
No such algorithm is executed or admitted by this note.

Thus E_K and the uniform support bound

    B(K)=max_(x in E_K) bitlen(T^h_V(K)(x))

are computable functions of K. The set is nonempty because it contains
0,1,2,3. This strengthens existence of a maximum, without claiming a
closed formula or a practical method for obtaining it.

## 4. Rational inputs have a bounded-or-linear dichotomy (`partial-proof`)

There is also a useful scope test for proposed activity growth laws.
Let x have spatially periodic tail of period p from position a. Extend
that tail to a bi-infinite p-periodic row v. T on p-periodic rows is
a deterministic map on the finite set of p-bit rows; its trajectory
therefore reaches a temporal cycle after some q steps, of period ell.

Put D=max(1,ceil(a/2)). For t<=s-D, the input cone of position2s
starts at2s-2t>=2D>=a. Thus T^t(x) and T^t(v) agree there. Of
the s times defining V_s, at most D-1 late times may disagree, once
s>=D. If m_i is the number of ones in column i modulo p over one
temporal cycle, finite transient and cycle counting give

    |V_s(x) - (m_(2s mod p)/ell) s| <= q+ell+D-1,
                                      for every s>=D.  (7)

The error bound is uniform in s, with constants determined by this
particular rational tail; no common denominator or period is imposed.

If the temporal cycle is nonzero, every m_i is positive. If one
column were zero throughout the cycle, its temporal differences would
be zero, and the local rule would force BOTH lower adjacent columns
zero throughout the same cycle. Iterating around the spatial period
would make the whole cycle zero, a contradiction. Hence in the
nonzero case every coefficient in (7) is at least 1/ell, and

    liminf_(s->infinity) V_s(x)/s >= 1/ell > 0.          (8)

If the cycle is zero, the periodic tail vanishes at time q. Finite
propagation then makes T^q(x) finite, so R(x)<infinity and Section2
gives an effectively eventually periodic activity sequence. Conversely
bounded R excludes the nonzero case by (8).

Thus on rational inputs bounded activity and positive lower linear
growth are the only alternatives. The coefficients may depend on the
spatial residue 2s modulo p; a single limiting slope is not asserted.
The dichotomy is not claimed for arbitrary irrational 2-adic inputs.
It also computes R on any GIVEN rational input: a nonzero tail cycle
certifies infinity; a zero cycle supplies finite entry and Section2
computes the finite value.

## 5. Finite lists are not finite-query membership (`partial-proof`)

The list algorithm does not decide R(x)<=K from finitely many digits
of an ARBITRARY 2-adic input x. Indeed no total finite-query decision
procedure on arbitrary digit oracles can do so. On input0 in E_K it
would halt after inspecting finitely many digit positions. Some other
input outside the finite E_K agrees with zero at all those positions;
the identical query transcript would force an incorrect positive answer.
This is an oracle-input limitation, not a claim of undecidability for
rational numbers given by numerator and denominator.

There is not even a universal finite sampling horizon for detecting
R>K on unrestricted inputs. For any N,K choose m>max(N,K) and put
x=2^(2m). All bits below2m remain zero under T, while the first one
at2m remains one. Therefore V_s(x)=0 for 0<=s<m, but V_m(x)=m>K.
This exact family delays every positive activity witness past N; it
uses no forced gate and refutes no actual-survivor-specific bound.
No experiment or first-witness search is needed for the argument.

## 6. The remaining equality obligation (`inconclusive`)

Even a computed E_K would not settle whether the actual survivor lies
in it. Candidate membership in E_K is decidable by Section2; equality
of a listed rational with the full fringe-coupled survivor is a DIFFERENT
infinite statement. Checking longer survivor prefixes only semidecides
inequality when a mismatch occurs. If a candidate equals the survivor,
waiting for a mismatch never stops. No algorithm deciding that equality
is supplied here, and no first-witness box is reopened.

Accordingly effective finiteness does not authorize an E_K census as
the next research step. The main obligation remains growth of V_s on
one fixed actual survivor. Equation(8) can diagnose a proof route that
also establishes irrationality or a rational tail, but by itself it
provides neither premise for the actual survivor.
