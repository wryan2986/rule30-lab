# Problem 1: K=3 exits impose a five-prefix spatial repair constraint

Status: exact corollary of the pushed three-bit repair identities; Problem 1 remains OPEN.

This note records a small source-restricted consequence that is easy to miss when the complete-driver and spatial-fringe descriptions are kept separate. It does not enumerate arbitrary periodic words or extend the unrestricted alternating-fiber census.

## Setup

Work on the fixed FULL orbit under an eventual physical strip `tau<=3`, at a one-bit `u,h=0` exit time `v` as in `problem1_three_bit_exit_repair.md`. Write the first five cells of the globally selected shadow at the exit as

    (hat r_0,...,hat r_4)(v)=(0,a,b,c,d).

Because this is specifically an exit, the defining condition is

    h=hat r_1(v)=a=0.                              (1)

Section 5 of the three-bit repair note proves by exact four-step transport that the necessary repair condition is

    (1 XOR a)*(1 XOR b)*(c OR d)=0.                (2)

Substituting the exit condition (1) gives the sharper source-restricted form

    (1 XOR b)*(c OR d)=0,

or equivalently

    b=1  OR  (c,d)=(0,0).                          (3)

Thus every genuine K=3 exit has shadow right quadruple

    (a,b,c,d) in {0000,0100,0101,0110,0111}.       (4)

The three patterns `0001`, `0010`, and `0011` are impossible at a repaired K=3 exit. This is not a free local-word census: `a=0` is the actual exit phase selected by the complete periodic driver, while (2) is the exact repair condition forced on the same global E shadow.

## Relation to the complete-driver restriction

The current complete-driver result simultaneously forces

    (b_0,b_1,b_2,b_3)=(2,2,2,1)

for the resetting core at every eventual-K=3 exit, and the backward phase condition rules out period four and restricts period five. Equation (3) supplies a complementary spatial constraint on the same event. A future transport theorem can therefore attack the next source from both sides: the periodic A-driver begins `2221`, while the original shadow fringe at the exit must satisfy (3).

No implication between the temporal driver symbols `b_s` and the spatial bits `b,c,d` is asserted here; the reused letter `b` in the older repair note is a spatial bit and should not be conflated with the complete-driver word. Establishing that coupling is precisely the remaining global task.

## Research consequence

The K=3 repair is not automatic once `h=0` is known. After imposing the actual exit phase, three of the eight possible remaining three-bit shadow suffixes are algebraically excluded before any further periodic-core information is used. This gives a concrete target for source-to-source transport: prove that the FULL/cyclic-source dynamics eventually forces one of those forbidden suffixes, or derive how the five allowed suffixes transform at the next negative-half-agreement source.

Dependencies: `problem1_three_bit_exit_repair.md` Section 5; `problem1_k3_exit_period_phase_restriction.md`.
