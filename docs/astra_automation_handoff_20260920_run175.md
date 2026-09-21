# Astra automation handoff — run 175

Problem 1 remains OPEN.

Run 175 closes the only ambiguity left by run 174 for a sufficiently late one-bit gate-u nonresetting source.

Established prefix from runs 173–174:

    (Delta_t,...,Delta_(t+4))=(0,1,1,0,2),
    s_(t+5)=t+5.

For `beta>0`, run 174 already had `s_(t+6)=t+6+beta`. The exceptional `beta=0` case is now also exact.

Key bridge: with `q=t+2`, the established one-bit birth formula is

    beta = 1 XOR (h_3(q) OR h_4(q)).

Two direct Rule-30 steps of the SAME original global E shadow give

    h_2(t+4)=1 XOR (h_3(q) OR h_4(q))=beta.

Hence `beta=0` fixes precisely the wider driver that run 174 left unresolved: `h_2(t+4)=0`.

The actual cyclic u-source at `t+4` is `G(z)=16 A^4 z+7`, so its low cells are `(r_0,r_1,r_2,r_3)=(1,1,1,0)`. Run 173 has `m(t+4)=1`, hence the shadow has `h_1(t+4)=0` and position 0 agrees. One more Rule-30 step forces a discrepancy at position 1 on row `t+5`. Therefore `m(t+5)=1`, `J(t+5)=t+6`, and `s_(t+6)>t+5`. The zero-delay upper bound gives `s_(t+6)<=t+6`, so

    s_(t+6)=t+6,
    Delta_(t+5)=1.

Thus the full six-step itinerary is uniformly

    (0,1,1,0,2,1+beta)

for all allowed `beta>=0`, including beta zero.

Its signed ledger charge is `beta-1`. This does not solve Problem 1: beta-zero passages have charge -1, beta-one passages charge 0, and only beta>=2 is positive.

Next target: exploit the now-complete one-bit original-cut itinerary together with the already excluded two-bit nonresetting source. Revisit the late source classification and determine whether repeated sufficiently late nonresetting episodes can still have beta=0/1 indefinitely, or whether complete-core/global-shadow transport forces a positive-beta escalation or another contradiction. Avoid merely summing births; the telescope warning in `ASTRA_AUTOMATION_HANDOFF.md` still applies.

New proof note: `proofs/informal/problem1_run175_zero_birth_terminal_residence_is_one.md`.
