# Problem 1: the five-prefix K=3 exit constraint is not a closed return state

Status: research stopping fence; Problem 1 remains OPEN.

The source-restricted repair corollary in `problem1_k3_exit_spatial_repair_constraint.md` leaves five possible shadow prefixes at an eventual-K=3 one-bit `u,h=0` exit:

    (a,b,c,d) in {0000,0100,0101,0110,0111}.

It is tempting to regard these five prefixes as a finite state space and compute a source-to-source transition graph. The pushed exact repair theorem shows that this is not yet justified.

At the repaired endpoint `v+6`, that theorem writes

    h = hat r_1(v+4),
    k = hat r_2(v+4),
    e = d_0(v+6) = 1 XOR k.

The four-step calculation from the exit prefix determines only

    h = (1 XOR a)(1 XOR b)(c OR d).

The repair condition sets `h=0`, which is exactly what produced the five-prefix restriction. But the endpoint type still depends on the additional datum `k`. In particular:

    k=0  => e=1, so the repaired endpoint is another center-only discrepancy;
    k=1  => e=0, so the repaired endpoint is cyclic.

No pushed identity expresses `k` as a function of the four exit bits `(a,b,c,d)`. The exact repair note explicitly warns that its center inputs cannot simply be reused at a later source and that the needed correlation belongs to the global E shadow.

Therefore the five allowed prefixes are a necessary spatial filter, not a Markov state. A transition graph on those five labels alone would silently choose or forget the datum that decides whether the passage ends cyclic or noncyclic, and so could create spurious FULL returns.

This also identifies the minimum information the next source-to-source theorem must transport. It must retain enough of the global shadow / complete periodic core to determine `k=hat r_2(v+4)` (and then the phase at the next negative-half-agreement source). Equivalently, the next useful state must strictly refine the five-prefix label by a phase/core datum; merely enumerating the five prefixes cannot close the K=3 argument.

This is consistent with the repository warning that the round-309 complete-core / phase-transport drafts were never pushed. Until their missing coupling is rederived from inspectable results, the safe frontier is: temporal core prefix `2221`, period/phase restrictions, five-prefix spatial repair filter, plus an unresolved endpoint bit `k`.

Dependencies: `problem1_three_bit_exit_repair.md`, `problem1_k3_exit_spatial_repair_constraint.md`, `problem1_k3_exit_period_phase_restriction.md`, `ASTRA_AUTOMATION_HANDOFF.md`.
