# Problem 1: exact autonomous half-row maps for an alternating center

Status: `partial-proof` for the biconditional reduction and inverse-branch
obstruction below. This does not exclude eventual period two or solve
Problem 1. The underlying two-step fringe and moving-cut identities already
exist in the repository; the contribution here is their explicit autonomous
phase formulation, with the complete finite halves retained.

## 1. Encoding and the question

Let `x_i(t)` be an ordinary Rule 30 configuration, with

    x_i(t+1) = x_(i-1)(t) XOR (x_i(t) OR x_(i+1)(t)).

At a time when the center is one, encode its complete left and right halves
by nonnegative integers

    L = sum_(j>=0) x_(-j) 2^j,
    R = sum_(j>=1) x_j 2^(j-1).

Thus `L` includes the center, and `R` begins at its immediate right
neighbor. Both are ordinary finite integers when the physical row has finite
support. For the next center value to be zero, its left neighbor must be
one: `x_0'=x_-1 XOR 1`. Consequently a phase of an alternating center
necessarily has `L=3 mod 4`.

The precise question is whether there are finite `L=3 mod 4`, `R>=0`
whose actual future center is `101010...`. Any eventual period-two trace of
a finite-support configuration can be rebased at a late center-one phase
to give such a pair. Conversely any such pair specifies a finite-support
initial row with an alternating center.

## 2. Two autonomous maps and the compatibility gate

Define ordinary-integer bit maps

    A(z) = (z>>2) XOR ((z>>1) OR z),
    Psi(L) = 4 A(A(L)) + 3,

    D(R) = (R<<1) XOR (R OR (R>>1)),
    F(R) = D(D(R) XOR 1),

    q(R) = 1 if R=0 mod 4, and 0 otherwise.

Call a pair admissible when

    L=7 mod 16  if q(R)=1,
    L=11 mod 16 if q(R)=0.                       (1)

All formulas use their actual complete integers. They do not replace the
right fringe by a finite observer or by an unconstrained binary schedule.

### Two-step identity

Suppose `L=3 mod 4`. Write `ell_j` for bit `j` of `L`, and `r_0,r_1`
for the first two bits of `R`. The first center output is zero, while the
first left and right neighbor outputs are

    x_-1' = 1 XOR ell_2,
    x_1'  = 1 XOR (r_0 OR r_1) = q(R).

The next center and left neighbor are therefore

    x_0''  = 1 XOR ell_2 XOR q(R),
    x_-1'' = ell_3 XOR ell_2.                    (2)

Both equal one exactly when `ell_2=q(R)` and `ell_3=1 XOR q(R)`.
Together with `ell_0=ell_1=1`, these are exactly (1).

For the remainder of the left half, the one-step identity is

    L' >> 1 = A(L),

because output site `-(j+1)` has inputs at `-(j+2),-(j+1),-j`.
Deleting a low bit commutes with `A`:

    A(z) >> 1 = A(z>>1).

It follows that `L''>>2=A(A(L))`. When (1) holds, (2) supplies the low
two bits `11`, giving `L''=Psi(L)`.

For the right half, one step with center input `c` is exactly
`D(R) XOR c`, where the XOR affects only its low bit. The two successive
center inputs are one and zero, so the right half after two steps is
`F(R)`. This identity retains every right-fringe bit.

We have proved:

> Starting from `L=3 mod 4`, the center and its left neighbor return to
> the pair `11` after two Rule 30 steps if and only if (1) holds. When it
> holds, the complete new halves are exactly `(Psi(L),F(R))`.

## 3. Exact infinite-orbit equivalence

For finite `L=3 mod 4` and `R>=0`, put

    L_m = Psi^m(L),  R_m = F^m(R).

Then the following statements are equivalent:

1. The actual future center of the encoded finite row is `101010...`.
2. The compatibility condition (1) holds for `(L_m,R_m)` for every
   integer `m>=0`.

For sufficiency, apply the two-step identity inductively. It proves that
the autonomous iterates are the actual complete halves at every even
time, and the intervening center value is zero. For necessity, an
alternating center forces its left neighbor to be one at every center-one
phase; applying (2) at each such phase gives (1), and the complete-half
identities give the autonomous iterates.

Thus period two is excluded for all finite-support configurations if and
only if every such finite pair eventually violates (1). No finite list of
successful gates establishes an infinite survivor, and no finite list of
failures proves this universal termination statement.

## 4. Bit length supplies no separation

For `z>0`, `A(z)` has exactly the same highest set-bit position as `z`:
the top bit of `(z>>1) OR z` is one and `(z>>2)` cannot cancel it.
Hence `Psi` increases the bit length of every positive input by exactly
two.

For `R>0`, `D(R)` increases bit length by one. Toggling its low bit
does not affect its highest bit, so `F` increases bit length by two.
Also `F(0)=3`, so the same increase holds at zero if its bit length is
defined as zero. Therefore

    bitlen(L_m) - bitlen(R_m)

is constant along all autonomous iterates. A contradiction based only on
the relative support widths cannot follow from these maps. This recovers
the neutral growth issue already present in the earlier first-return
formulation; it does not resolve the compatibility of the full patterns.

## 5. The right half selects information lost by the left map

There is a genuine finite collision:

    A(171)=213,  A(213)=202,
    A(199)=214,  A(214)=202,
    Psi(171)=Psi(199)=811.

But `171=11 mod16` and `199=7 mod16`, so the two predecessors need
opposite values of `q(R)`. For example, `(171,1)` and `(199,0)` each
satisfy one compatibility gate; their next right halves are respectively
`F(1)=7` and `F(0)=3`. Thus finiteness alone does not make the left
map invertible on the union of the two admissible gate branches.

The complete right map is injective on finite integers. To see this, set

    J(z) = z XOR ((z>>1) OR (z>>2)).

Its bit equation is `y_j=x_j XOR (x_(j+1) OR x_(j+2))`. Starting
above the highest nonzero bit and descending determines each `x_j`
uniquely, so `J` is a bijection of the nonnegative finite integers and
preserves positive bit length. Moreover,

    D(z)>>1 = J(z),   J(z)>>1 = J(z>>1),
    F(R)>>2 = J(J(R)).                            (3)

Consequently a true successor `R_next` determines its unique predecessor
as `J^(-2)(R_next>>2)`. For an arbitrary proposed successor, the candidate
must also pass the forward check `F(R)=R_next`; dropping the low two
bits does not assert that every integer belongs to the image.

Once `R` has been recovered, it fixes which low-four-bit branch of `L`
is allowed. The local map `A^2` is left permutive in its furthest input
bit: output bit `j` has the form

    (A^2 L)_j = ell_(j+4) XOR B(ell_j,...,ell_(j+3))

for a fixed Boolean function `B`. The coefficient of `ell_(j+4)` is
one because it occurs only in the leftmost input of the outer Rule 30
update. Given the four lowest input bits, this identity recursively
determines every next bit from the output, so there is at most one
finite predecessor in each fixed gate branch. This proves injectivity of
the full map `(Psi,F)` on admissible finite pairs, despite the displayed
collision for `Psi` alone.

Existence of a finite left predecessor is an additional support condition.
A unique recursively determined infinite bit sequence need not be an
ordinary finite integer. It has the following exact finite-state test for
one inverse passage.

Let `z=(L_next-3)/4`, assuming `L_next=3 mod4`, and let `N=bitlen(z)`.
Initialize a four-bit state `(a,b,c,d)` to the low-to-high bits of `7`
or `11`, as specified by the recovered right half. For each output bit
`y=z_j`, in order `j=0,...,N-1`, compute

    B(a,b,c,d) = (d OR c)
                 XOR ((d XOR (c OR b)) OR (c XOR (b OR a))),
    e = y XOR B(a,b,c,d),
    (a,b,c,d) <- (b,c,d,e).                       (4)

The identity in (4) is the explicit twofold Rule 30 composition, so after
`N` input bits the state is exactly
`(ell_N,ell_(N+1),ell_(N+2),ell_(N+3))` of the unique infinite inverse.
The inverse is an ordinary finite integer if and only if this terminal
state is `0000`.

Indeed, a positive finite inverse must have exactly `N` bits, because
`A^2` preserves positive bit length; its terminal state is therefore zero.
Conversely, if the state is zero, every remaining output bit is zero and
`B(0,0,0,0)=0`, so the inverse remains zero forever. The case `z=0`
is also covered: its only finite inverse under `A^2` is zero, which
neither gate seed equals, and the initial state fails the terminal test.

This is a 16-state transducer and terminal test for one specified inverse
gate. It is not a finite-state presentation of the whole diagonal map or
of the unbounded sequence of gates. For an actual finite admissible
forward orbit the test is necessarily satisfied by its actual predecessor;
it supplies no termination argument or bounded-use resource by itself.
The inverse/support analysis in `problem1_global_support_bridge_20261008.md`
relates this condition to the repository's inverse-section notation.

## 6. Remaining obligation

The exact unsolved statement is the termination of (1) for every finite
pair. The autonomous formulation removes no part of that quantifier.
Its useful features are a single fixed pair of complete-half maps, an
explicit compatibility gate, and a finite collision showing why the
right-fringe branch cannot be discarded. These do not prove termination,
an all-period theorem, or the original-support excess target.
