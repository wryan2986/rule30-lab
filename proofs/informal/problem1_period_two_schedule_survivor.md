# Period-two schedule survivor and mismatch cocycle

Status: complete informal proof of an exact all-width support/schedule reduction,
plus bounded regression checks. This is a partial structural result. It does not
exclude eventual period two and does not solve Rule 30 center nonperiodicity.

## 1. Context

For the pure alternating temporal trace, the accumulated inverse word at block
`m` has the exact update

```text
H_(m+1) = (H_m)|_11 p q_m,
```

where `q_m` is `u` when the moving-fringe schedule head is `T`, and is `t`
when that head is `P` or `U`. If `H_m=t^ell K_m`, removing the leading `t`
run does not change the preimage of zero because `t(0)=0`. Define

```text
x_m = K_m^(-1)(0) = H_m^(-1)(0).
```

The preceding renewal reduction proves that the emitted base-4 block is zero
exactly when

```text
x_m = 3 mod 4.
```

On such a block the normalized integer recurrence is

```text
x_(m+1) = Q_m(P((x_m-3)/4)),
```

where `P,Q_m` are the forward maps inverse to the lowercase letters `p,q_m`.
Another zero is possible only in the two exact branch cylinders

```text
q_m=u  and x_m=7  mod 16,
q_m=t  and x_m=11 mod 16.
```

The goal here is to couple this integer recurrence to the complete *future*
moving-fringe schedule rather than study either object alone.

## 2. Inverse zero-branch contractions

Let lowercase `t,p,u` denote the inverse tree automorphisms of the forward maps
`T,P,U`. For `q in {t,u}`, define on the 2-adic integers

```text
B_q(y) = 4 p(q(y)) + 3.
```

This is the exact inverse of one zero-emitting normalized step with branch `q`:

```text
F_q(x) = Q(P((x-3)/4)),
F_q(B_q(y)) = y.
```

The tree automorphisms `p` and `q` are 2-adic isometries. Therefore

```text
v_2(B_q(a)-B_q(b)) = v_2(a-b)+2.                 (1)
```

Thus every `B_q` is a strict 2-adic contraction by a factor of `4`.
When the successor is itself zero-emitting, `y=3 mod 4`, it also lands in
the correct branch cylinder:

```text
y=3 mod 4  implies  B_u(y)=7  mod 16,
y=3 mod 4  implies  B_t(y)=11 mod 16.              (2)
```

Equation (2) can be checked from the first two levels of the inverse generator
recursions, or equivalently from the exact modulo-16 continuation table.

## 3. Unique survivor for a future schedule

Fix any infinite future schedule

```text
q_m, q_(m+1), q_(m+2), ... ,   q_j in {t,u}.
```

For an arbitrary 2-adic terminal value `z`, form

```text
X_m^(n)(z)
  = B_(q_m) B_(q_(m+1)) ... B_(q_(m+n-1))(z).
```

By repeated use of (1), changing `z` changes `X_m^(n)(z)` only at bit
positions `2n` and above. Hence the sequence converges in `Z_2`, independently
of `z`, to a unique limit

```text
X_m = lim_(n->infinity) X_m^(n)(z).              (3)
```

The limits satisfy the exact cocycle relation

```text
X_m = B_(q_m)(X_(m+1)).                           (4)
```

By (2), `X_m` is in the zero-emitting cylinder and in the unique branch
cylinder required by `q_m`. Applying the forward recurrence to (4) gives
`X_(m+1)`. Therefore `X_m` emits zero forever while following exactly the
prescribed future schedule.

Conversely, any 2-adic state that emits zero forever under that schedule must
lie in the same nested cylinders for every `n`; equation (1) makes their
diameters tend to zero. It must equal `X_m`. We call `X_m` the
**schedule-survivor state**.

This is a uniqueness theorem, not an existence theorem for an ordinary finite
integer. The earlier `1/3` and `5/3` examples are schedule survivors for the
constant `t` and constant `u` schedules, respectively, but have infinite
2-adic support.

## 4. Identification with the alternating inverse lift

Let

```text
S = Delta^(-1)(-1/3)
```

be the unique 2-adic spatial seed whose growing diagonal is the pure
alternating temporal trace. Let `T` be the right-edge moving-frame map from the
whole-tail formulation. At even time `2m`, discard the first `2m` low spatial
bits and write the remaining moving tail as

```text
Y_m = floor(T^(2m)(S) / 2^(2m))
```

in the compatible finite-quotient sense.

The alternating diagonal fixes the two low temporal bits consumed in the next
block. The same section calculation that gives the normalized zero recurrence
gives

```text
Y_m = B_(q_m)(Y_(m+1)).                           (5)
```

The branch `q_m` is exactly the one read from the moving-fringe pair of the
same orbit. Thus `(Y_m)` follows the complete actual future schedule and emits
zero in the normalized recurrence forever. By uniqueness of the schedule
survivor,

```text
Y_m = X_m for every m.                            (6)
```

In particular,

```text
X_0 = S.                                          (7)
```

Therefore the output-pair transducer below is not merely an auxiliary
construction: at shift zero it generates the binary digits of the actual
alternating inverse lift. Proving that its output is not eventually `00` is
exactly proving that the alternating inverse lift has infinite spatial support.

## 5. Exact mismatch valuation law

Let `x_m` be any ordinary normalized state paired with the same future schedule,
and let

```text
r_m = v_2(x_m-X_m),
```

with `r_m=infinity` if the states are equal in `Z_2`.

Because every `X_m` is `3 mod 4`, the current emitted block is zero exactly
when `r_m>=2`.

If `r_m>=4`, then `x_m` and `X_m` agree modulo `16`, so they use the same
schedule branch. The forward maps `P` and `Q_m` are 2-adic isometries and the
division by four removes exactly two agreement bits. Consequently

```text
r_(m+1) = r_m-2.                                  (8)
```

If `r_m` is `2` or `3`, the current block is zero, but `x_m` does not lie in
the modulo-16 branch cylinder of `X_m`. After the scheduled step the successor
is not `3 mod 4`, so the next block is nonzero.

It follows immediately that the exact number `L_m` of consecutive zero blocks
starting at `m` is

```text
L_m = floor(r_m/2),                               (9)
```

when `x_m != X_m`. If `x_m=X_m`, then `L_m` is infinite.

Equation (9) is the desired support/schedule cocycle. It converts a finite zero
run into an exact 2-adic common-prefix length and gives the infinite statement

```text
there is a final zero tail starting at m
iff x_m = X_m in Z_2.                            (10)
```

Since every actual `x_m` is an ordinary nonnegative integer, period two will be
excluded if one proves that every schedule survivor `X_m` generated by the
actual moving-fringe schedule has infinitely many nonzero binary digits.

## 6. Exact output-pair transducer

The support question in (10) has a direct word-transducer form. In low-to-high
binary notation, equation (3) begins

```text
X_m = 11 || p q_m(X_(m+1)),
```

where `||` denotes concatenation of bit streams and `11` is the forced low
pair.

Set

```text
G_0 = p q_m.
```

For `j>=0`, feed the literal input pair `11` through `G_j`. Let

```text
(a_j,b_j) = G_j(11),
S_j       = (G_j)|_11.
```

Then update

```text
G_(j+1) = S_j p q_(m+j+1).                       (11)
```

The low-to-high binary pairs of `X_m` are exactly

```text
11, (a_0,b_0), (a_1,b_1), ... .                  (12)
```

This follows by substituting the nested expression for `X_(m+1)`: `G_j` acts
on the next forced pair `11`, and its section after that input acts on the
remaining deeper tail. Equation (11) is just the composition rule for sections.

An element of `Z_2` is an ordinary nonnegative integer exactly when its binary
expansion is eventually zero. Therefore

```text
X_m is an ordinary integer
iff the pair stream in (12) is eventually 00.      (13)
```

Equations (11)-(13) replace the vague request for a “support-sensitive
invariant” with a concrete coupled transducer problem. The branch input is the
actual autonomous moving-fringe schedule, and the accepting obstruction is an
eventually-all-zero output pair stream.

## 7. Finite regression campaign

The accompanying analyzer independently implements:

- triangular inversion of `T`, `P`, and `U` modulo powers of two;
- backward contractions `B_t` and `B_u`;
- the exact moving-fringe schedule;
- accumulated inverse words and ordinary normalized states;
- the survivor output-pair transducer.

At the default limits it checks the actual path through block 512 using
128-bit survivor residues. For every checked block it verifies (9). The largest
observed zero run is three blocks and the largest mismatch valuation is seven.
It also emits the first 128 survivor bit pairs and checks them against direct
backward contraction modulo `2^256`.

These checks are regression evidence only. Seeing nonzero output pairs in a
finite prefix does not prove that the pair stream is not eventually zero.

## 8. Remaining target

The period-two route is now reduced to either of the following equivalent
support statements for the actual moving-fringe branch sequence:

1. For every block shift `m`, the schedule survivor `X_m` is not a nonnegative
   ordinary integer.
2. For every shift, the output-pair transducer (11) emits a nonzero pair
   infinitely often.
3. No actual ordinary state `x_m` equals its future schedule survivor in `Z_2`.

The next admitted work is to seek a finite closure, cocycle, or forbidden cycle
for the *coupled* system consisting of the moving-fringe generator and the word
state `G_j`. A fixed-depth portrait or a longer pair prefix is not a substitute
for such a closure theorem.
