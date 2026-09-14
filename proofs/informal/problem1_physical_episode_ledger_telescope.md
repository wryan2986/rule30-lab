# Physical episodes telescope in the residence ledger

Status: `partial-proof`. This is an exact bookkeeping consequence of the
already established global-front identities and the pushed nonreset-return
profile. It does not solve Problem 1. Its purpose is to close a tempting
but insufficient route: treating a forced local birth as an independently
positive contribution to the shift-tail residence ledger.

## 1. Endpoint telescoping identity

Fix the ORIGINAL finite actual row and its original-cut delays

    s_j = tau(L_j(r(0))).

The residence length of characteristic `j+1` is

    Delta_j = s_(j+1)-s_j >= 0.

Its signed contribution to the shift-tail excess ledger is therefore

    Delta_j - 1.

For any integers `a<b`, summing gives the exact identity

    sum_(j=a..b-1) (Delta_j-1)
      = s_b-s_a-(b-a)
      = (s_b-b)-(s_a-a).                         (1)

The global-front threshold formula is

    tau(Y_j)=max(s_j-j,0).                         (2)

Hence whenever BOTH endpoint physical delays are positive,

    sum_(j=a..b-1) (Delta_j-1)
      = tau(Y_b)-tau(Y_a).                         (3)

No FULL assumption is needed for (1)-(3). The identity is just the signed
residence ledger written in physical coordinates, but it is an important
fence on local-passage arguments: a passage that starts and ends at the
same positive delay has exactly zero total ledger charge, regardless of
how many births, skips, or long residences occur internally.

More generally, concatenating such passages only telescopes their endpoint
delays. Therefore a family of bounded-delay local episodes cannot yield an
independent positive ledger budget unless it also forces the positive
endpoint delays themselves to rise without bound, or it supplies additional
information at zero-delay endpoints where (2) loses the negative value of
`s_j-j`.

## 2. The forced two-bit nonreset birth has net charge -1

Use the pushed profile in `problem1_nonreset_return_birth_spacing.md`.
At a two-bit nonresetting even source (`u=0`) at physical time `t`, the
exact delays through the forced next birth are

    tau(Y_t),...,tau(Y_(t+6)) = 2,1,0,0,0,0,1.    (4)

The endpoint delays in (4) are positive, so (3) applies directly with
`a=t`, `b=t+6`:

    sum_(j=t..t+5) (Delta_j-1) = 1-2 = -1.         (5)

Thus the forced birth at `t+6` does create a new positive-delay row, and
there must be residence length supporting that birth, but the WHOLE
conditional passage from the nonreset source through that birth is not a
positive ledger event. Its exact signed charge is `-1`.

This rules out the current hoped-for inference

    late two-bit nonreset source
      -> forced birth at t+6
      -> prefix-independent positive P-Z gain.

The last arrow is false even on the actual FULL domain on which the pushed
source profile was proved.

## 3. Including the immediately created resetting t-source does not help

The same pushed note states that when the forced `beta=1` birth occurs,
`Y_(t+6)` is a one-bit `t` source and its core is resetting. The complete
one-bit passage table in `problem1_exit_wait_front_residence.md` gives the
two possible `t`-source delay triples

    1,1,1

or

    1,0,1.                                         (6)

Either way the endpoints at `t+6` and `t+8` both have positive delay one.
Equation (3) therefore gives

    sum_(j=t+6..t+7) (Delta_j-1) = 1-1 = 0.        (7)

Combining (5) and (7), the eight-step segment beginning at the two-bit
nonreset source and including the full immediate resetting one-bit passage
still has exact charge

    sum_(j=t..t+7) (Delta_j-1) = -1.               (8)

So extending the forced-birth episode by its first resetting passage does
not recover a positive local budget.

## 4. One-bit nonreset sources are no better as isolated birth events

For the one-bit nonreset source (`u=1`), the pushed profile has source
delay `d=1` and terminal birth indicator `beta in {0,1}` at `t+6`.
If `beta=1`, both endpoints have delay one, so (3) gives exact six-step
charge zero. If `beta=0`, the terminal physical delay is zero and (3) is
not available because `s_(t+6)-(t+6)` may be negative; in particular the
profile supplies no forced positive ledger gain.

Thus neither type of nonreset passage gives the desired local positive
charge merely from the existence of the next birth.

## 5. Consequence for the current strategy

The physical-time tail conjugacy remains useful, but the proposed next step
in the automation handoff needs refinement. A restart-local FULL obligation
cannot be counted as an additive positive residence-ledger charge solely
because it forces a birth. Equation (3) shows that, on any episode with
positive endpoints, all internal births and skips have already telescoped
to the change in physical delay.

A viable next mechanism must therefore do at least one of the following:

1. force endpoint physical delay to increase by an amount that cannot later
   be repaid under the assumed bounded strip;
2. control the hidden negative excess `s_j-j` at zero-delay rows, where the
   truncation `tau(Y_j)=max(s_j-j,0)` discards information; or
3. introduce a genuinely non-telescoping global charge, distinct from the
   signed residence sum itself, with bounded reuse on the original finite
   fringe.

In particular, separated forced births from
`problem1_nonreset_return_birth_spacing.md` cannot simply be summed into a
contradiction. Their local residence surplus can be, and in the two-bit
profile is, absorbed by skips inside the same exact original-cut ledger.

Dependencies: `problem1_global_discrepancy_front.md` Sections 1-3;
`problem1_nonreset_return_birth_spacing.md` Sections 1-4;
`problem1_exit_wait_front_residence.md` Section 4;
`problem1_shift_tail_residence_ledger.md`.
