# Run 175: zero birth still forces a unit terminal residence

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

For every sufficiently late one-bit gate-u nonresetting source at even physical time `t`, runs 173–174 give

    (Delta_t,...,Delta_(t+4)) = (0,1,1,0,2),
    s_(t+5)=t+5.

If the terminal birth parameter `beta>0`, the threshold identity already gives

    s_(t+6)=t+6+beta,
    Delta_(t+5)=1+beta.

For `beta=0`, run 174 left only

    s_(t+6) in {t+5,t+6},
    Delta_(t+5) in {0,1}.

The missing input was the original global-shadow position-2 driver at row `t+4`.

## Beta fixes that driver

Put `q=t+2`. The established nonreset-return theorem gives, in the one-bit case `u=1`,

    (h_0,h_1,h_2)(q)=(1,1,1),

and writing

    a=h_3(q), b=h_4(q),

its birth formula reduces to

    beta = 1 XOR (a OR b).

Thus `beta=0` is exactly

    a OR b = 1.                                      (1)

Propagate the SAME original global E shadow two Rule-30 steps from `q` to `t+4`. From the row fragment

    (h_0,h_1,h_2,h_3,h_4)(q)=(1,1,1,a,b),

the first step at positions 1,2,3 is

    (0,0, 1 XOR (a OR b)).

Therefore the second step at position 2 is

    h_2(t+4)
      = 0 XOR (0 OR (1 XOR (a OR b)))
      = 1 XOR (a OR b).

By (1), in the zero-birth case

    h_2(t+4)=0.                                      (2)

This is the wider original-shadow driver that run 174 correctly refused to guess.

## The actual position 2 is one

The same established nonreset-return theorem gives the complete cyclic u-source at `t+4` as

    G(z)=16 A^4 z + 7.

Hence its actual low bits are rigid:

    (r_0,r_1,r_2,r_3)(t+4)=(1,1,1,0).

In particular

    r_1(t+4)=1,
    r_2(t+4)=1.                                      (3)

Run 173 already proved

    m(t+4)=1,

so position 0 agrees between actual and the same original global shadow. Since position 1 is a discrepancy and (3) has `r_1=1`, necessarily

    h_1(t+4)=0.

Let the common position-0 value be `d`. In fact (3) gives `d=1`, but its value is irrelevant below.

## Position 1 remains discrepant at t+5

Using (2)–(3), one more Rule-30 step gives

    r_1(t+5)=d XOR (1 OR 1)=d XOR 1,

while

    h_1(t+5)=d XOR (0 OR 0)=d.

Thus position 1 is unconditionally a discrepancy at physical row `t+5` in the `beta=0` case.

Since `s_(t+5)=t+5`, the global-front identity implies the next active characteristic cannot lie left of position 1. The explicit discrepancy makes it exact:

    m(t+5)=1,
    J(t+5)=t+6.

Therefore

    s_(t+6)>t+5.

But `beta=0` means `tau(Y_(t+6))=0`, so the threshold identity gives

    s_(t+6)<=t+6.

Integrality forces

    s_(t+6)=t+6,
    Delta_(t+5)=1.

## Consequence

The terminal ambiguity from run 174 is closed. The full six-step original-cut itinerary of a sufficiently late one-bit gate-u nonresetting source is

    (0,1,1,0,2,1+beta)

for every allowed `beta>=0`; at `beta=0` this reads `(0,1,1,0,2,1)`.

Equivalently,

    s_(t+6)=t+6+beta

holds uniformly, including the previously exceptional zero-birth case.

The signed six-increment ledger charge is therefore

    sum(Delta_j-1, j=t,...,t+5) = beta-1,

consistent with endpoint excess: `s_(t+6)-(t+6)=beta` and `s_t-t=1`.

This does not solve Problem 1. In particular `beta=0` passages still have charge `-1`, `beta=1` passages charge `0`, and only `beta>=2` gives positive charge. The useful new fact is that there is no hidden extra skip at the terminal zero-birth row: the original cut visits characteristic `t+6` for exactly one step.

Dependencies: `problem1_run173_one_bit_fifth_residence_is_exactly_two.md`; `problem1_run174_terminal_one_bit_cut_dichotomy.md`; `problem1_nonreset_return_birth_spacing.md`; `problem1_global_discrepancy_front.md`.
