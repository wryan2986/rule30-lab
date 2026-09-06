# Anchored pair activity is an exact finite-entry criterion

Status: `partial-proof`, fresh independent derivation accepted in scope
after lead audit. Review: `problem1_anchored_activity_finite_entry_review.md`.
The review's initial spatial-limit objection used a different order of
extension and shifting; the reviewer withdrew it after re-deriving the
original all-integer-offset statement. Exact versions are archived in the
round-six audit. No weakening of the theorem was needed.
All actual full-fringe growth claims remain `inconclusive`; Problem 1 is
open. This note proves a converse explicitly left unasserted in the round-five
joint-window note. No numerical experiment is proposed, admitted, or run.

## 0. Decision and relevance to the current bottleneck

The target sup_n J_n(x)=infinity is already sufficient for the desired
fixed-survivor record growth. Before trying to derive it from the actual
fringe, test whether bounded J has an exact dynamical meaning, or whether it
can hide an infinite-activity input as fixed-ray density can. A proof of
uniform tail extinction would make the anchored target equivalent to the
original finite-entry obstruction. A counterexample would require a separate
mechanism beyond finite-entry exclusion to force J growth. The argument below
settles this question by local identities and compactness, with no census.
It does not supply that still-missing full-fringe mechanism.

Use the established one-sided maps

    T(x)=x XOR ((x<<1) OR (x<<2)), pi(x)=x>>2,
    A(x)=pi T(x)=(x>>2) XOR ((x>>1) OR x),
    P_n(x,t)=bit_(2n)(A^t x) OR bit_(2n+1)(A^t x),
    J_n(x)=sum_(t=0..n-1)P_n(x,t), n>=1,
    Q(x)=sup_(n>=1)J_n(x).

Q is a new name for the record of the EXISTING anchored observable; it is
not a branch letter or the forward generator Q used in older forced notes.
Write H_m=sum_(r=1..m)1/r, H_0=0, and

    h_J(K)=min{h>=0:H_(h+1)>K}, K a nonnegative integer.

This uses ordinary harmonic sums, not the earlier odd harmonic constants.
In particular h_J(0)=0, h_J(1)=1, h_J(2)=3.

## 1. Last pair activity under A (`partial-proof`)

Here ONLY, use bi-infinite spatial rows u_i(t), i in Z, t>=0, obeying

    u_i(t+1)=u_(i+2)(t) XOR (u_(i+1)(t) OR u_i(t)).     (1)

Let b_j(t)=(u_(2j)(t),u_(2j+1)(t)), a symbol in {0,1,2,3}.
The already derived temporal deletion identity holds directly in this
bi-infinite setting:

    b_(j+1)(t)=g(b_j(t),b_j(t+1)),                    (2)
    g((a0,a1),(c0,c1))=(r,s),
    r=c0 XOR(a0 OR a1), s=c1 XOR(a1 OR r).

Indeed solve (1) at positions 2j and 2j+1 successively for the two
higher bits. The local algebra uses no one-sided boundary or inverse-limit
argument. The essential terminal identities are

    g(0,0)=0,      g(a,0)=3 for EVERY a!=0.             (3)

For a!=0 the first output bit r is 1, so the second is also 1.
Thus for any finite-support temporal word b, the word Phi(b)_t=g(b_t,b_(t+1))
has exactly the SAME last nonzero time, and is zero iff b is zero.

Suppose every spatial pair j has finitely many nonzero times. Equations
(2)-(3) imply all pairs have the same last time M, including the possible
value -infinity for the all-zero spacetime. In the nonzero case (3), applied
to pair j-1, makes b_j(M)=3 for every j. Row M is identically one and
every later row is zero. No assertion that pair counts are monotone is used.

If every pair has at most K nonzero times, then

    H_(M+1)<=K.                                      (4)

For each r=0,...,M, a zero interval of r+1 consecutive pairs at time M-r
would give a zero pair at its left endpoint at time M: the r-step input
cone of that output pair is exactly the 2r+2 cells in that interval.
This contradicts b_j(M)=3. Hence every such interval contains a nonzero
pair at time M-r. In any N consecutive pairs there are at least
floor(N/(r+1)) active pairs at that time. Sum these M+1 finite counts,
bound the total by KN, divide by N, and let N tend to infinity. This
proves (4), without interchanging infinite sums. Consequently every such
spacetime is zero by time h_J(K). For K=0 it is zero initially.

## 2. Bounded anchored activity gives uniform finite entry (`partial-proof`)

**Theorem.** For EVERY x in Z_2 and K>=0,

    Q(x)<=K  implies  A^h(x) in N and T^h(x) in N,
    where h=h_J(K), N includes zero.                  (5)

Take any limit of initial rows obtained by shifting x left by even bit
amounts 2n_l with n_l tending to infinity. Extend x arbitrarily, for
example by zero, at negative indices BEFORE shifting. Precisely, let
bar{x}_i=x_i for i>=0 and bar{x}_i=0 for i<0, and translate by
v^(l)_i=bar{x}_(i+2n_l) for EVERY i in Z. The artificial boundary
therefore tends to minus infinity; it is not reset at each shifted origin.
Diagonal compactness gives a convergent subsequence on every finite window.
Local A evolution commutes with these limits; its fixed finite input cones
are eventually entirely within the original nonnegative indices.

Fix any integer j and any finite temporal horizon L. Pair j in the limiting
spacetime is the limit of pair n_l+j of A^t(x). Eventually n_l+j>=max(1,L),
so all times 0,...,L-1 occur within J_(n_l+j)(x), whose count is <=K.
Thus that limiting pair has at most K nonzero times in every finite horizon,
and hence in total. This is true for every j. Section 1 makes EVERY such
spatial limit vanish at the SAME time h=h_J(K).

If A^h(x) had infinitely many nonzero pairs, shift the input by even amounts
at those pairs and take a convergent subsequence. The output pair at index 0
would be nonzero in the limit, contradicting uniform extinction. Therefore
A^h(x) is a nonnegative finite integer. The imported exact identity

    A^h(x)=pi^h T^h(x)

then makes T^h(x) finite as well: restoring 2h low digits preserves
finiteness. This is NOT a commutation assertion for pi and T.

## 3. Exact finite-input record and an explicit finite level (`partial-proof`)

For a finite z, put N(z)=max(ceil(bitlen(z)/2)-1,0). Then

    Q(z)=N(z).                                        (6)

A preserves the bit length of every positive finite row: its top bit is
the unshifted contribution in (x>>1) OR x, while x>>2 cannot cancel it.
Consequently, if N(z)>=1, its highest pair stays nonzero at EVERY A time,
and J_(N(z))(z)=N(z). All higher pairs vanish, and every lower J_n<=n<=N(z).
For bitlen(z)<=2 every n>=1 lies above the support, so Q(z)=0.

For every x,n,h>=0 in the applicable ranges, temporal-window comparison gives

    J_n(A^h x)<=J_n(x)+h,
    Q(A^h x)<=Q(x)+h.                                (7)

If n<h the whole shifted count is <=n<=h; otherwise only h times are new.
For Q(x)<=K let h=h_J(K), z=A^h(x). Equations (5)-(7) give

    bitlen(z)<=2(K+h+1),
    bitlen(T^h x)<=2K+4h+2.                           (8)

Since T^h is an injective unit-triangular map, the level {x:Q(x)<=K} is
contained in the explicit FINITE set

    {T^(-h)(y):0<=y<2^(2K+4h+2)}.                    (9)

No candidate list is computed. The previously proved inverse-tail recursion
shows that every candidate is a rational 2-adic. Finiteness here follows
from the explicit support bound and injection, with no extra isolation step.

Conversely, if z=A^h(x) is finite, then for n>N(z) all P_n(x,t) vanish at
t>=h. For n<=N(z), J_n<=n<=N(z). Therefore

    Q(x)<=max(h,N(z)).                               (10)

Together with (5) this proves the exact equivalences

    Q(x)<infinity iff some A^h(x) is finite
      iff some T^h(x) is finite iff R(x)<infinity.     (11)

Only the last equivalence imports the reviewed single-column finite-entry
theorem. The new direction Q bounded => finite entry was proved directly.
The earlier joint-window note asserted only Q unbounded => R unbounded;
its decision not to assert a converse was a scope boundary, not a no-go.

## 4. A false invariance that must not be imported (`refuted`)

Finite Q levels are NOT generally A-invariant, in contrast with the R levels.
For n>=2 take the exact negative integer

    x=-3*4^(n+1).

Hand identities: T(-3)=3, and T(4^k v)=4^k T(v), so

    A(x)=3*4^n.

The initial pairs below n+1 are zero. Every pair above n is nonzero at
time zero and zero at every later A time. Pair n is zero initially and
nonzero forever afterwards (the top pair of the finite image). Thus

    Q(x)=max(1,n-1)=n-1,   Q(Ax)=n.                   (12)

For pairs j<n only the trivial J_j<=j<=n-1 is needed. The upper bound in
(7) is therefore sharp already at h=1. This family uses no forced gate
or actual fringe and refutes no actual-survivor-only assertion.

## 5. What the full fringe would still have to contradict (`inconclusive`)

The anchored target is now exact, rather than merely a sufficient stronger
hypothesis: sup_n J_n(x)=infinity iff the original fixed-survivor R is infinite.
A hypothetical bounded-J actual survivor has a far tail which becomes ZERO
after the common time h_J(K), with the finite support bound (8). This is an
exact alternative for a future coupling argument; naming it does not exclude it.

The branch self-trace is at the fixed physical column -2 at even times,
whereas P_n follows the left-moving pair (-2n-t,-2n-t-1). No step above
transfers those branch events onto the rays. Finite Q levels do not make an
F orbit stay in one level, and (12) warns even against importing A-invariance.
Full-fringe exclusion of every bounded level remains unproved. No new
ray, period, prefix, finite-level, or forced-orbit search is authorized.
