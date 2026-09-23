# Astra automation handoff — run 229

Problem 1 remains open.

## New all-depth result

Run 229 followed run 228's proposed square-map route. For `r>=4`, if

`c = x_{r-2} OR x_{r-3}` and `d = x_{r-3} OR x_{r-4}`,

then the exact two-step update is

\[
T_R^2(x)_r=x_r\oplus h_r(x),
\]

with

\[
h_r=c\oplus d\oplus x_{r-1}d\oplus x_{r-2}c\oplus cd.
\]

This follows from the Boolean identity

\[
(a\lor b)\oplus((a\oplus c)\lor(b\oplus d))
=c\oplus d\oplus ad\oplus bc\oplus cd.
\]

## Interpretation / dead end

Squaring preserves triangularity but does not preserve the original two-neighbor OR forcing family. The forcing window expands to four lower coordinates and the ANF becomes more complicated. Therefore the tempting repeated-squaring self-similarity route from run 228 does not close naively.

Do not spend another run merely expanding `T^(2^q)` symbolically; complexity is expected to grow.

## Better continuation

Exploit the order filtration instead. Since `O_r=2^{m_r}` and `O_r | O_{r+1}`, `T_R^{2^q}` fixes every prefix coordinate `r` with `m_r<=q`. Study the first coordinate above that frozen prefix as a skew extension. Try to express the next doubling criterion using only the forcing accumulated over one frozen-prefix cycle. This attacks the actual target `m_R` without carrying the full repeated-square polynomial.

Detailed proof: `proofs/informal/problem1_run229_exact_square_map_forcing.md`.