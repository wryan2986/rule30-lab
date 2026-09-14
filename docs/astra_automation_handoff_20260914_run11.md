# Astra automation handoff — run 11

Problem 1 remains **OPEN**.

This run starts from branch head `60a6d796436c0b6867ce41bd8cf29ee8bcf1a55f` and adds `proofs/informal/problem1_post_threshold_half_bound_sharp.md`.

## New exact obstruction

The run-10 post-threshold causal estimate

    d_H >= ceil((Q_H+1)/2)

is sharp even in the canonical common-origin tower `v=1`.

For `v=1`,

    h_0=0,
    h_1=1,
    h_2=2,

so `n=2` is a genuine plateau entry with height `H=2` and common-origin threshold `2H=4`.

The physical row at that threshold is

    T^2(1)=25.

Its literal zero extensions have exact `A`-cycles

    25  -> 27  -> 25,
    50  -> 55  -> 50,
    100 -> 111 -> 100,
    200 -> 222 -> 200,
    400 -> 444 -> 401 -> 445 -> 400.

Thus `tau(25*2^q)=0` for `0<=q<=4`.

But

    800 -> 888 -> 802 -> 891 -> 801 -> 889 -> 803 -> 891 -> ...,

so

    tau(800)=3.

Therefore the height-2 plateau has

    Q_H=5,
    d_H=3,

and hence

    d_H=ceil((Q_H+1)/2).

Its complete post-threshold signed excess change is

    d_H-Q_H=-2.

## Routes now fenced off

This exact physical example disproves the following universal local strengthenings:

1. `d_H >= Q_H` at every post-threshold plateau exit;
2. `Q_H <= 2H` for every plateau reaching the threshold;
3. any theorem asserting a strict universal improvement over the existing half-depth lower bound at every exit without extra hypotheses excluding the `v=1,H=2` case.

So the run-10 option of forcing essentially full repayment at each individual plateau exit cannot be the proof mechanism in this form.

## Preferred next target

Move from a single-exit inequality to an inter-plateau coupling theorem.

A useful theorem would show that a negative local charge

    d_H-Q_H < 0

forces compensating positive excess later, with bounded reuse of the same structural event. The proof must use information beyond the scalar pair `(Q_H,d_H)` at one plateau exit — for example phase/core information transported into the next rise, or a genuinely non-telescoping global charge.

Do not retry `d_H>=Q_H` or `Q_H<=2H`; both fail on the exact single-cell tower.

New proof commit before this handoff: `edcce7eb9c6a8d61e23de4fa33626edb9097fe26`.
