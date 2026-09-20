# Run 149: transported-pair birth quotient hits a domain obstruction

Status: `stopping-fence`. No new exclusion of FULL is proved. Problem 1 remains OPEN.

## Question tested

Runs 142--148 left one specific target: after the distinguished two-bit nonresetting passage, can the transported shadow pair at the forced resetting one-bit source determine the next return/birth observable, giving an iterable small quotient?

Keep the notation of `problem1_nonreset_return_birth_spacing.md`. A two-bit nonresetting t source at physical time t forces a birth at t+6. The row at t+6 is a one-bit t source and is resetting. In the distinguished-source notation of `problem1_distinguished_source_four_step_right_pair_transport.md`, q=t+2 and

    (hat r_1,hat r_2)(q+4) = (a, a OR b).

Thus the transported pair at t+6 is one of 00, 01, 11.

## Exact obstruction

The available cyclic-source birth law cannot be applied at t+6.

`problem1_shadow_gate_birth_phase.md` proves

    chi_s = u_s XOR hat u_s

only when Y_s is A-periodic. Its direct proof uses equality of the actual row and its cyclic representative on the complete center-and-left half at the source. The forced row Y_(t+6) above is instead explicitly a newly created lag-one row: the nonreset-return theorem gives beta=1 at t+6, and states that this new one-bit t source is resetting. Hence it is not cyclic at that source.

Therefore the run-142 transported pair is not, by itself, an input to the proved birth law. Treating its zero-pair flag as the next birth flag would silently cross the theorem's domain boundary.

The existing one-bit return theorem does not repair this gap in the current eventual-K=3 branch. `problem1_one_bit_strip_return_constraint.md` proves the t/u lag-one transition law only under the stronger eventual hypotheses tau<=1 and bit-depth<=1 at all sufficiently late times. The current K=3 alternative supplies neither global hypothesis for the future of this newly born row. Importing that theorem here would therefore be circular/invalid.

## Consequence

The proposed immediate finite-state iteration

    distinguished cyclic source -> transported pair at t+6 -> next birth

is presently unavailable, for a structural reason rather than lack of Boolean expansion. More right-fringe truth tables at t+6 will not fix it: what is missing is a theorem transporting the *noncyclic resetting one-bit source* back to a cyclic source (or otherwise expressing its eventual return/birth observable) under the actual K=3 hypotheses while retaining the complete original fringe.

This also clarifies what a valid next lemma must accomplish. One needs one of:

1. a K=3-valid return theorem for the forced resetting one-bit t source at t+6, with its complete shadow/fringe retained; or
2. a birth/renewal observable valid directly on that noncyclic source, not merely on cyclic sources.

Only after such a bridge is proved can the 00/01/11 transported pair be tested as a quotient of the next episode. Until then, iterating the pair would overstate the existing results.

## Why this is useful

This is a stopping fence against a tempting but invalid composition of two individually correct lemmas. It narrows the unresolved step to a domain-extension/return problem and prevents further local driver enumeration from being mistaken for an episode transition law.
