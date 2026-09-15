# Cross-doubling budget target after the dyadic-period audit

Status: route audit / precise target. Problem 1 remains open.

## Context

The common-origin scan machinery already gives, on the same fixed FULL realization, periods tending to infinity with transitions `p -> p` or `p -> 2p`. Hence there are infinitely many genuine doubling passages. Run 41's theorem that all finite A-cycle periods are powers of two is consistent with, but does not strengthen, that transition structure.

The question left by run 42 was whether successive doublings can be charged to a finite-entry resource on the same original realization.

## 1. A naive charge to entry events cannot be the missing argument

The reviewed joint-window note gives the quantitative bounded-activity contrapositive. If `R(x) <= K`, put

    h = h_V(K),  g = g(K).

Then `z=A^h x` is finite, `bitlen(z) <= 4g+2`, and for

    J_n(x) = sum_(t=0..n-1) [bit_(2n)(A^t x) OR bit_(2n+1)(A^t x)]

one has

    sup_n J_n(x) <= max(h,2g).                         (1)

In particular, after age h all sufficiently deep boundary pairs are identically zero. Thus a proof which assigns each late doubling to a *new* finite-entry/birth event cannot work unless it first proves that the doubling has an ancestor before this cutoff. The existing late-source-diagonal theorem does not provide such an anchored ancestor; it locates the doubling source late, not inside the original window `0 <= t < n` used by `J_n`.

This is the precise failure of the simplest cross-doubling charging idea. Infinitely many doubling passages are already compatible with there being no new deep entry events after a fixed age. Any successful charge must therefore be to a persistent common-origin object, or must pull a late source back to a distinct anchored event by an additional theorem.

## 2. The useful reformulation

Equation (1) makes the required bridge exact. To contradict bounded activity it is enough to prove, for the one fixed FULL realization,

    sup_n J_n(x) = infinity.                           (2)

Therefore a cross-doubling theorem need not attach a numerical cost directly to period size. It is sufficient to construct from infinitely many doubling passages a family of pairwise distinct anchored events

    (n,t),  0 <= t < n,

with

    bit_(2n)(A^t x) OR bit_(2n+1)(A^t x) = 1,         (3)

and with unbounded multiplicity in the `J_n` windows (or otherwise force unbounded `J_n`).

A merely injective assignment of doublings to different depths n is NOT enough: it would only prove `J_n >= 1` along infinitely many n, whereas (1) allows that. The bridge must force many anchored events into at least some single depth-window, or use the stronger transport inequality to accumulate them in a joint window.

This multiplicity point is important: "one birth per doubling" is structurally too weak even if such a pullback exists.

## 3. What the next lemma must actually say

A useful next lemma should have one of the following forms.

### A. Anchored multiplicity

For a doubling chain `p,2p,...,2^r p` on one common-origin realization, prove that some depth `n=n(r)` satisfies

    J_n(x) >= f(r),

where `f(r) -> infinity`.

Combined with infinitely many doublings and (1), this immediately contradicts bounded activity.

### B. Joint-window accumulation

Associate r distinct doubling passages to boundary occurrences counted by one transport window `C_n(a,W)`, with the pullback performed on the original x rather than on successive forced states. Then use the already proved transport inequality

    sum_(s=a+2..a+W+n) V_s(x) >= C_n(a,W) H_n.

This avoids needing every event to land in the anchored `J_n`, but still requires a common window and non-reuse.

### C. Persistent-resource monotonicity

Find a common-origin label transported between consecutive doublings which cannot be recreated after consumption. This would bypass `J_n`, but the label must belong to the original realization; local source preperiod, period size, and source spacing have already been shown insufficient.

## 4. Dead end to avoid

Do not pursue either of these statements without extra structure:

1. `infinitely many doublings => infinitely many distinct entry events`;
2. `one anchored event at a new depth for each doubling => unbounded activity`.

The first lacks the needed pullback theorem, and the second does not imply unbounded `J_n` or the reviewed transport criterion.

## 5. Current bottleneck

The highest-value target is now a **many-to-one-depth pullback theorem**: show that a long chain of late doubling sources on one FULL common-origin realization forces increasing multiplicity in an anchored boundary window of the original x. This is stronger than source existence and weaker than trying to invent a globally monotone period-dependent energy.

No claim of such a theorem is made here. The contribution of this note is to reduce the cross-doubling budget idea to the exact multiplicity statement needed by the already reviewed finite-entry machinery, and to rule out the weaker injective-charging formulations.