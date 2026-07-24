# Period-two actual consecutive-gap-two cylinder

Status: complete all-time proof of the exact return-coordinate cylinder that
produces two consecutive gap-two returns, plus a bounded zero-initialized
actual-orbit campaign. The cylinder theorem is exact at every return. The actual
avoidance statement is finite only and does not exclude eventual center period
two or solve Rule 30 center nonperiodicity.

## 1. Return coordinates

At a `u` event the packed even-time right fringe has its first two bits zero, so
write

```text
A = 4z.
```

Let `rho(z)` be the number of two-step blocks to the next `u` event. The existing
first-return theorem gives `rho(z) in {2,3,4,5}` and determines it from `z mod
16`.

Two consecutive gap-two returns mean that the five branch letters beginning at
the current return are

```text
u t u t u.
```

## 2. Exact dependency cone

A schedule word of length five depends only on the first ten bits of `A`. Since
`A=4z`, it depends only on `z mod 256`. Exhausting those 256 assignments gives
exactly twelve witnesses:

```text
28, 44, 60, 92, 108, 124,
156, 172, 188, 220, 236, 252.
```

These are precisely the lifts modulo 256 of three classes modulo 64. Therefore,
for every return state and with no bounded-time assumption,

```text
rho(z)=2 and rho(R(z))=2
    iff z mod 64 is in {28,44,60}.                 (1)
```

Here `R` is the exact first-return map. Equation (1) is stronger than the
four-bit return selector: a single gap two only requires `z mod 16` in
`{4,8,12}`, while a second gap two selects three of the sixteen lifts modulo
64.

The proof is a complete Boolean dependency-cone proof, not an orbit sample. The
five output letters cannot depend on bits beyond the exhausted eight bits of
`z`, and the resulting truth table factors through the low six bits.

## 3. Zero-initialized actual campaign

Starting with `A_0=0`, the exact packed fringe recurrence was run for 200,000
blocks. It contains 42,854 `u` returns. Their return coordinates use only

```text
z mod 64 in {0,3,11,24,35,43,56,63}.
```

The exact counts are

```text
0:1, 3:7101, 11:21458, 24:20,
35:1, 43:14251, 56:1, 63:21.
```

None lies in the three cylinders from (1). The return-gap counts are

```text
2:21, 3:7102, 4:1, 5:35729.
```

There are no consecutive gap-two pairs in this campaign. Every observed gap-two
return starts outside the bad cylinder; the last begins at block 144.

This finite campaign is useful because the unique generic phase-minimizer
counterexample currently known uses the gap pair `(2,2)`. It shows that this
counterexample cannot occur on the tested actual prefix. It does not prove that
the actual return orbit avoids the three residue classes forever.

## 4. Remaining target

The period-two route now has a concrete actual-fringe subproblem:

> Prove that the zero-initialized return orbit never reaches
> `z mod 64 in {28,44,60}`, or replace this finite residue condition with a
> stronger actual/minimizer coupling that excludes every zero-penalty shadow.

A proof of permanent avoidance would rule out consecutive gap-two returns on the
actual schedule, but it would not by itself exclude zero two-return penalties
for other gap pairs at larger witness complexity. The universal isolated-zero
lemma is already false.

## 5. Scientific boundary

The all-time conclusion here is only the cylinder equivalence (1). The
200,000-block avoidance statement is finite exhaustive computation on the
zero-initialized orbit. No actual return penalty is proved positive at all
depths, no finite actual period-two survivor is constructed, and Rule 30 center
nonperiodicity is not solved.
