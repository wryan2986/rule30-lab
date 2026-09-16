# Problem 1: reverse predecessor uniqueness/reset lemma

## Status

Problem 1 remains open. This note continues the reverse-basin/derivative-lift program after run 63.

## Reverse predecessor equation

For the reconstruction

    q_(i+2) = S q_i xor (q_(i+1) OR q_i),

suppose two consecutive later columns are fixed. Writing

    u = q_(i+1),
    w = q_(i+2),
    x = q_i,

a predecessor must solve

    w = Sx xor (u OR x).

Coordinatewise (with cyclic indices),

    x_(j+1) = w_j xor (u_j OR x_j).

This gives a simple but useful complete uniqueness criterion.

## Lemma

If `u != 0`, the reverse predecessor equation has **at most one** cyclic solution `x`.

If `u = 0`, it reduces to

    Sx xor x = w.

In that case it has either zero solutions or exactly two solutions; when two exist they are complements. Solvability is equivalent to even XOR parity of `w`.

## Proof

Take two putative solutions `x,y` and define their difference

    delta_j = x_j xor y_j.

If `u_j=0`, the coordinate update is

    x_(j+1)=w_j xor x_j,

so

    delta_(j+1)=delta_j.

If `u_j=1`, however,

    x_(j+1)=w_j xor 1

is independent of `x_j`, and therefore

    delta_(j+1)=0.

Thus a `1` anywhere in `u` resets the difference of any two candidate predecessor solutions to zero. Subsequent coordinates can never recreate a difference: a site with `u=0` copies zero and a site with `u=1` resets to zero again. Going around the cycle therefore gives `delta=0` everywhere. Hence at most one cyclic predecessor exists whenever `u` is nonzero.

When `u=0`, the equation is the cyclic discrete derivative `(S+I)x=w`. Its kernel consists of the two constant words, so a solvable equation has exactly two complementary solutions. XORing all coordinate equations shows the necessary parity condition `xor_j w_j=0`; conversely, fixing `x_0` and cumulatively integrating `w` closes around the cycle exactly under this parity condition. Therefore parity zero is also sufficient.

## Consequence for the reverse-basin program

This sharply localizes **all possible reverse branching**. There is no hidden branching anywhere along a connector while the middle/current column `u` is nonzero. Every genuine branch can occur only at a state whose relevant column is exactly zero, and then the branch is precisely a discrete-derivative integration event.

This explains structurally why the singularities found at reverse depths 9, 30, and 401 all had the form

    Sx xor x = h.

Those are not merely three examples of a common-looking obstruction: **this is the only possible mechanism by which reverse predecessor uniqueness can fail at all.**

Combined with run 63, when the derivative right-hand side is a doubled odd-parity lower-period word `E(c_p)`, the two solutions are complements and are related by the half-period shift, hence form one temporal necklace. Therefore that scale-transition singularity is unique modulo phase.

## What remains

The unique-necklace induction is now reduced further. To prove rigidity of the post-lift connector, it is enough to control occurrences of a zero middle column `u` along reverse propagation. Between such zero-column events, predecessor propagation is automatically unique by this lemma; no separate connector-wide uniqueness argument is needed.

A particularly useful next theorem would be:

> Starting from the canonical doubled-period derivative lift, every subsequent zero-column event before the legal initial pair either (a) is impossible, or (b) has an even-parity derivative RHS whose two integrations are the same temporal necklace modulo phase.

If this can be established recursively, reverse-basin uniqueness modulo temporal rotation would follow without enumerating arbitrary predecessor trees.
