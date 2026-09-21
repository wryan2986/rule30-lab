# Astra automation handoff — run 177

Problem 1 remains OPEN.

Run 177 extracted the exact hidden-slack path of the now-complete one-bit nonresetting passage. With `g_j=j-s_j`, the proved itinerary gives

    (g_t,...,g_(t+6)) = (-1,0,0,0,1,0,-beta), beta in {0,1}.

Hence the earlier six-step signed charge is exactly

    beta-1 = g_t - g_(t+6),

which makes the telescope obstruction explicit on this passage.

More importantly, combining this with the complete-core terminal classification gives a clean dichotomy at `t+6`:

* beta=0: lag is erased (`g=0`) and the row is cyclic;
* beta=1: lag one survives (`g=-1`) but the row is resetting (complete code at A-time 1 equals gate symbol 1).

Thus a late one-bit NONRESETTING passage cannot exit with both ingredients needed for another such source: beta chooses whether lag or nonresetting-core status is destroyed.

New note: `proofs/informal/problem1_run177_one_bit_passage_slack_reset_dichotomy.md`.

Next target: do not continue local beta magnitude/prefix work. Study the first possible RECOMBINATION after the terminal dichotomy. In beta=0, track the first later creation of negative slack from cyclic `g=0`; in beta=1, track whether the resetting witness can disappear while lag one persists, or whether lag must heal first. Seek an all-depth cost/monotone or bounded-reuse event attached to this recombination. Existing results only guarantee no new nonresetting source through `t+7`, so anything stronger needs a new invariant rather than a longer finite gate word.
