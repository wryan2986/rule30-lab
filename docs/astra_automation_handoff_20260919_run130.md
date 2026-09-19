# Astra automation handoff — run 130

Problem 1 remains OPEN.

Starting branch tip: `f4d6afc1f347662abbd3320bd1069fb550b49e75` (`research/astra-next`). No intervening work was found after run129.

## New result

Run129 left the target of continuing sensitive-1 provenance from the cyclic center at `t+4` backward through the preceding cyclic `t` source at `q=t+2`.

This continuation is now exact. Gate `t` at `q` implies `r_1(q) OR r_2(q)=1`, hence `r_1(q+1)=0`. FULL centers `1,0,1` at `q,q+1,q+2` then force `r_-1(q+1)=1`, so the center at `q+2=t+4` is produced by exact neighborhood `100` and routes sensitively to that left-neighbor 1.

The neighborhood producing `r_-1(q+1)=1` has right input `r_0(q)=1`; Rule 30 forces its left input `r_-2(q)=0`. It is therefore exactly:

    001 if r_-1(q)=0,
    011 if r_-1(q)=1.

Thus the route either reconnects to the previous distinguished cyclic center at `t+2` (`001`) or terminates at the unique sensitive-1 obstruction (`011`). Recorded in `proofs/informal/problem1_forced_birth_sensitive_route_previous_source_dichotomy.md`, commit `ca7201f4780ead7714cd25872373bd93420eb13d`.

## Next target

Do not extend generic provenance farther. Focus on the single source-relative fork bit `r_-1(q)` at cyclic `t` returns produced by two-bit nonreset passages. Determine from the complete-core/code identities whether this bit is constrained across successive episodes, or whether both values can recur without consuming a finite original-row resource. A useful result must establish monotonicity/bounded reuse, or a no-go showing this fork cannot provide it.
