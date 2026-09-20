# Global return-shadow identity excludes terminal hidden slack g=2

Status: `partial-proof` / structural advance. Problem 1 remains OPEN.

## Setup

Continue the sufficiently late TWO-BIT nonresetting source `t` in the eventual K=3 branch and put `q=t+2`. Let `g=g_{t+5}` be the terminal hidden original-cut slack immediately before the forced birth at `t+6`.

Runs 154--159 reduced the only unresolved maximal case `g=2` to two possible global-front itineraries and then translated those itineraries into exact conditions on the ORIGINAL global E-shadow at the distinguished cyclic row `q`:

    A: (d_2,d_3,d_4,d_5)=(1,0,0,4)
       => hat r_1(q)=0;

    B: (d_2,d_3,d_4,d_5)=(0,1,0,4)
       => (hat r_1(q),hat r_2(q))=(1,1).

The third scalar itinerary `(0,0,1,4)` was already excluded by the actual distinguished source bit `r_2(q)=0`.

## Previously established complete-shadow identity

The older all-depth nonreset-return theorem retained the SAME original finite actual FULL row and its SAME global E-shadow. At an even nonresetting source `t`, with `u` the actual gate-u indicator and `(a,b)=(hat r_3(t),hat r_4(t))`, it proves exactly

    (hat r_1(q),hat r_2(q)) = (1, u*(a OR b)),    q=t+2.

This is equation (3) of `problem1_nonreset_return_birth_spacing.md`. It is not a newly initialized local shadow and not a finite-prefix surrogate: the proof explicitly transports the original global E-shadow.

For the TWO-BIT source considered here, that theorem has `u=0`. Therefore

    (hat r_1(q),hat r_2(q)) = (1,0).              (*)

## Exclusion of both surviving g=2 itineraries

Compare (*) with the exact front patterns from run159.

Case A requires `hat r_1(q)=0`, contradicting `hat r_1(q)=1` in (*).

Case B requires `(hat r_1(q),hat r_2(q))=(1,1)`, contradicting the second bit `hat r_2(q)=0` in (*).

Run157 already excluded the only third scalar itinerary. Hence there is no `g=2` itinerary left:

    g_{t+5} != 2.

Together with run154, which excluded `g=3`, and nonnegativity of hidden slack,

    boxed: 0 <= g_{t+5} <= 1.

Using the exact repayment identity from run153,

    d_5 = s_{t+6}-s_{t+5} = g_{t+5}+2,

we obtain the improved terminal jump bound

    boxed: s_{t+6}-s_{t+5} in {2,3}.

Equivalently, the four-step scalar possibility and every larger one have now been excluded on the actual FULL/global-shadow domain.

## Why this bridge was previously missed

Run158 correctly found that the complete cyclic-core transition cannot distinguish the two `g=2` survivors: the quotient discards the original-cut front position. Run159 then localized the missing information to the first two bits of the original global shadow. Those exact bits had already been computed in the older nonreset-return theorem. Combining the two results closes `g=2` without any new cone search.

This is an all-depth synthesis of two previously established identities, not a claim that arbitrary local neighborhoods with these bits are globally admissible.

## Remaining branch

The hidden-slack route is now reduced to `g in {0,1}`. If `g=1`, run155's residence classification requires `r_3(q)=1`, but the original shadow at q is fixed only through `(hat r_1,hat r_2)=(1,0)` by the return identity above. Excluding `g=1` therefore needs one more bridge between the original-cut residence and either a wider transported shadow bit or another all-depth invariant. Do not revisit `g=2` local residence/core cases.

Dependencies: `problem1_run159_g2_itineraries_equal_exact_shadow_front_patterns.md`; `problem1_run157_g2_third_itinerary_excluded_by_source_bit.md`; `problem1_run154_distinguished_source_excludes_maximal_hidden_slack.md`; `problem1_run153_zero_plateau_slack_exact_repayment.md`; `problem1_nonreset_return_birth_spacing.md` equation (3).
