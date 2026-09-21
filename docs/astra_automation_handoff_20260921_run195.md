# Astra automation handoff — 2026-09-21 run 195

Problem 1 remains OPEN.

## New result

Run 194's corrected front seed was propagated one more row exactly. Let

`q = r_-4(t+4)`.

The complete beta=1 driver already fixes `(r_-3,r_-2,r_-1,r_0)(t+4)=(0,1,1,1)`. Direct Rule-30 propagation gives

`r_-1(t+7)=1 xor q`.

Using run 194's corrected discrepancy seed (`m(t+7)=0`, actual/shadow `11/00` at positions `0,1`) gives

`d_-1(t+8)=q`,
`d_0(t+8)=1`.

Hence the corrected front is exactly

- `q=1`: `m(t+8)=-1`, `J(t+8)=t+7`;
- `q=0`: `m(t+8)=0`, `J(t+8)=t+8`.

So `m(t+8)=-q`.

## Important correction status

Do not reuse the run-184--192 claims that `t+8` is a forced positive-delay center crossing or has a particular resetting/nonresetting source type. Those claims depended on the erroneous `m(t+7)=1` premise. Runs 193--195 are the active corrected continuation.

## Next target

Determine whether `q=r_-4(t+4)` is constrained by the complete-driver expression `Y_(t+4)=16 A^4 z+7`. If it is genuinely free, propagate both corrected branches to `t+9` and reconnect them to the original-cut residence/threshold identities. Prefer exact driver decoding over introducing new independent local bits.