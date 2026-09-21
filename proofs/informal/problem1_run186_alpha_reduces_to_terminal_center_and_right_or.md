# Run 186: the t+8 candidate bit reduces to one terminal center bit and one right-OR

Status: `partial-proof` / obstruction refinement. Problem 1 remains OPEN.

## Setup

Continue the sufficiently late one-bit gate-u nonresetting passage in the terminal `beta=1` branch. Run 180 gives at physical row `t+6`

    actual (r_1,r_2) = (0,1),
    shadow (h_1,h_2) = (1,1).

Run 181 writes

    x := r_0(t+6)

and proves at `t+7`

    (r_0,r_1,r_2) = (1 XOR x, 1 XOR x, 0).

Run 185 defines

    y := 1 XOR x,
    p := r_3(t+7),
    alpha := y XOR p,

so that `(r_1,r_2)(t+8)=(0,alpha)`. Under the hypothesis `N_(t+8)`, `alpha` completely selects the candidate source type and exact delay.

## Eliminate the intermediate bit p

No core classification is needed to express `p` directly in the terminal row. Rule 30 at position 3 from `t+6` to `t+7` gives

    p = r_3(t+7)
      = r_2(t+6) XOR (r_3(t+6) OR r_4(t+6)).

Since run 180 fixes `r_2(t+6)=1`, put

    omega := r_3(t+6) OR r_4(t+6).

Then

    p = 1 XOR omega.

Substituting into run 185's definition,

    alpha = (1 XOR x) XOR (1 XOR omega)
          = x XOR omega.

Hence the exact candidate-control bit is

    alpha = r_0(t+6) XOR (r_3(t+6) OR r_4(t+6)).      (1)

This is an exact physical Rule-30 identity on the actual passage, not a cyclic-source or birth-law statement.

## Consequence

Run 181's proposed target of determining only `x=r_0(t+6)` is insufficient to determine the `t+8` candidate gate. Even after the rigid terminal right pair `01` is imposed, the two cells immediately beyond that pair enter through the single Boolean

    omega = r_3(t+6) OR r_4(t+6).

Thus the unresolved complete-driver information at the first allowed recurrence is exactly the pair `(x,omega)`, and only through their XOR. In particular:

    alpha=1 iff x != omega,
    alpha=0 iff x = omega.

Combining with run 185, if `N_(t+8)` holds then

    x != omega  => gate u, tau(Y_(t+8))=1, Delta_(t+7)=2,
    x =  omega  => gate t, tau(Y_(t+8))=2, Delta_(t+7)=3.

So determining the terminal center alone cannot close the branch unless another theorem also fixes `omega` or relates it to `x`.

## Dead end / fence

The resetting label at `t+6` by itself does not currently provide an identity for `omega`. The nonresetting-core theorem cannot be applied there: the `beta=1` endpoint is explicitly a resetting one-bit t-source. Likewise the cyclic-source birth law is unavailable because this endpoint is noncyclic. Treating either `r_3(t+6)` or `r_4(t+6)` as a fresh free fringe bit would lose the same complete-driver compatibility that earlier runs were designed to preserve.

The next useful target is therefore not another unconstrained gate-prefix extension. It is to transport the complete code of the known cyclic row

    Y_(t+4)=G(z)=16 A^4 z+7

through the forced beta=1 birth and express `x XOR omega` in terms of that same complete driver `z` (or its already-defined shadow cells). A simplification or invariant there could decide `alpha`; failure would identify exactly which deeper driver symbol first survives into the t+8 recurrence.

Dependencies: `problem1_run180_terminal_shadow_pair_is_rigid.md`; `problem1_run181_beta_one_forces_tplus7_front.md`; `problem1_run185_tplus8_nonreset_candidate_has_exact_delay.md`; `problem1_nonreset_return_birth_spacing.md`.
