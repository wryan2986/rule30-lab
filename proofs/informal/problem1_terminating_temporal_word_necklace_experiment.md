# Problem 1: small terminating temporal words form a single necklace

Status: `computational-conjecture`. Continues `problem1_doubling_parent_temporal_word_reconstruction.md`.

## Question

For a cyclic binary word `c` of dyadic length `p`, iterate the exact column recurrence

    q_(i+2) = S q_i xor (q_(i+1) OR q_i),
    q_0 = 0,
    q_1 = c,

where `S` is cyclic time shift. Run 52 showed that odd-parity `c` terminates at `(0,0)` exactly when it reconstructs a finite parent eligible for a one-bit doubling (with exact parent period automatic when `c` has exact period `p`).

## Exact exhaustive computation for p <= 8

I exhaustively tested every odd-parity word for `p = 1,2,4,8`, iterating the deterministic pair state `(q_i,q_(i+1))` until either `(0,0)` was reached or a pair repeated.

Results:

| p | odd words | terminating words | termination column | terminating necklace representative |
|---|-----------|-------------------|--------------------|------------------------------------|
| 1 | 1 | 1 | 3 | `1` |
| 2 | 2 | 2 | 8 | `01` |
| 4 | 8 | 4 | 29 | `0111` |
| 8 | 128 | 8 | 400 | `00001101` |

For every tested `p`, the terminating words are **exactly all cyclic rotations of one word**. Thus the number of terminating odd words is exactly `p`, not a positive fraction of the `2^(p-1)` odd words.

Explicitly:

- `p=1`: `1`;
- `p=2`: rotations of `01`;
- `p=4`: rotations of `0111`;
- `p=8`: rotations of `00001101`.

The `p=4` and `p=8` representatives have exact temporal period `p`, so these are genuine period-`p` parents rather than repetitions of shorter words.

This is a much stronger pattern than the run-52 small-state sanity check suggested. Local parent combinatorics does **not** appear permissive: through period 8 there is only one eligible temporal necklace at each dyadic period.

## A useful parity identity

Writing `P(v)=xor_s v(s)` and using over F2

    a OR b = a xor b xor (a AND b),

parity of the column recurrence gives

    P(q_(i+2))
      = P(q_(i+1)) xor P(q_i AND q_(i+1)).

(The two copies of `P(q_i)` cancel, and cyclic shift preserves parity.)

For the doubling initial data `q_0=0`, `P(q_1)=1`, this forces

    P(q_2)=1,
    P(q_3)=0,

because `q_2=q_1=c` and `P(c AND c)=P(c)=1`.

This identity is not yet a classification theorem, but it supplies an exact scalar constraint on every subsequent reconstructed column and may be useful in proving uniqueness of the terminating necklace.

## Interpretation

The experiment changes the most promising local target. Rather than looking for a large terminating family, the evidence supports:

> **Unique-necklace conjecture.** For every dyadic `p=2^m`, the odd-parity cyclic words whose reconstruction terminates consist of exactly one rotation orbit, of size `p`.

If true, every genuine doubling parent of a given dyadic period is unique up to temporal phase. That is potentially strong enough to constrain the common-origin scan: infinitely many required doublings could not choose arbitrary protected histories; at each period they would have to realize one prescribed temporal necklace.

The rapidly increasing observed termination widths (`3,8,29,400`) may also be relevant. No claim about their growth law is justified from four data points.

## Dead ends / cautions

- Do not infer a recurrence for the representatives from the four displayed words yet; none has been proved.
- Do not use the termination-column sequence as asymptotic evidence beyond noting that it grows quickly.
- The exhaustive computation here stops at `p=8`. A naive exhaustive `p=16` scan is substantially more expensive because nonterminating pair orbits can be long; it should be implemented with memoization/basin classification rather than independently simulating every odd word.

## Next target

Compute/classify `p=16` efficiently by memoizing the functional graph on reachable pair states, and compare the resulting terminating words with lifts/decimations of the `p=8` necklace. In parallel, seek a proof that termination plus odd parity forces a unique predecessor/decimation structure from length `2p` to length `p`. A theorem of that form would inductively prove the unique-necklace conjecture and give a rigid compatibility condition for the infinitely many doubling parents required by FULL.
