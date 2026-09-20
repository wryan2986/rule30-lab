# Run 159: the two surviving g=2 itineraries are exact shadow-front patterns

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue the distinguished sufficiently-late TWO-BIT nonreset passage and put

    q=t+2.

Runs 156--158 reduce the unresolved terminal hidden-slack case g_(t+5)=2 to exactly two possible original-cut residence itineraries:

    A: (d_2,d_3,d_4,d_5)=(1,0,0,4),
    B: (d_2,d_3,d_4,d_5)=(0,1,0,4).

At the distinguished cyclic source row q the exact actual block gives

    r_1(q)=1, r_2(q)=0.

Run158 showed that the cyclic core/gate quotient cannot distinguish A from B. The global discrepancy-front identity does distinguish them exactly.

## Exact front location at time q

For the fixed original cuts, let

    J(u)=min{j:s_j>u},
    m(u)=J(u)-u.

The global-front theorem proves that m(u) is the physical position of the leftmost actual-vs-shadow discrepancy at time u.

We have s_q=q.

### Itinerary A = (1,0,0,4)

Here s_(q+1)=q+1. Hence at u=q,

    s_q=q <= q < s_(q+1)=q+1,

so

    J(q)=q+1,  m(q)=1.

Therefore position 1 is the leftmost discrepancy. Since r_1(q)=1,

    hat r_1(q)=0.

Thus A is equivalent, at the source row, to the shadow beginning to disagree at position 1.

### Itinerary B = (0,1,0,4)

Here s_(q+1)=q and s_(q+2)=q+1. Hence

    J(q)=q+2,  m(q)=2.

So actual and shadow agree through position 1 and first disagree at position 2. Using the rigid actual bits r_1(q)=1 and r_2(q)=0 gives

    hat r_1(q)=1,
    hat r_2(q)=1.

Thus B is equivalent, at the source row, to shadow pair

    (hat r_1,hat r_2)(q)=(1,1).

Combining both cases:

    A <=> m(q)=1 <=> hat r_1(q)=0,
    B <=> m(q)=2 <=> (hat r_1,hat r_2)(q)=(1,1),

within the already-established g=2 branch and distinguished source hypotheses.

## Why this is useful

This identifies precisely the information lost by the cyclic-core quotient in run158. The unresolved distinction is not an abstract tail property: it is the first one or two right-of-center bits of the COMPLETE original shadow at the distinguished cyclic source.

The result also gives a concrete bridge to the older global-shadow and right-pair transport calculations. Any independent theorem fixing hat r_1(q), or excluding the pair 11 at q under the distinguished nonreset hypotheses, immediately removes one of the two g=2 itineraries. Conversely, an admissible source with either shadow pattern realizes the corresponding front location at time q; no further core comparison is needed to identify which itinerary begins.

Do not confuse this with the transported pair at q+4 from run149. That later pair belongs to the forced noncyclic resetting source and cannot be fed into the cyclic-source birth law. The present criterion is at the cyclic source q itself and uses only the exact global-front identity.

## Next target

Search the established global-shadow/source identities for a constraint on

    hat r_1(q)

or on

    (hat r_1,hat r_2)(q).

If none exists, the right next computation is a complete-shadow finite-support witness search conditioned on the distinguished source and g=2, rather than another cyclic-core or residence calculation.

Dependencies: `problem1_global_discrepancy_front.md`; `problem1_run156_g2_forces_two_skips_then_four_step_residence.md`; `problem1_run157_g2_third_itinerary_excluded_by_source_bit.md`; `problem1_run158_surviving_g2_itineraries_are_core_indistinguishable.md`; `problem1_run150_distinguished_source_forces_011_provenance_obstruction.md`.
