# Round-5 sidecar: REJECTED triangular-bound proposal + two-step defect transfer

Status overview: the round-5 triangular pair-vanishing proposal is
`inconclusive` as a novelty claim and rejected as a route (lead review;
corrections accepted in Sec 2). Only the radius-2 physical formula is
`refuted`; the corrected transported statements are not new. The two-step
defect identities in Sec 3 re-express the imported boundary formulas
(`partial-proof`, lead checked); this calculation supplied no additional
restriction. No new general no-go theorem is asserted. Problem 1 remains open. No experiment was
run, proposed, or admitted. Same-file ownership only.

## 1. Rejected proposal (summary for the record)

The sidecar had proposed: for a finite-start alternating-center survivor
with leftmost one at -L, transducer pairs of X_m vanish at depths
n >= 2m + C(L). This is withdrawn as a new lemma.

## 2. Accepted corrections (lead review)

- Radius error: physical f(l,c,r) = l XOR (c OR r) has radius 1. The
  physical leftmost cell moves one step left per step (L_{t+1} = L_t - 1),
  not two. The factor of 2 belonged to the right-edge map T's bit-growth
  and was wrongly mixed into physical coordinates.
- Corrected bit bound: X_m has bit length at most L + 2m + 1. This is
  ALREADY given by the forced degree law plus the moving-cut identity.
- Corrected pair threshold m + floor(L/2) + 1 is finite support
  transported through the transducer dictionary. It adds no new content
  and admits no new first-witness evaluation.
- Non-ordinary X_0 alone does NOT exclude the mortal rational alternative:
  T^h(X_0) with h > 0 could still be finite. Finite-entry exclusion needs
  the full forward orbit, not one shift's support shape.
- Excluding a pure-trace finite seed S does NOT handle all eventual
  traces: eventual periodicity with a transient/preperiod is a strictly
  larger class than the pure alternating trace from t = 0.

## 3. Exact symbolic task: two-step defect transfer at nearest columns

Physical coordinates: x_i(t+1) = x_{i-1}(t) XOR (x_i(t) OR x_{i+1}(t)).
Assume the pure alternating center x_0(2m) = 1, x_0(2m+1) = 0. Defect
d_i(t) = x_i(t+2) XOR x_i(t), so d_0 = 0 identically. All identities below
are exact hand derivations from the update rule; no machine was used.

### 3a. Base identities (rechecked, `partial-proof`)

- (B1) x_{-1}(2m) = 1: even-to-odd center gives
  0 = x_{-1}(2m) XOR (1 OR x_1(2m)) = x_{-1}(2m) XOR 1.
- Odd companions: x_1(2m+1) = 1 XOR (x_1(2m) OR x_2(2m)) =: b_m, and
  x_{-1}(2m+1) = x_{-2}(2m) XOR 1.
- (B2) x_{-2}(2m) = b_m = NOR(x_1(2m), x_2(2m)): odd-to-even center gives
  1 = x_{-1}(2m+1) XOR x_1(2m+1), i.e. 1 = NOT x_{-2}(2m) XOR b_m.
- (B3) x_{-3}(2m) = 1 - b_m: x_{-2}(2m+1) = x_{-3}(2m) XOR (b_m OR 1)
  = NOT x_{-3}(2m), while x_{-1}(2m+2) = 1 forces x_{-2}(2m+1) = b_m.
  Further: x_{-1}(2m+1) = 1 - b_m, x_{-2}(2m+1) = b_m,
  x_{-3}(2m+1) = NOT x_{-4}(2m) (imports the deeper variable x_{-4}).

### 3b. Even- and odd-time defects (`partial-proof`)

- d_{-1}(2m) = 1 XOR 1 = 0, automatic: carries no information.
- d_{-2}(2m) = b_{m+1} XOR b_m; d_{-3}(2m) = d_{-2}(2m).
- d_{-1}(2m+1) = d_{-2}(2m+1) = b_{m+1} XOR b_m.
- d_{-3}(2m+1) = x_{-3}(2m+3) XOR x_{-3}(2m+1)
  = NOT x_{-4}(2m+2) XOR NOT x_{-4}(2m) = d_{-4}(2m): regresses leftward.
- The even-center two-step condition x_0(2m+2) = 1 is exactly
  (1 - b_m) XOR x_1(2m+1) = 1, i.e. the already-known x_1(2m+1) = b_m.

### 3c. Scoped disposition (`inconclusive`)

These nearest-column identities only transport the already-known free
branch differences b_(m+1) XOR b_m and import the next deeper column.
This particular calculation supplied no nonnegative quantity or new
whole-tail restriction. It does NOT prove that every fixed-width defect
closure or every nonnegative defect quantity is impossible. No such
universal conclusion follows from the local radius or XOR/OR formulas.
The route was set aside without admitting any new numerical campaign.

The authoritative positive round-five results are in the staircase,
transport, sparse-code, temporal-gate and joint-window notes. This memo
preserves a rejected route and its coordinate/quantifier corrections;
it is not a missing dependency of those proofs.
