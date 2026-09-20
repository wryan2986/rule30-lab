# Distinguished two-bit return forces the 011 provenance obstruction

Status: `partial-proof` / structural synthesis. Problem 1 remains OPEN.

## Setup

Keep one sufficiently late two-bit nonresetting `t` source at even time `t` in the eventual K=3 branch, and put `q=t+2`. The established nonreset-return theorem makes `Y_q` cyclic with actual gate `t`; the next even row `q+2=t+4` is cyclic with gate `u`, and the passage forces a birth at `t+6`.

Two previously separate analyses describe the same cyclic source `q`.

1. The distinguished-source FULL-trace calculation proves the exact source block

       (r_-5,...,r_2)(q) = 10101110.                 (1)

   It was originally written for the global shadow, but `Y_q` is cyclic, so actual and shadow rows coincide there.

2. The sensitive-one provenance calculation for the forced birth at `t+6` proves that, at the preceding cyclic `t` source `q`, the route reaches the neighborhood

       0 a 1  at positions (-2,-1,0),                (2)

   where `a=r_-1(q)`. If `a=0`, the neighborhood is `001` and the route reconnects to the center at `q`; if `a=1`, it is the unique `011` obstruction and the sensitive route terminates.

## Exact synthesis

Reading positions `-2,-1,0` from (1) gives

       (r_-2,r_-1,r_0)(q) = (0,1,1).                (3)

Therefore

       a = r_-1(q) = 1,                              (4)

and the `001` branch of the previous dichotomy is impossible on every distinguished two-bit nonreset return satisfying these hypotheses.

Hence every forced birth produced by this passage has the exact backward sensitive route

       center(t+4)
         <- r_-1(t+3)
         <- 011 obstruction at time t+2.             (5)

There is no direct sensitive reconnection to the earlier cyclic center at `t+2`.

The larger block in (1) also fixes the farther-left bit used in the source-fork update identity: `p=r_-3(q)=1`. Since `a=1`, that identity gives

       r_-2(q+1) = p XOR a = 0,                      (6)

consistent with the exact route calculation. Thus the obstruction is not an artifact of retaining only the three-cell neighborhood; its immediate farther-left phase is fixed as well.

## Consequence and limit

This removes one previously open provenance alternative. Repeated forced births from two-bit nonreset sources cannot evade the `011` obstruction by repeatedly taking the `001` reconnecting branch. Any finite-support birth-budget proof along this route may therefore focus exclusively on counting or aligning these source-relative `011` events.

This still does **not** prove that `011` obstructions are finite in number. Rule 30 can create `011` neighborhoods repeatedly, and the source positions move in spacetime. A global argument is still required to show bounded reuse, telescoping along a common staircase, or incompatibility of infinitely many distinguished `011` events with the fixed finite initial row.

The next useful target is therefore narrower than the run149 return-bridge proposal: compare the spacetime coordinates of the forced `011` obstruction at successive two-bit nonreset sources. Determine whether their fixed preceding block `1011` aligns on a single characteristic/staircase or whether each event can draw on a fresh farther-left ancestor. If the latter occurs at the generic cone rate, record it as a stopping fence.

Dependencies: `problem1_distinguished_011_full_trace_forces_five_cell_left_staircase.md`; `problem1_forced_birth_sensitive_route_previous_source_dichotomy.md`; `problem1_source_fork_bit_exact_update_identity.md`; `problem1_nonreset_return_birth_spacing.md`.
