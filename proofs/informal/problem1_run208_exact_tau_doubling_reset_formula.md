# Problem 1 run 208 — exact tau-doubling reset formula

Problem 1 remains OPEN.

This continues only the corrected run-193--207 chain.

## Setup

Let

    A(q) = (q >> 2) XOR ((q >> 1) OR q).

For fixed finite q, put

    r_k = A^k(q),
    s_k = A^k(2q).

Run 207 proved the exact decomposition

    s_k = 2 r_k XOR d_k,   d_k in {0,1},

with d_0=0 and one-bit update driven by the low two bits of r_k:

    00 : d' = d
    01 : d' = 1 XOR d
    10 : d' = 1
    11 : d' = 0.

The symbols 10 and 11 are resets.

Let

    a = tau(q),
    P = eventual period of q.

Thus r_{a+j+P}=r_{a+j} for all j>=0.

## Exact theorem

### Case 1: the eventual r-cycle contains no reset

Equivalently, bit_0(r_{a+j})=0 for every cycle phase j.

Then every driver map on d is either identity (00) or toggle (01). Starting from any d_a, the pair (r,d) is already periodic from time a: after one r-period, d is either unchanged, or toggled and hence returns after two r-periods.

Because s=2r XOR d and the decomposition into (floor(s/2), bit_0(s)) is unique,

    tau(2q) <= a.

So a strict increase tau(2q)>tau(q) is impossible in the no-reset case.

### Case 2: the eventual r-cycle contains a reset

There is a unique periodic defect phase d*_j over the r-cycle. Indeed, choose any reset in the period; its constant map fixes the outgoing d independently of the incoming value, after which all later phases are forced, including consistently through the next occurrence of that reset.

Compare the actual d_a with the periodic value d*_0 at lower-orbit cycle entry.

If

    d_a = d*_0,

then (r_a,d_a) is already on the periodic lifted cycle, hence

    tau(2q) <= a.

If

    d_a != d*_0,

let rho be the least j>=1 such that the transition from phase j-1 to phase j is a reset (driver symbol 10 or 11 at r_{a+j-1}). Before that reset all maps are bijections of one bit (identity/toggle), so the mismatch persists. At the reset both actual and periodic defect bits are forced to the same value, and from then onward they agree forever.

Therefore the lifted pair is not periodic before a+rho and is periodic from a+rho. Uniqueness of the decomposition s=2r XOR d gives the exact identity

    tau(2q) = a + rho.

Thus:

    tau(2q) > tau(q)

iff the lower eventual cycle contains a reset and d_a is out of phase with the unique periodic lifted defect response; when this happens, the increment is exactly the forward distance from cycle entry to the first reset.

Equivalently,

    tau(2q)-tau(q) = rho

in the mismatch case, with 1 <= rho <= P, and is <=0 otherwise.

## Shift-tower consequence

For

    q_n = 2^n x,
    a_n = tau(q_n),

any positive adjacent increment has the exact form

    a_n - a_{n-1} = rho_n,

where rho_n is the distance from the q_{n-1} cycle-entry phase to its first low-bit-1 cycle symbol, provided the run-207 defect bit is mismatched there. Otherwise a_n <= a_{n-1}.

Hence the true late-renewal condition from run 202,

    a_n > max(a_{n-1}, b+n),

is equivalent, in the only possible positive-increment case, to

    a_{n-1} + rho_n > b+n.

This is substantially sharper than merely saying that a phase mismatch is necessary: the entire amount of a positive tau jump is a concrete first-reset distance on the lower eventual cycle.

## Important dead end / warning

The hoped-for next lemma that such mismatches can occur only finitely often for fixed finite x is not supported by bounded exact computation. For x=1, direct exact orbit detection through n=119 shows many indices satisfying

    a_n > max(a_{n-1}, n),

including numerous indices near the end of that range. This is finite evidence only and is not a proof of infinitely many renewals, but it decisively warns against trying to prove mismatch finiteness from the one-bit automaton alone.

The one-bit automaton explains the increments; it does not by itself make them scarce.

## Next target

Do not try to prove eventual absence of reset mismatches without additional structure. The useful next question is whether the FULL hypothesis imposes a restriction on the *cycle-entry phases / first-reset distances* rho_n that is absent for an arbitrary shift tower such as x=1. In particular, combine

    a_n > max(a_{n-1}, b+n)

with the exact formula

    a_n = a_{n-1} + rho_n

and the existing global-front / complete-code identities. Any contradiction now has to use more than the adjacent-tower dynamics, because arbitrary finite x can exhibit many above-diagonal renewals.