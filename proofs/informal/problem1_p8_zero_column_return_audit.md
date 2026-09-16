# Problem 1: exact p=8 zero-column return audit

## Purpose

Run 66 reduced reverse-necklace branching to the singular states where the middle reconstruction column is zero. This note performs the proposed exact audit on the known terminating period-8 reconstruction.

## Convention and trajectory

Use

\[
q_{i+2}=S q_i\oplus(q_{i+1}\lor q_i)
\]

with cyclic temporal shift `S`. Under the coordinate convention used by the direct recurrence script, a phase/orientation representative of the known period-8 terminating initial word is

`c8 = 10110000`.

Starting from `(q0,q1)=(0,c8)`, direct exact bit propagation reaches the first terminal zero pair at `q400=q401=0`, agreeing with the previously recorded termination width `N_8=400`.

The nonterminal zero columns on this trajectory are exactly:

- `q371 = 0`, with following target `q372 = 01110111`;
- `q392 = 0`, with following target `q393 = 01010101`;
- `q397 = 0`, with following target `q398 = 11111111`;
- `q400 = 0`, followed by the terminal `q401 = 0`.

Thus there are only three nonterminal singular reverse-integration targets to audit on the entire p=8 terminating orbit.

## Phase-equivalence criterion

Run 66 proved: for an even-parity target `w`, the two solutions of

\[
Sx\oplus x=w
\]

are phase-equivalent iff `w` has a rotational period `k` such that the corresponding length-`k` repeating block has odd XOR parity.

Each p=8 target passes:

1. `01110111 = (0111)^2`. It has rotational period 4, and `0111` has XOR parity 1.
2. `01010101 = (01)^4`. It has rotational period 2, and `01` has XOR parity 1.
3. `11111111 = (1)^8`. It has rotational period 1, and `1` has XOR parity 1.

Therefore at every nonterminal zero-column singularity on the p=8 terminating trajectory, the two derivative integrations are one temporal necklace modulo rotation.

## Conclusion

**Exact p=8 result.** The known period-8 terminating reconstruction has no genuine reverse necklace branching anywhere along its full 400-column trajectory. Away from zero columns, the predecessor is exactly unique by the reverse-predecessor classification. At each of the three nonterminal zero columns, the two algebraic predecessors are phase-equivalent by the odd-parity rotational-block criterion.

Consequently the complete reverse path from the terminal pair back through this known p=8 trajectory is unique modulo temporal rotation.

This is stronger than checking only the scale-transition singularity: it audits every possible branching location on the full p=8 connector.

## Reproducibility

The audit uses direct integer/bit recurrence only. At each step compute `q[i+2] = S(q[i]) XOR (q[i+1] OR q[i])`, record indices with `q[i]=0`, and stop at the first consecutive zero pair. No search over predecessor words is required.

## Remaining gap

This is a finite exact verification, not an all-scale proof. The structural target is now to prove that every nonterminal zero-column target on a terminating dyadic orbit has an odd-parity primitive rotational block (or, more generally, satisfies the run-66 phase-equivalence criterion). Such a theorem, combined with exact predecessor uniqueness off zero columns, would eliminate genuine reverse necklace branching at every scale.