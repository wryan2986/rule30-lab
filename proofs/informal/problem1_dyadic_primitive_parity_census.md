# Problem 1: exact parity census for dyadic primitive necklaces

## Statement

Let `n=2^m` with `m>=1`. Among binary necklaces of exact rotational period `n`:

- the number of odd-Hamming-parity primitive necklaces is exactly

  `N_odd(n) = 2^(n-1)/n`;

- the number of even-Hamming-parity primitive necklaces is exactly

  `N_even(n) = (2^(n-1) - 2^(n/2))/n`.

Consequently, for any genuinely new exact-period-`n` portal component with `E` even internal vertices, `O` odd terminal leaves, and `V=E+O`, the previously proved leaf balance `O=E+1` gives the sharper unconditional bounds

`E <= (2^(n-1) - 2^(n/2))/n`,

`O <= (2^(n-1) - 2^(n/2))/n + 1`,

and

`V <= 2(2^(n-1) - 2^(n/2))/n + 1`.

These are stronger than bounding `E` only by half of the total primitive-necklace census, although they remain exponential and do not solve the finite-support birth-budget problem.

## Proof

A binary word of odd Hamming weight at dyadic length `n` must have exact rotational period `n`.

Indeed, if it had proper period `d<n`, then `d` divides `n` and the length-`n` word would be the repetition of a length-`d` block exactly `n/d` times. Since `n` is a power of two and `d<n`, the repetition factor `n/d` is even. The total Hamming weight would therefore be even, contradiction.

Exactly half of all `2^n` binary words have odd Hamming weight, so there are `2^(n-1)` odd words, and every one is primitive. Every primitive necklace has exactly `n` distinct rotations. Therefore

`N_odd(n)=2^(n-1)/n`.

For dyadic `n`, the standard primitive-necklace count is

`N_prim(n)=(2^n-2^(n/2))/n`,

because the only square-free divisors contributing to the Möbius sum are `1` and `2`. Subtracting the odd primitive necklaces gives

`N_even(n)=N_prim(n)-N_odd(n)`

`=(2^n-2^(n/2)-2^(n-1))/n`

`=(2^(n-1)-2^(n/2))/n`.

Every continuing vertex of a full-period portal tree has even parity, so `E<=N_even(n)`. The previous exact tree identity `O=E+1` then gives the stated bounds on `O` and `V`.

## Structural interpretation

At dyadic lengths, odd parity itself is a certificate of full rotational period. Thus every terminal odd leaf in a new full-period portal component automatically lies in the primitive sector; there is no hidden proper-period odd terminal state to account for.

Conversely, the scarcer parity class among primitive necklaces is the even class, because proper-period dyadic repetitions are necessarily even. Since all internal portal-tree vertices must come from this scarcer class, the exact ambient-state obstruction is controlled by `N_even(n)`, not by the total primitive count.

For example:

- `n=4`: `N_even=1`, hence `E<=1`, `O<=2`, `V<=3`;
- `n=8`: `N_even=14`, hence `E<=14`, `O<=15`, `V<=29`;
- `n=16`: `N_even=2032`, hence `E<=2032`, `O<=2033`, `V<=4065`;
- `n=32`: `N_even=67,106,816`, hence `E<=67,106,816`, `O<=67,106,817`, `V<=134,213,633`.

(The period-32 values use `(2^31-2^16)/32 = 67,106,816`.)

## Relevance and limitation

This is a genuine tightening of the fixed-period state-space bound and an exact parity census, but it still grows exponentially with `n`. It therefore does not provide the missing theorem required by `ASTRA_HANDOFF.md`: a bound on births or terminal resources in terms of one survivor's original finite support.

The useful conceptual point for the next step is that any original-support charging rule only needs to control the even continuing vertices (equivalently, by leaf balance, the odd leaves). At dyadic period there is no additional proper-period odd sector that can absorb or obscure terminal mass.
