# Automation handoff supplement — hidden-slack causal bound

Continue on `research/astra-next`. Problem 1 remains OPEN.

Read `ASTRA_AUTOMATION_HANDOFF.md` first, then `proofs/informal/problem1_hidden_slack_causal_bound.md` from this run.

## New exact result

For the fixed ORIGINAL finite actual row with right support ending at `R`, original-cut delay `s_j=tau(L_j)`, and any VISITED characteristic `j` (`s_j>s_(j-1)`), the global-front theorem gives the final erasing cell

    r_(j-s_j)(s_j-1)=1.

Finite radius-one propagation from the original support gives

    j-s_j <= R+s_j-1,

hence

    2s_j >= j-R+1.

In the shift tail `j=R+n`, with `h_n=tau(2^n v)`, this becomes

    h_n>h_(n-1)  =>  2h_n>=n+1.

Thus every genuine rise of the zero-extension preperiod reaches at least half the extension depth. Since `h_n->infinity`, this occurs infinitely often.

For a maximal block of `k` skips beginning at tower index `n`, with constant inherited preperiod `H=h_n` and exit residence `d=delta_(n+k)>0`,

    d >= ceil((n+k+2)/2)-H.

The signed charge of the block plus exit is therefore only bounded by

    B=d-k-1 >= ceil((n+k+2)/2)-H-k-1,

which need not be positive. Do NOT claim skip-block compensation from this bound alone.

## Geometric interpretation

At a visited zero-delay characteristic, hidden slack

    g_j=j-s_j

is exactly one less than the final rightward position of the global discrepancy front before its erasure:

    m(s_j-1)=g_j+1.

The causal bound is therefore a genuine one-spacetime restriction, not only ledger algebra.

## Remaining loophole / preferred target

Skipped characteristics have no residence and therefore no final erasing cell at their label. The causal argument does not directly bound their hidden slack. The next useful theorem should do one of:

1. control maximal skip-block length in terms of inherited preperiod `H` on the actual FULL tower;
2. strengthen the exit-erasing support constraint using FULL/complete-core structure rather than the bare radius-one cone; or
3. combine the half-depth rise bound with another all-depth restriction to force unbounded positive excess.

Do not return to generic nested periodic lifts, additive forced-birth counting, or finite drift sampling; those routes are already fenced in `ASTRA_AUTOMATION_HANDOFF.md`.
