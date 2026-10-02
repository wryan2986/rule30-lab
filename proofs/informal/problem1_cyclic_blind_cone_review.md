# Cyclic blind-cone lemma: verification and failed claims ledger

Status: INDEPENDENTLY CHECKED for the quotient lemmas in
`problem1_cyclic_blind_cone_bound.md`; `finite-exhaustive` for the separate
bounded record. Prize Problem 1 remains OPEN. Agreement between reviewers
is not used as a substitute for the written induction.

## 1. Accepted mathematical unit

The parent derived the zero-difference cone, the blind-visit exclusion with
`g_r=max(2,floor(r/2)+1)`, cyclic packing, parity-conditioned affine
dimension, and the divisor-sum charge. It then reconstructed the update from
two original Rule-30 rows and checked the proof from the fixed boundaries.

Independent reviewer route: `opencode-go/space-bunny-free`.
Agent `01a0fd83-9a17-7c61-8f4e-628cf434da81` reviewed the equations and
quantifiers, including cyclic wrap, arbitrary labels, non-least presentation
periods, odd spatial depths, and finite termination. Its final corrected
disposition found no mathematical gap in the cone/spacing/charge statements
at their exact scope. It was closed after integration.

Two useful clarifications from that review were incorporated: parity-free
driver reconstruction at depth `2p`, and the fact that the charge bound is
depthwise and does not require compatibility between depths. The proof
does not assume an infinite same-period tower exists.

## 2. FAILED — unrepaired closed form at p=1

The expression

    2 sum_(q=1..p) floor(p/q)-4p+floor(p/2)+1

cannot bound the nonnegative charge for ALL `p>=1`: it equals `-1` at
`p=1`. The smallest possible period is already a counterexample.

Concrete depth-one control: driver `1`, state `(X_1,Y_1)=(0,1)` is fixed
by `T_1`, has no blind phase, and has charge zero. The proposed inequality
would be `0<=-1`.

Repair accepted: define `U(1)=0` separately and use the expression only for
`p>=2`. The parent found and repaired this before receiving the independent
review. The finite verifier also compares the repaired formula to its
defining nonnegative sum for every `1<=p<=256`.

## 3. Rejected reviewer objections, with exact controls

The first reviewer report confused affine dimension with cardinality. For
the fixed period-12 depth-one orbit

    ((0,0),(1,1))^6,

the six transitions out of `(1,1)` are blind. Exactly 32 odd aligned
labelings realize this orbit. They form an affine space of dimension five,
exactly `u=k-1`; thus this example CONFIRMS the dimension theorem. Necklace
counts are a different quantity. The reviewer withdrew its objection.

The same report claimed depth-two blind density was at most `1/3`. This
is refuted by the explicit odd two-cycle

    A=(0,0,1,0) --0--> E=(1,1,1,1) --1--> A.

State E is blind and A is not, giving density `1/2`. The reviewer withdrew
that claim; it supplies the sharpness control in the final proof instead.

The parent also corrected an inconsistent sentence in the first review's
induction: the zero tail is `j>2t+2` STRICTLY, since `j=2t+2` is the
nonzero frontier. The proof note already had the strict inequality.

These controls are in the committed verifier; no rejected inference is
imported into the mathematical result.

## 4. Independent finite implementation and certificate

Verifier: `experiments/problem1_nonperiodicity/check_cyclic_blind_cone_independent.py`.
Record: `results/problem1/20261002_cyclic_blind_cone_independent.json`.

The primary implementation computes the two original row updates separately,
then converts their outputs to normalized pairs. The comparison implementation
is the existing polynomial pair recurrence. Exact domains and counts are in
the proof note and atomic JSON. Parent audited all recorded source hashes,
the payload hash, the mathematical meaning of each loop, and the reference
hash. The reference was not edited.

No all-depth claim is deduced from these finite enumerations. The proof is
the local induction followed by cyclic packing and elementary counting.

## 5. Routing and failed attempts

The parent model configuration is `gpt-6.1-sol` with reasoning effort `max`.
No Astra subagent, router policy, combo, or automatic escalation was used.
Before delegation the parent inspected the installed router: explicit
provider/model names return the specified provider route; there were no
configured blocked-model redirects, combos, or routing profiles. The
explicit provider routes fail on provider errors rather than substituting
the native provider. No global model settings were changed.

Space Bunny computational worker `01a0fd82-6610-70c0-8878-27174fcf31a9`
returned no verifier after an extended attempt and was closed. This was
not mathematical evidence.

Two cheap retries failed before doing the task:

* `deepseek/deepseek-v4-flash`, agent
  `01a0fd87-e94c-72f1-a811-cdc4ec8da3b1`: insufficient balance (402).
* `opencode-go/deepseek-flash`, agent
  `01a0fd8a-7878-7b01-9241-f96514bb2f47`: insufficient account funds (402).

Both were closed without model escalation. The parent then built and ran
the small verifier locally. A separate Space Bunny review of the prior
rank theorem was requested as agent `01a0fd80-0ab5-7511-ad5c-bc0ee089efff`;
its disposition is separate from the completed new-lemma review above.

## 6. Remaining uncertainty

The lemma bounds charge in terms of one fixed presentation period `p`.
It does not bound first zero-return depth, infer endpoint parity, control
reuse across portal restarts, bound dyadic period growth from original
support, or contradict FULL. A finite-support charge usable across those
changes remains unproved.
