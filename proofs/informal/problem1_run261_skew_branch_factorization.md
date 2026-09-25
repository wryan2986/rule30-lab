# Problem 1 run 261 — factor the 32-step skew branch

Problem 1 remains open. Continuing run 260, write

[
b=x_0Q
]

with

[
Q=1\oplus x_1\oplus x_2\oplus x_1x_2x_3\oplus x_1x_2x_4
\oplus x_1x_2x_3x_4\oplus x_5\oplus x_1x_5\oplus x_2x_5.
]

## New exact Boolean factorization

In the Boolean quotient ring, where (x_i^2=x_i),

[
\boxed{Q=(1\oplus x_1\oplus x_2)
(1\oplus x_5\oplus x_1(x_3\lor x_4)).}
]

Direct Boolean expansion reproduces the nine-term ANF from run 260. Hence

[
\boxed{b=1\iff x_0=1,quad x_1=x_2,quad
x_5=x_1(x_3\lor x_4).}
]

Thus the skew branch consists of two cases:

- (x_1=x_2=0, x_5=0);
- (x_1=x_2=1, x_5=x_3\lor x_4);

always with (x_0=1), while (x_3,x_4,x_6,x_7,x_8) are otherwise free.

This also explains exactly the 64 states with (b=1) in run 260:
(2\cdot4\cdot8=64).

The remaining target (b=1\Rightarrow W=1) can now be proved after substituting these simple state constraints rather than carrying the nine-term relation. Because (W)'s selector uses times congruent to 0 or 1 mod 4, the next useful attack is a four-step recurrence in the two cases above.

This is a Boolean-ring factorization; idempotence is essential.
