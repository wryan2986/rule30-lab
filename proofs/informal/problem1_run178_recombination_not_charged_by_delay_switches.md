# Run 178: recombination is not charged by the delay-switch ledger

Status: `partial-proof` / obstruction note. No new experiment. Problem 1 remains OPEN.

## Setup

Work in the eventual K=3 regime and take a sufficiently late one-bit gate-u nonresetting source at even physical time t. Runs 168--177 established the exact original-cut itinerary

    (Delta_t,...,Delta_(t+5)) = (0,1,1,0,2,1+beta),

where beta is the Boolean terminal birth indicator. Equivalently the hidden slack g_j=j-s_j follows

    (g_t,...,g_(t+6)) = (-1,0,0,0,1,0,-beta).

The nonreset-return theorem independently classifies the endpoint:

* beta=0: Y_(t+6) is cyclic and g_(t+6)=0;
* beta=1: Y_(t+6) has delay one, gate t, and a resetting core, while g_(t+6)=-1.

Every later nonresetting source is even and has delay one (gate u) or two (gate t), and its next even row is cyclic.

## 1. What a switch-count argument can and cannot charge

At paired even times put

    I_m = 1[tau(Y_(2m))>0].

Every nonresetting source is a 1->0 switch of I, by the existing nonresetting-core return theorem. That theorem's switch inequality already charges such returns against 0->1 births, up to endpoints and clock growth.

The run-177 terminal dichotomy does **not** create an additional switch that can be charged before the next nonresetting source.

For beta=0 this is immediate: the passage exits with I=0. A later nonresetting source has I=1, so at least one 0->1 switch must occur in between. But that is exactly the ordinary birth already counted by the existing B_m ledger. There is no second independent event.

For beta=1 the obstruction is sharper. The passage exits with I=1 already. A later nonresetting source also has I=1. Therefore the endpoint data alone do not force *any* intervening 0->1 switch. What must change is the **type of the delayed core**: the endpoint core is resetting, while the later source core is nonresetting. The Boolean delay indicator I cannot see this transition.

Thus the hoped-for statement

    every completed one-bit N passage forces a fresh delay birth before the next N passage

is false as an inference from the established endpoint classification: it is justified in the beta=0 branch, but not in the beta=1 branch.

## 2. Why the existing N/O transport does not repair the gap

The exact all-depth identity

    N_r iff O_(r+2)

marks nonresetting and constant-one core traces two physical steps apart. It does not say that a resetting delayed core must become cyclic before it can later become N. In particular, at the beta=1 endpoint we know delay one and a resetting witness, but the current theorems give no monotone quantity measuring disappearance of that witness while delay remains positive.

Consequently one cannot insert an unproved cyclic row between a beta=1 endpoint and the next N source, and one cannot charge that transition to B_m. Doing either would double-count or assume precisely the missing all-depth driver control.

## 3. Precise remaining target

The recombination problem has therefore split cleanly:

* beta=0 branch: ordinary delay-birth accounting already captures the necessary recreation of lag. Any improvement must show that this birth has an additional finite-support cost not present in the current telescope.
* beta=1 branch: the missing event is **resetting-to-nonresetting conversion at positive delay**, not delay recreation. A useful invariant must detect core type (or the complete periodic driver), not merely tau, b, s, g, or I.

This rules out extending the current switch/slack ledger as though both terminal branches paid the same new-birth cost. The next productive target is an all-depth transport law for the resetting witness/driver from a beta=1 endpoint, ideally proving that it cannot disappear while I stays 1 without consuming a separately bounded original-shadow resource.

## Dependencies

* `problem1_nonresetting_core_returns.md`, especially Sections 1--4.
* `problem1_nonreset_return_birth_spacing.md`, especially Sections 3--4.
* `problem1_run175_zero_birth_terminal_residence_is_one.md`.
* `problem1_run176_terminal_beta_is_boolean_and_cannot_escalate.md`.
* `problem1_run177_one_bit_passage_slack_reset_dichotomy.md`.
