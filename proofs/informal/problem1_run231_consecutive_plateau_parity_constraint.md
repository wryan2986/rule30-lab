# Problem 1 — run 231: consecutive plateau parity constraint

Problem 1 remains open.

## Setup

Use the near-edge triangular automata from runs 223–230. Let

\[
T(x)_r=x_r\oplus(x_{r-1}\lor x_{r-2})
\]

(with the established boundary conventions), let `O_s` be the order of the width-`s` prefix, and define

\[
G_s(x)=\bigoplus_{t=0}^{O_s-1}(x_s(t)\lor x_{s-1}(t)).
\]

Run 230 proved

\[
O_{s+1}=O_s \iff G_s\equiv0.
\]

Also define the orbit parity

\[
p_r(x)=\bigoplus_{t=0}^{O_r-1}x_r(t).
\]

## Theorem: a second consecutive non-doubling forces lower top parity to vanish

Suppose

\[
O_{s-1}=O_s=O_{s+1}.
\]

Then

\[
\boxed{p_{s-1}\equiv0.}
\]

Equivalently, every orbit of the width-`s-1` automaton contains an even number of times at which its top coordinate is `1`.

### Proof

Flip only the newest coordinate `x_s` in a width-`s` state. The two trajectories remain identical below coordinate `s`, while coordinate `s` stays complementary at every time. For bits `a,b`,

\[
(a\lor b)\oplus((a\oplus1)\lor b)=1\oplus b.
\]

Therefore

\[
G_s(x)\oplus G_s(x\oplus e_s)
=\bigoplus_{t=0}^{O_s-1}(1\oplus x_{s-1}(t)).
\]

Because `O_s` is even (for the nontrivial widths under consideration), the constant ones cancel, giving

\[
G_s(x)\oplus G_s(x\oplus e_s)
=\bigoplus_{t=0}^{O_s-1}x_{s-1}(t).
\]

Under the first equality `O_{s-1}=O_s`, the lower trajectory has period dividing `O_{s-1}=O_s`, with no repetition multiplier, so the right side is exactly `p_{s-1}`.

Under the second equality `O_s=O_{s+1}`, run 230 gives `G_s\equiv0`. Hence the left side vanishes for every `x`, proving `p_{s-1}\equiv0`.

## Equivalent even-time cancellation

Run 228 proved

\[
p_{s-1}(x)=\bigoplus_{j=0}^{O_{s-1}/2-1}
\bigl(x_{s-2}(2j)\lor x_{s-3}(2j)\bigr).
\]

Thus a length-three constant-order plateau forces the all-state identity

\[
\boxed{
\bigoplus_{j=0}^{O_{s-1}/2-1}
(x_{s-2}(2j)\lor x_{s-3}(2j))=0.
}
\]

So consecutive non-doublings are not independent: the second one imposes a parity cancellation one full level lower in the filtration.

## More general derivative statement

Without assuming `O_{s-1}=O_s`, write `q_s=O_s/O_{s-1}\in\{1,2\}`. Then

\[
D_{e_s}G_s
=(q_s\bmod2)\,p_{s-1}.
\]

Hence:

- if the previous extension doubled (`q_s=2`), `G_s` is automatically insensitive to the newest bit;
- if the previous extension did not double (`q_s=1`), its newest-bit derivative is exactly `p_{s-1}`;
- if this non-doubling is followed by another non-doubling, `G_s\equiv0`, forcing `p_{s-1}\equiv0`.

The first two bullets are compatible with run 226; the third is the useful plateau consequence isolated here.

## What this does and does not prove

This is an all-depth necessary condition on constant-order plateaus. It does **not** yet bound plateau length or the exponent `m_R=v_2(O_R)`: vanishing of `p_{s-1}` may occur at many widths. The next useful question is whether `p_{s-1}\equiv0`, together with `G_{s-1}\equiv0`, forces an additional lower-level cancellation that can be iterated down a long plateau. If a plateau of length `L` forced `L-2` successively independent descended parity identities, one could hope to bound or classify plateau lengths.