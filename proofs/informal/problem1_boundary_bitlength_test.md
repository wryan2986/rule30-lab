# Does the boundary exclusion need frontier membership?

Status: `inconclusive` for the all-depth candidate. The fixed finite box
below is `finite-exhaustive`, with independent full-orbit replay.

## Admission and mathematical purpose

The canonical-return reduction is committed and pushed at
`33fdfaf8e2bedb94728daf3b2de219eb47f20876`. B_all is still open. Before trying
an invariant on ordinary frontiers, test whether the simpler bit-length
condition alone could suffice.

Candidate (`heuristic`, not a theorem): for every positive integer x with
`k=ceil(bitlen(x)/2)>=2`, its forced schedule has no full-domain three-return
occurrence at cut `c>=k-2`. This drops membership in O_(a,k), keeping only
its bit-length law. It uses the same forced recurrence and admissibility
convention as B_all; the final appended u is not observed.

Ranked next routes (`heuristic`):

| Rank | Candidate mechanism | All-depth potential | Falsifiability / cost |
| --- | --- | --- | --- |
| 1 | Bit-length-only boundary exclusion | Strong if true; avoids frontier correlations | High / very low |
| 2 | A frontier-specific invariant at the critical cut | Strong; directly addresses B_all | Unknown until specified / high |
| 3 | Exact joint-fiber correlations over canonical returns | Strong for signed nonvanishing; separate boundary remains | Medium / high |

Admitted search: integers x=4,...,4095 in increasing numeric order, stopping
at the first counterexample or exhaustion. Thus bit lengths 3 through 12,
with k determined separately for each input. Read at most k+14 forced
branches; the proved localization makes this horizon exact for the boundary
predicate, including schedules that stop or become inadmissible. Test the
literal 56-triple definition, with the first cut and lexicographic triple
reported. No phase-frontier search or historical census-cap increase.

A counterexample refutes removing frontier membership and supplies a named
state for checking what extra frontier information excludes it. No example
in this box would prove an infinite bound or justify a larger box. That
outcome instead calls for a structural bit-growth derivation or a change of
route. One local CPU, 120 seconds and 1 GiB; atomic JSON with embedded source,
full Git commit, exact parameters, timings, hashes and limitations. Any
reported example must be replayed independently before adoption.

## Immediate constraint on a bit-length proof

The established degree law already prevents using raw bit length as a
decreasing rank. For a continuing x, put z=x>>2. Then z>0, and each of
T,P,U adds two to positive input bit length. Consequently

```text
bitlen(F(x)) = bitlen(Q(P(z))) = bitlen(x)+2.
```

For every finite continuing orbit segment,
`bitlen(F^j(x))-2j=bitlen(x)`. This exact identity provides no decreasing
quantity or termination argument. Even if the candidate survives the fixed
box, a proof must control digit correlations or admissibility, not just
repeat the degree law. This observation does not rule out a more refined
bit-length-dependent invariant.

## Fixed-box outcome and interpretation

All 4,092 inputs x=4,...,4095 were exhausted; no boundary occurrence was
found. The literal 56-triple search executed 1,039 forced transitions. The
lead independently regenerated every orbit using cell arrays, the odd
section identity `P(z)=T(2z+1)>>1`, and the proved third-u prefix criterion.
All states and branch words agree. No input reached its k+14 horizon, so
all these particular schedules were also observed through termination.

Coverage is weak and must not be hidden: only ONE input in this entire box
has any three-return occurrence at any cut. It is x=903 (`0x387`), k=5,
with forced word `utututt` and occurrence cut 0, gaps (2,2,2). The critical
threshold is 3, so it does not test a nearly violating boundary cut. The
maximum admissible prefix length in the box is 7; the maximum total forced
word length is 14. The latter can include inadmissible words.

These observations neither prove the broader bit-length candidate nor show
that ordinary-frontier membership is necessary. The candidate remains open.
No larger box is warranted by absence. The next useful question is a
structural lower bound on the initial integer imposed by a late three-return
prefix, or a more specific frontier invariant.

The exact arithmetic reformulation is:

```text
For every occurrence at cut c, the bit-length-only candidate requires
x >= 4^(c+2).
```

Indeed `c+1<=ceil(bitlen(x)/2)-2` is equivalent to
`bitlen(x)>=2c+5`, hence to the displayed integer bound. This merely
rewrites the conjecture; it provides no proof of the lower bound.

Atomic records (each includes executed source and exact provenance):

- `results/problem1/20260905_boundary_bitlength_primary.json`: default
  reviewer Dewey's literal search, with its original contributed payload
  retained unchanged inside the standard protocol record.
- `results/problem1/20260905_boundary_bitlength_independent.json`: lead
  cell-array replay, complete orbit agreement, and explicit occurrence
  coverage. This is the same admitted box, not a search extension.

Muse's provider was unavailable in this phase after two terminal HTTP 429
responses. Neither run is attributed to Muse. No all-depth conclusion is
drawn from the finite checks.

Independent final review by Dewey accepted the arithmetic reformulation,
the degree identity, and these proof/evidence boundaries without correction.
The two elementary identities are `partial-proof` statements; they do not
upgrade the status of the open bit-length-only candidate.
