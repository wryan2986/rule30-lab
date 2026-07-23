# Period-two terminal-zero and leading-order cocycle

Status: complete informal proof of an exact all-word nonlinear cocycle for the
period-two whole-word transducer, together with bounded exhaustive and actual-
orbit checks. This is a partial structural result. It does not prove that the
alternating inverse lift has infinite support, exclude eventual center period
two, or solve Rule 30 center nonperiodicity.

## 1. Context

Let `G_m` be the accumulated inverse word for the pure alternating temporal
trace. The established complete-word recurrence is

```text
G_(m+1) = (G_m)|_11 p q_m,   q_m in {t,u},
```

and the next spatial output pair is

```text
e_m = G_m(11) in {00,01,10,11}.
```

The alternating inverse lift has ordinary finite support exactly when `e_m=00`
for every sufficiently large `m`.

Previous work ruled out fixed-width endpoint tests and universal additive
cocycles. The present note uses a nonlinear order statistic on the complete
word. For a word `G`, define

```text
ord_t(G) = length of the maximal leading run of t letters.
```

This statistic lives at the outer word boundary, while `G(11)` is the terminal
state obtained only after scanning the complete word from the opposite end.

## 2. Exact transducer column needed for the proof

The `t` input column of the established right-to-left transducer is

| incoming pair | emitted letter | successor pair |
|---|---|---|
| `00` | `t` | `00` |
| `01` | `p` | `01` |
| `10` | `p` | `11` |
| `11` | `u` | `10` |

Thus a leading input `t` emits a leading output `t` exactly when its incoming
scan state is `00`. Once the scan reaches `00`, every additional leading `t`
keeps the state at `00` and emits another `t`.

For the first non-`t` input letter, the only transitions entering state `00`
are

```text
p with incoming state 11:  p -> t / 00,
u with incoming state 10:  u -> t / 00.
```

In both cases that boundary letter emits one new `t`.

## 3. Terminal-order theorem

Write

```text
G = t^ell K,
```

where `ell=ord_t(G)` and `K` is empty or begins with `p` or `u`. Let

```text
S = G|_11,
e = G(11).
```

### Theorem

For either branch `q in {t,u}`,

```text
ord_t(S p q) = ell+1,  if e=00,
               0,      otherwise.                 (1)
```

### Proof

Suppose first that `e=00`. The suffix `K`, scanned before the leading `t` run,
must bring the scan state to `00`. The word `K` cannot be empty: scanning a
nonempty pure power of `t` from `11` alternates within states `11` and `10` and
never reaches `00`.

The first letter of `K` is therefore the transition that enters `00`. By the
complete table it emits `t`. Every one of the `ell` leading input `t` letters is
then processed in state `00`, emits `t`, and leaves the state at `00`. Hence
`S` begins with exactly `ell+1` letters `t`.

It cannot begin with more. If the next emitted position, coming from the
second letter of `K`, were also `t`, then that transition would leave scan
state `00`: every transducer transition that emits `t` has successor `00`. The
first letter of `K` would then be a `p` or `u` processed with incoming state
`00`, and the table says it would emit `p`, not `t`. This contradicts the
extra leading `t` already identified. Appending `p q` to the right end does not
change the leading run, so `ord_t(S p q)=ell+1`.

Now suppose `e` is not `00`. If `S` began with `t`, then either the first input
letter of `G` were a leading `t` processed in state `00`, or the first input
letter were `p/u` on one of the two transitions entering `00`. In either case
the terminal scan state after the leftmost letter would be `00`, contradicting
`e!=00`. Therefore `S` does not begin with `t`, and appending `p q` cannot
create a leading `t`. Thus `ord_t(S p q)=0`. QED.

The theorem is branch-independent because the appended `q` lies at the
opposite, right end of the word.

## 4. Exact zero-run counter

Put

```text
ell_m = ord_t(G_m).
```

Applying (1) to the block recurrence gives

```text
ell_(m+1) = ell_m+1,  if e_m=00,
            0,        otherwise.                   (2)
```

Starting from the empty word `G_0`, for which `ell_0=0`, induction yields:

> `ell_m` is exactly the number of consecutive terminal pairs equal to `00`
> immediately preceding block `m`.

This is an all-word identity for every possible branch driver, not a property
inferred from the actual finite orbit.

Consequently,

```text
e_m is eventually 00
```

if and only if, from some point onward,

```text
ell_(m+1)=ell_m+1,
```

or equivalently `ell_m` diverges with unit slope. Ordinary finite support is
therefore equivalent to eventual unbroken growth of a visible outer-word
order.

This is a genuinely cross-word relation: the terminal pair at one scan
boundary exactly increments or resets a run length at the opposite boundary,
with the complete growing middle eliminated by the transducer.

## 5. What this adds and what it does not

The result supplies the first nonlinear complete-word cocycle in this route.
It is stronger than counting letters:

- the leading order is position-sensitive rather than additive;
- its increment is controlled by the terminal pair after a complete scan;
- and it turns the support question into a reset problem on the exact coupled
  fringe/word orbit.

It does not by itself prove that resets occur infinitely often. Arbitrary
branch drivers can produce long finite zero-pair runs, and the actual
zero-initialized fringe orbit also produces increasing record runs.

## 6. Bounded actual-orbit diagnostic

The accompanying analyzer runs the exact autonomous fringe recurrence

```text
A_(m+1) = (F_m << 1) XOR (F_m OR (F_m >> 1)),
F_m = (1+2A_m) XOR (((1+2A_m) >> 1) OR ((1+2A_m) >> 2)),
```

with `A_0=0`, supplies `q_m=u` exactly when `A_m=0 mod 4`, and updates the
complete word by the exact transducer.

Through block 10,000, the record consecutive-`00` run lengths are

```text
1, 2, 3, 4, 5,
```

with the length-five record at blocks 2,948 through 2,952 (zero-based). This
is bounded regression evidence only. In particular, it refutes any attempted
proof that assumes the actual zero-pair runs have a small uniform bound based
on the earlier 512-block campaign.

## 7. Remaining target

The support problem is now equivalently:

> Prove that the zero-initialized coupled fringe orbit resets `ord_t(G_m)` to
> zero infinitely often.

A useful continuation must control this order using information special to the
actual fringe orbit. Plausible next forms are:

1. a return-map rule that forces a reset after a scale-dependent fringe event;
2. a nonlocal valuation or parity detecting the first non-`t` letter of the
   transformed word;
3. a renormalized comparison between long leading-`t` episodes and the exact
   `u`-return states of the fringe.

A fixed numerical bound on zero runs is not supported by the current data.
