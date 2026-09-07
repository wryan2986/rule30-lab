# The sharp width-minus-one delay bound is false

Status: `refuted` for(W) below; `finite-exhaustive` for the declared finite
falsification test. The physical-time implication is `partial-proof` and
conditional on the bound that was tested. External review remains missing.
Problem1 is OPEN.

The frozen PRE-RUN admission is
`problem1_width_delay_bound_test.md`; its pending status records the state
before execution, and this file supplies the outcome. No larger intercept
or growth profile was tested after the failure.

## 1. Exact failed claim and certificate

The tested statement was

    (W)  tau(y)<=bitlen(y)-1 for every finite y>0.

The counterexample is y=144, with width8 and least delay8. Its entire
closed orbit, in order, is

    144 ->252 ->193 ->209 ->205 ->220 ->201 ->223
        ->200 ->222 ->200.                          (1)

The first eight rows are distinct and outside the final two-cycle200/222.
Consequently tau(144)=8 and p(144)=2. Since8 is divisible by2, its
phase-correct representative is200, not222. Thus8>8-1 refutes(W).

For a separate hand arithmetic check of the newly exposed prefix, use
A(y)=(y>>2) XOR ((y>>1) OR y):

| y | y>>2 | (y>>1) OR y | A(y) |
| --- | --- | --- | --- |
| 144 | 36 | 216 | 252 |
| 252 | 63 | 254 | 193 |
| 193 | 48 | 225 | 209 |
| 209 | 52 | 249 | 205 |
| 205 | 51 | 239 | 220 |

The remaining suffix is already a closed hand certificate in the
full-driver phase-memory note. No assertion about a larger family is
inferred from this one transient.

## 2. What this changes at the physical-time bottleneck

For one finite row with original left extent L and its complete actual
finite right fringe, the bridge Y_t=A^t L_t gives

    tau(Y_t)=max(tau(L_t)-t,0), bitlen(L_t)=L+t.

Therefore(W), had it been true, would have given tau(Y_t)<=L-1 at all
applicable times. The exact counterexample even has the required zero
extension form144=2^4*9. For the original finite seed9 with zero right
half, L=4 and its physical time-four row is

    Y_4=A^4(144)=205, tau(Y_4)=4>L-1=3.             (2)

This follows from the SAME closed certificate(1); no new physical prefix
was searched. This orbit is not FULL: its initial center and next center
are both1, since the initial left neighbor of the center is0.

Neither(1) nor(2) refutes an EVENTUAL bounded delay on this orbit or on a
FULL orbit. In particular it does not refute a universal bound of the
different form tau(y)<=bitlen(y)+C for some finite C, or a bound tailored
to one complete original fringe. No such C is fitted or claimed.
An all-depth unbounded-excess family would be needed to close that
broader width-plus-constant route; none is established here.

## 3. Finite verification and stopping fence

`experiments/problem1_nonperiodicity/check_round305_width_delay.py` examined
positive inputs in increasing numeric order, with a predeclared maximum4095
and immediate stopping at the first violation. It stopped at144; no
larger input was examined. For each input, separate packed and Boolean-cell
recurrences, with different repeat-detection implementations, agreed on the
entire orbit, least onset, least period and phase-correct core. The frozen
width-three hand edges were checked first.

Atomic record: `results/problem1/20260907_round305_width_delay.json`.
It gives the checked interval1..144, full witness, ordered transcript hash,
software/hardware, full Git/source hashes, runtime, and cap disposition.
The30-second/128MiB caps passed. Status `finite-exhaustive` applies to that
finite interval and certificate; `refuted` applies to precisely(W).

This is not a shift-tower sample or a source/clock census. In particular
do not continue with larger144 shifts, a larger source interval, or a fitted
intercept. The exact counterexample is the stopping point for this test.
