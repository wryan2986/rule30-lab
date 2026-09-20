# Surviving g=2 front itineraries are indistinguishable to the cyclic core transition

Status: `stopping-fence` / structural reduction. Problem 1 remains OPEN.

## Setup

Continue the sufficiently late two-bit nonresetting `t` source in the eventual K=3 branch and put `q=t+2`. Runs 156--157 reduce terminal hidden slack `g_{t+5}=2` to exactly two still-possible original-cut residence itineraries

    A: (d_2,d_3,d_4,d_5) = (1,0,0,4),
    B: (d_2,d_3,d_4,d_5) = (0,1,0,4).

The third scalar possibility `(0,0,1,4)` is excluded because its one-step residence would require `r_2(q)=1`, whereas the distinguished cyclic source has

    (r_-5,...,r_2)(q) = 10101110,

so `(r_0,r_1,r_2)(q)=(1,1,0)`.

The run157 handoff proposed testing A and B against the cyclic gate/core transition from `q` to `q+2`.

## Exact core transition

That test cannot distinguish A from B. The already established nonreset-return theorem gives, on the same actual FULL domain, that `Y_q` is cyclic with actual gate `t`, `Y_{q+2}` is cyclic with actual gate `u`, and for the complete core `z=Z_t`,

    Z_{q+2} = G(z) = 16 A^4 z + 7.

Equivalently its complete code is

    I_3 I_1 shift^4 Theta(z).

This identity is determined by the two-bit nonresetting source and the paired cyclic scan. It contains no original-cut residence variable `d_2,d_3,d_4` and was proved before any choice between A and B was made. Both surviving itineraries therefore have exactly the same certified cyclic gate sequence

    gate(q)=t,  gate(q+2)=u

and the same certified complete-core transition `z -> G(z)`.

This is not merely a failure of a finite prefix test. Within the currently proved identities, the *entire* complete cyclic code at `q+2` is already fixed as the same function of the incoming core `z` in both cases. Hence no predicate depending only on `Theta(Z_q)`, `Theta(Z_{q+2})`, their gate symbols, or the exact map `G` can separate A from B unless one first proves an additional theorem linking that predicate to the original-cut residence itinerary.

## Where the distinction actually lives

The two cases differ only in which characteristic receives the unique one-step residence before the two skips:

    A: characteristic t+3 is visited once; t+4,t+5 are skipped.
    B: characteristic t+3 is skipped; t+4 is visited once; t+5 is skipped.

At the common starting row `q`, the one-step residence endpoint condition asks respectively for

    A: r_0(q)=1,
    B: r_1(q)=1.

The distinguished source forces both bits to 1. Thus the local residence certificate also fails to distinguish them. The common four-step terminal residence was already classified in run155 and reduces to the separate condition `r_3(q)=1`; it likewise does not choose A versus B.

Therefore the unresolved information is genuinely the position of the *global original-cut discrepancy front*, not the cyclic core or the already-known local eraser bits.

## Consequence / stopping fence

Do not spend another run comparing the two survivors using only the `q -> q+2` cyclic gate/core map: the complete map is identical on both alternatives by construction.

To make progress on `g=2`, one needs a bridge theorem that couples original-cut residence to some all-depth object not erased by the core quotient. Concretely, one of the following would suffice:

1. an exact condition for `d_2=1` versus `d_3=1` in terms of the complete global E-shadow/discrepancy tail at `q`;
2. a proof that one of the two one-step erasers (`r_0(q)` or `r_1(q)`) cannot be the *first* eraser for its characteristic once the full earlier discrepancy tail is imposed; or
3. a fully admissible finite-support witness realizing either A or B, which would show that the present hidden-slack route cannot exclude `g=2` without additional global input.

The core quotient itself has discarded exactly the information needed to choose between A and B.

Dependencies: `problem1_run156_g2_forces_two_skips_then_four_step_residence.md`; `problem1_run157_g2_third_itinerary_excluded_by_source_bit.md`; `problem1_nonreset_return_birth_spacing.md`; `problem1_run155_g2_residence_trace_collapses_to_single_driver_bit.md`.
