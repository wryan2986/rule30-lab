# Run 180: the beta=1 terminal shadow pair is rigid

Status: `partial-proof` / correction to run 179. Problem 1 remains OPEN.

## Correction

Run 179 claimed that, at the cyclic gate-u row `t+4` of a sufficiently late one-bit nonresetting passage, the terminal shadow flag

    gamma := hat u_(t+6)

remains an independent Boolean datum under `beta=1`. That claim omitted an already-proved original-cut constraint from run 173 and is false on the actual admissible passage.

The Boolean examples in run 179 only showed non-implication from `beta=1` for arbitrary four-bit tuples. They are not compatible with all previously established passage data.

## Previously established constraint at t+4

Run 173 proved for the SAME original global E shadow that

    m(t+4)=1.

Run 175 records the complete actual cyclic u-source at this row:

    G(z)=16 A^4 z+7,

hence

    (r_0,r_1,r_2,r_3)(t+4)=(1,1,1,0).

Since `m(t+4)=1`, position 0 agrees and position 1 is the first discrepancy. Because the actual position-1 cell is 1,

    hat r_1(t+4)=0.                                  (1)

Write, as in the forward shadow transport theorem,

    (a,b,c,d)=(hat r_1,hat r_2,hat r_3,hat r_4)(t+4).

Equation (1) therefore fixes

    a=0.                                             (2)

This constraint was missed in run 179.

## Beta=1 fixes the second shadow cell

At `t+4` the actual gate is u, so `u_(t+4)=1`. The cyclic-source birth law is

    beta = 1 XOR hat u_(t+4).

Thus `beta=1` implies `hat u_(t+4)=0`, i.e. the shadow right pair is not `00`. Together with `a=0`, this forces

    b=1.                                             (3)

Therefore the beta=1 branch has the exact shadow right pair

    (hat r_1,hat r_2)(t+4)=(0,1).                   (4)

No wider-right shadow datum enters (4).

## Exact two-step transport to t+6

Use the established cyclic-source two-step formulas with common shadow centers `1,0`:

    A = 1 XOR(a OR b),
    B = a XOR(b OR c),
    C = b XOR(c OR d),

and

    (hat r_1,hat r_2)(t+6)=(A OR B, A XOR(B OR C)).

Substituting `a=0,b=1` gives, for every `c,d`,

    A=0,
    B=1,
    C=1 XOR(c OR d),

so

    (hat r_1,hat r_2)(t+6)=(1,1).                   (5)

In particular

    gamma=hat u_(t+6)=0.                             (6)

Thus gamma is not an independent Boolean datum on the actual beta=1 passage: it is forced to zero.

For comparison, the actual low cells at `t+4` begin `(1,1,1,0)`. The identical two-step physical formula gives

    (r_1,r_2)(t+6)=(0,1),                            (7)

independently of the actual `r_4(t+4)`. Hence at the resetting delayed endpoint

    actual right pair = (0,1),
    shadow right pair = (1,1).                       (8)

The actual and shadow zero-pair flags agree (`0`), but the first right cell remains discrepant.

## Consequence for the continuation

Run 179's proposed state variable `gamma` should be deleted from the continuation target: its apparent freedom came from dropping the known global-front condition `m(t+4)=1`.

The beta=1 resetting endpoint is more rigid than previously stated. At `t+6` the SAME original global shadow has right pair `11`, while the actual row has right pair `01`. Any resetting -> nonresetting recombination argument should begin from this exact pair discrepancy, not from an arbitrary gamma branch.

This does not yet determine the complete shadow driver at `t+6`, nor does it prove that the later resetting -> nonresetting conversion must pass through cyclicity or a fresh delay birth. Wider cells can still affect subsequent evolution once their cones reach positions 1 and 2.

## Dependencies

* `problem1_run173_one_bit_fifth_residence_is_exactly_two.md` (`m(t+4)=1`).
* `problem1_run175_zero_birth_terminal_residence_is_one.md` (actual low cells of `G(z)`).
* `problem1_shadow_gate_birth_phase.md`, equation (9) and its full two-step formulas.
* `problem1_run179_beta_one_retains_next_shadow_gate_bit.md` (corrected here).
