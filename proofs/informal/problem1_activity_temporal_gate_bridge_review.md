# Review disposition: temporal-code gate bridge (corrected)

Role: independent adversarial recheck of the ENTIRE corrected bridge
after the lead's fatal-flaw finding. Status of the source:
`partial-proof`, pending lead review. Problem 1 remains open. No
experiment or census run. Lead independently replays all hand
arithmetic and index identities in parallel.

Corrected source: proofs/informal/problem1_activity_temporal_gate_bridge.md,
SHA256 34b9626da27a665c0541328735ba74bb95e4ffb9c5b511d117bb60d7209786ac.

## 1. Original errors corrected

1. Boundary-index misuse (FATAL, now fixed): the original Sec 3 treated
   c_0 = 3 as mappable by the n >= 1 shift and called P_0 a
   'different kind'. Corrected: P_0 is the SAME pair-OR formula at
   n = 0 (identical to raw-symbol nonzeroness, since b_s is that low
   pair); c_0 = 3 is P_0(Fx,0) = 1 with n = 0, outside the shift
   domain, with no image under pullback.
2. Bijection ambiguity (now fixed): the scan's per-state permutation
   was overstated as a full x-to-c bijection. Corrected: exact
   bijection between tail b_{>=2} and c with c_0 = 3; F is 2-to-1 on
   the gate-cylinder union; each fixed-gate branch (b_1 = 1 or 2 from
   the actual fringe) is bijective.
3. Unsupported generality (now fixed): 'no dissipation' replaced by
   the lead's exact wording -- each fixed scan state h is a
   permutation of the input symbol; no monotone quantity proved.

## 2. Adversarial recheck of the corrected file

Sec 1 (imports): pi F = A^2, conjugacy, deletion rule, ray identity,
permitted-domain premise, fringe-supplied q -- all attributed imports,
no new derivation to break. Clean.
Sec 2: Phi(c) = shift^2(b) follows from deletion plus conjugacy;
h inversion recovers r then s, hence per-state permutation; table
rows [0,3,2,1],[1,2,3,0],[3,2,1,0],[3,2,1,0] replayed by hand and
confirmed; gate temporal reading confirmed (low4 7: Ax low pair
(0,1) = 2 for u; low4 11: (1,0) = 1 for t). 2-to-1 fiber over b_1
confirmed: c sees only b_{>=2}. Clean.
Sec 3: shift proof via Phi/shift commutation re-indexed by hand
(both orders give g(b_{t+k},b_{t+k+1}); an earlier private
mis-indexing was caught and does not appear in the file).
Counterexample x = 11 replayed in full: A(11) = 13, A^2(11) = 12,
pi(51) = 12 with low pair 3 consistent with the lead's F(11) = 51;
P_0(x,2) = 0 against P_0(Fx,0) = 1 refutes the substitution, while
P_1(F(11),0) = 0 confirms the valid n = 1 shift. The F(11) value
itself is the lead's and is replayed by the lead. Clean.
Sec 4: novelty fence uses the exact corrected wording; joint-window
arithmetic verified (W >= n gives at most 2W ages; R >= e H_n/2 ->
infinity over unbounded n). Unproved status and no-census discipline
explicit. Clean.

## 3. Exact remaining issues

1. The m-step form P_n(F^m x,t) = P_{n-m}(x,t+2m) needs F^k x on the
   permitted domain for every k < m; for actual forced orbits this
   holds by definition, otherwise it is a hypothesis. Scope note, not
   a flaw.
2. The joint-window target is unproved by design; no census admitted.
3. Source remains `partial-proof` pending lead review; this
   disposition is an independent recheck, not a second acceptance.

## Verdict

All three fatal/correction items are fixed and verified; no new flaw
found in the corrected bridge. Accepted at `partial-proof` from
this side; lead acceptance is separate.
