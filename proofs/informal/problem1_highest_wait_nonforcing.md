# The current highest-disagreement wait does not bound the whole delay

Status: `partial-proof` for the lead-audited all-depth arguments;
`refuted` for the universal scalar bound stated in Section 3. Fresh external
adversarial review was unavailable; its absence and the lead disposition
are recorded in problem1_round10_fresh_review.md. Problem 1 remains OPEN.
No experiment is required for this proof.

## 0. Admission and scope

The round-nine erasing formula is exact at the highest differing bit but
does not assert equality with the whole-row preperiod. Determine whether
there is at least a universal upper bound on the latter in terms of that
one initial waiting time. A positive answer would justify concentrating on
the current highest driver; a negative answer requires following subsequent
erasures or the new physical delay-injection recurrence.

The counterfamily below consists of initially finite positive rows, in the
single shift tower 2^n*7. It does not construct a FULL orbit. In particular
2^n*7 is a moving INITIAL cut of one finite seed, not its actual time-n row.
The distinction is essential to the final scope statement.

## 1. A finite seed cannot have an entirely cyclic zero-extension tower

Claim (`partial-proof`). For any positive finite integer v, it is impossible
that 2^k v is A-periodic for every k>=0. The same conclusion holds after
any finite starting depth by replacing v with that shifted integer.

Suppose otherwise and let p_k be the least A-period of 2^k v. Their widths
grow strictly with k. Full-code injectivity makes the set of finite
A-periodic states of period at most any fixed P finite: at most
sum_(p=1..P)4^p purely periodic codes are available. Consequently p_k
tends to infinity. One-bit extension preserves or doubles the least
period, so at some k, p_(k+1)=2p_k.

Put y=2^k v and z=2y. The doubling classification forces the low A-trace
of y to be identically zero. For b_s=bit_0(A^s z), the pure code of z
is (b_s,0). Doubling forces b to visit both 0 and 1: its return over one
input period flips the bit. If w_s is the low trace of 2z, its driven
recurrence is therefore

    w_(s+1)=b_s OR w_s, w_0=0.                       (1)

The drive b is periodic and contains 1. Its unique recurrent response is
identically 1. Hence 2z is not A-periodic, contrary to the supposed cyclic
tower. This is a contradiction at the second extension following the
doubling source, not an argument from merely large finite widths.

## 2. Every positive finite shift tower has unbounded least preperiod

Claim (`partial-proof`). For every positive finite integer x,

    tau(2^n x) tends to infinity as n tends to infinity. (2)

Each term is finite because A preserves positive finite width. The terms
are nondecreasing, since sigma(2^(n+1)x)=2^n x and spatial deletion cannot
increase a least preperiod. It suffices to rule out a uniform upper bound H.

If such H existed, A^H(2^n x) would be A-periodic for every n. For n>=2H,
the reviewed A^H=sigma^(2H) T^H and T's commutation with multiplication by
2^n give the exact integer identity

    A^H(2^n x)=2^(n-2H) T^H(x).                      (3)

Here T(x)=x XOR ((x<<1) OR (x<<2)). The finite integer T^H(x) is positive:
T is injective, fixes zero, and sends finite integers to finite integers.
As n runs over all integers >=2H, (3) would make every zero extension of
that fixed positive integer A-periodic. Section 1 excludes this. This
proves (2), including convergence rather than only an unbounded subsequence.

No bound on the rate in (2) is claimed. In particular it does not assert
tau(2^n x)>n infinitely often or even once.

## 3. A constant first wait and an unbounded whole-row delay (`refuted` bound)

For every n>=0 set y_n=2^n*7 and z_n=cyc(y_n). The hand identities are

    A(7)=6, A(6)=6, cyc(7)=6.

Cycle completion commutes with sigma^n, so

    sigma^n y_n=7, sigma^n z_n=6.                    (4)

The bits above n agree, bit n differs, and the common bit at n+1 is 1.
Thus the HIGHEST differing bit is exactly n. The exact round-nine waiting
formula at that bit gives

    tau(sigma^n y_n)=1,
    1+min{s>=0:bit_(n+1)(A^s z_n)=1}=1.              (5)

The first highest disagreement is erased at the very first A step for
EVERY n. Nevertheless Section 2 gives tau(y_n) tending to infinity.

Therefore the following proposed local assertion is refuted:

    There exists f:N_(>=1)->N such that for EVERY initially finite
    nonperiodic y, tau(y)<=f(w(y)), where w(y) is its current
    highest-disagreement erasing wait.

Indeed w(y_n)=1 and tau(y_n) is unbounded. This also refutes equality of
the two quantities, but the stronger unbounded separation is the new point.
The function's codomain contains finite integers; allowing f(1)=infinity
would remove the substantive claim.

## 4. Why the rest of the erasing history remains necessary (`partial-proof`)

For any initially finite eventually A-periodic y, follow A^s y against
A^s cyc(y), with no physical extension. Higher bits depend only on higher
inputs, so an erased highest disagreement can never be recreated at or
above that position by lower disagreements. If y is already periodic, the
erasing history is empty and its delay is zero. Otherwise, at each time s_j when the
disagreement set is nonempty, let d_j be its highest position and put

    w_j=1+min{r>=0:bit_(d_j+1)(A^(s_j+r)cyc(y))=1},
    s_(j+1)=s_j+w_j, s_0=0.                         (6)

The minimum exists by the same projected wrong-lift argument as in the
round-nine note. At s_(j+1) the next highest disagreement, if any, is
strictly below d_j. After at most d_0+1 such erasures no disagreements
remain. At every earlier time in a waiting interval the current highest
bit still differs. Hence the LEAST whole-row preperiod is exactly

    tau(y)=sum_j w_j.                               (7)

The later d_j and waits must be evaluated on the evolved complete row:
lower disagreements may have changed or already vanished during a wait.
Formula (7) does not replace them with their initial values, nor assert
that every bit initially different needs a separate erasure.

## 5. Scope and restart fence (`inconclusive` for FULL)

The no-go concerns one CURRENT highest wait on finite rows. It does not
show all waits in (7) are bounded in the family, and it does not refute a
claim that uses the entire erasing history or the full actual right fringe.

With zero initial right half, the ACTUAL center-and-left row of seed 7 at
time n is Y_n=A^n(2^n*7). Thus

    tau(Y_n)=max(tau(2^n*7)-n,0).                    (8)

Nothing in (2) controls that difference. These actual rows are not claimed
to satisfy FULL or to have unbounded delays. In particular the new theorem
does not settle the desired one-orbit bounded-strip question and does not
turn later-row delay into the original anchored Q budget.

Do not sample further shifted rows to estimate a growth rate: the admitted
question is already settled by (2)-(5). The continuing task is the actual
infinite sequence of erasures or the resetting lifts at inherited horizons.

Dependencies: problem1_physical_time_cycle_defects.md Sections 1,4,6;
problem1_cycle_completion_defect_transport.md Sections 1,5;
problem1_scan_doubling_cycle_lag.md Section 1 (finite-code counting);
the reviewed identities for T, A and spatial deletion. The exact external
review failures and final lead disposition are recorded separately.
