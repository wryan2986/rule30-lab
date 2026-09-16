# Problem 1: exact classification of one-step reverse predecessors

## Status

Problem 1 remains open. This note strengthens the run-64 reset lemma from an at-most-one statement to a complete existence-and-cardinality theorem.

The reconstruction recurrence is

    q_(i+2) = S q_i xor (q_(i+1) OR q_i).

Given two consecutive output-side words `u=q_(i+1)` and `w=q_(i+2)`, a predecessor `x=q_i` must solve

    w = Sx xor (u OR x).

Coordinates are indexed cyclically modulo the temporal period `p`, with `(Sx)_j=x_(j+1)`. Thus

    x_(j+1) = w_j xor (u_j OR x_j).

## Theorem: complete predecessor classification

For every cyclic pair `(u,w)`:

1. If `u != 0`, there exists exactly one cyclic predecessor `x`.
2. If `u = 0`, predecessors exist iff `w` has even XOR parity. In that case there are exactly two, and they are complements. If `w` has odd XOR parity there is no predecessor.

Thus reverse reconstruction is a total deterministic map everywhere off the hyperplane `u=0`; every failure of existence and every branching event occurs exactly at a zero middle column.

## Proof when u != 0

Run 64 proved uniqueness by the reset mechanism. Existence is just as rigid and does not require search.

Choose any index `k` with `u_k=1`. The coordinate equation at `k` loses dependence on `x_k`:

    x_(k+1) = w_k xor 1.

This fixes `x_(k+1)` outright. Now apply the recurrence successively at

    k+1, k+2, ..., k-1  (mod p).

Each step deterministically fixes the next bit, eventually determining `x_k`. At that point every coordinate equation except possibly the one at `k` has been used. But the equation at `k` was exactly the anchor equation that initially fixed `x_(k+1)`, and because `u_k=1` it is independent of the newly determined value of `x_k`. Hence it is automatically satisfied.

Therefore a cyclic solution always exists. The reset lemma shows it is unique.

This also gives an O(p) constructive predecessor algorithm: locate one `1` in `u`, set the bit immediately after it to `w_k xor 1`, and sweep once around the cycle.

## Proof when u = 0

The equation becomes

    Sx xor x = w.

XORing all coordinates of the left side gives zero, so even XOR parity of `w` is necessary. If `w` has even parity, choose `x_0` arbitrarily and integrate

    x_(j+1)=w_j xor x_j.

Even parity is exactly the cyclic closure condition. The two choices of `x_0` produce two solutions differing by the constant-one word, hence they are complements.

## Structural consequence for the reverse basin

There are no hidden compatibility failures inside a nonzero connector segment. Once a reverse trajectory leaves a zero-column singularity with `u != 0`, its predecessor exists uniquely at every subsequent step until the next time the middle column becomes zero.

Accordingly the entire reverse basin can be compressed to a sequence of zero-column return events. At a state `(u,w)=(0,w)` only three things can happen:

- `parity(w)=1`: the reverse path dies;
- `parity(w)=0`: exactly two complementary lifts occur;
- after either lift, all intervening reverse motion is forced until the next zero middle column.

Combined with the derivative-lift antiperiodicity lemma, the known scale-transition lifts are one temporal necklace modulo phase. Therefore an all-scale uniqueness proof no longer needs to control arbitrary reverse states or prove existence along connector segments: it needs only classify the zero-column return map and show that all surviving even-parity lifts are equivalent modulo temporal phase in the relevant basin.

## Next target

Define the induced first-return map from one zero-middle-column state to the next. For an even-parity target `w`, integrate `Sx xor x=w`, choose either complementary lift, then apply the unique O(p) predecessor rule until the middle column next becomes zero (or until the legal initial boundary is reached). Determine whether this return map descends to a single-valued map on temporal necklaces. If it does, the apparent binary reverse tree collapses to a one-dimensional necklace dynamics, which is the natural setting for proving the unique terminating-necklace conjecture.
