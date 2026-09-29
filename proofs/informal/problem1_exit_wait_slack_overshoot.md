# Problem 1: exit waiting is an exact unbounded-slack mechanism

Status: exact consequence of pushed identities / route reduction; Problem 1 remains OPEN.

This note combines `problem1_exit_wait_front_residence.md` with the signed hidden-slack coordinate

    g_j = j-s_j,

used in `problem1_hidden_slack_tail_identity.md` and `problem1_forced_birth_slack_reset.md`. The preceding note showed that the forced terminal birth after a two-bit nonreset source only resets hidden slack to `g=-1`, independent of the accumulated zero-delay slack. Here the general one-bit exit gives the complementary fact: its complete-driver waiting time is an exact mechanism for arbitrarily deep negative slack.

## Exact calculation

At an even one-bit exit time `v` of the `u,h=0` type, `problem1_exit_wait_front_residence.md` proves that if

    L = min{n>=1 : b_n in {1,3}},

for the resetting complete driver `b`, then

    (tau(Y_v), tau(Y_(v+1)), tau(Y_(v+2))) = (1,L,L-1)

and, in original-cut thresholds,

    s_v = v+1,
    s_(v+1) = s_(v+2) = v+L+1.

Therefore the signed slack is exactly

    g_v     = -1,
    g_(v+1) = -L,
    g_(v+2) = 1-L.                                  (1)

So the first physical step of this exit passage performs

    -1  -->  -L,                                    (2)

an overshoot of `L-1` units. The next step recovers one unit without changing the threshold.

Equivalently the threshold increments are

    Delta_v     = L,
    Delta_(v+1) = 0,

which agrees with `g_(j+1)-g_j=1-Delta_j`.

## Immediate reduction

If the complete-driver exit waits `L` are unbounded along the actual FULL/cyclic-source orbit, then (1) immediately gives

    liminf_j g_j = -infinity,

and hence, by the shift-tail identity,

    limsup_n e_v(n) = +infinity.

Thus unbounded exit waits would finish the scalar asymptotic target directly; no accumulation of local birth credits is needed.

Conversely, any hypothetical bounded-delay survivor necessarily has bounded exit waits. Indeed the pushed exit theorem already gives `L<=K` under an eventual physical strip `tau<=K`. Therefore a proof by contradiction inside a fixed strip cannot obtain unbounded overshoot merely by repeating the same exit type: it must instead show that the FULL dynamics eventually force an exit whose complete-driver reset distance exceeds the strip, or obtain growing delay from another passage.

## Contrast with the forced birth reset

The two currently isolated local mechanisms have sharply different slack effects:

1. two-bit nonreset return followed by its forced birth: `q -> -1`, erasing local history with fixed overshoot one;
2. one-bit `u,h=0` exit: `-1 -> -L`, with overshoot controlled exactly by the complete-driver reset distance `L`.

Hence the complete-driver waiting time `L` is presently the only pushed local scalar parameter in these passages that can itself carry arbitrarily large negative slack. This does not prove that `L` is unbounded; periodic cores can have finite reset distances, and no global recurrence for successive complete drivers is currently proved.

## Research consequence / stopping fence

Do not try to accumulate the fixed `g=-1` forced-birth resets as independent gain. A more proof-relevant target is:

> Show that an infinite admissible FULL/cyclic-source continuation cannot keep all `u,h=0` complete-driver reset distances `L` bounded while also keeping every other physical delay bounded.

In an eventual `K=3` contradiction this specializes further: every such exit has `L=3` and code prefix `(2,2,2,1)`, as already proved in `problem1_exit_wait_front_residence.md`. Therefore the remaining K=3 problem is not numerical slack accounting; it is incompatibility or forced phase transport of these rigid complete-core words with the intervening nonreset/cyclic-source passages.

This note adds no new experiment and claims no recurrence between distinct exits. It only identifies exactly where an unbounded slack excursion can already occur in the pushed complete-driver machinery and separates that mechanism from the fixed-depth birth reset.
