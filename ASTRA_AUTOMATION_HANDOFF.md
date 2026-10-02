# Automation research handoff — 2026-09-13

Problem 1 remains **OPEN**. Continue on `research/astra-next`.

This handoff supplements, and does not replace, `ASTRA_HANDOFF.md` and its archived predecessors.

## Repository-state warning

The pushed `ASTRA_HANDOFF.md` says these round309 drafts existed only in its worktree checkpoint:

- `proofs/informal/problem1_three_bit_complete_core_system.md`
- `proofs/informal/problem1_complete_core_phase_transport.md`
- `proofs/informal/problem1_fixed_fringe_phase_collapse.md`

They are not present in the pushed branch. Do not reconstruct or cite their proofs from handoff summaries alone. The pushed `problem1_nonreset_return_birth_spacing.md` is inspectable.

## 1. Shift-tail excess reduction

Read `proofs/informal/problem1_shift_tail_excess_reduction.md`.

For a fixed nonzero finite original row, let `R` end its right support and put `v=L_R(r)>0`. Then

    L_(R+n)(r)=2^n v.

The global-front threshold identity gives

    tau(Y_(R+n)) = max(tau(2^n v)-(R+n),0).

Thus an eventual finite physical delay strip is equivalent to boundedness above of

    e_v(n)=tau(2^n v)-n.

The existing theorem `tau(2^n v)->infinity` is insufficient; a sufficient scalar target is

    limsup_n e_v(n)=infinity.

## 2. Exact residence ledger

Read `proofs/informal/problem1_shift_tail_residence_ledger.md`.

Put

    h_n=tau(2^n v),
    delta_n=h_(n+1)-h_n >= 0.

Define

    Z_v(N)=#{0<=n<N:delta_n=0},
    P_v(N)=sum_(delta_n>=2, n<N)(delta_n-1).

Then exactly

    e_v(N)=tau(v)+P_v(N)-Z_v(N).

Geometrically `delta_n` is the residence length of characteristic `R+n+1`: skip `delta=0` contributes `-1`, one-step residence contributes `0`, and long residence contributes `delta-1`.

The desired theorem is therefore unbounded positive excursions of `P_v-Z_v`.

## 3. Transient stripping

Read `proofs/informal/problem1_transient_stripping_zero_extensions.md`.

For finite `y`, let

    H=tau(y),
    u=T^H(y),
    x_m=A^H(2^m y).

Then

    tau(2^m y)=H+tau(x_m).

For `m<=2H`,

    x_m=sigma^(2H-m)u,

so the tower increment problem becomes a chain of nested one-bit lifts after the inherited transient is removed.

For `y=2^n v`,

    delta_n=tau(x_1),
    delta_n+delta_(n+1)=tau(x_2).

A skip is exactly `tau(x_1)=0`.

## 4. Periodic one-bit lift classifier

Read `proofs/informal/problem1_periodic_one_bit_lift_classifier.md`.

For periodic `z_s=A^s(z)`, write

    b_s=bit_0(z_s),
    c_s=bit_1(z_s),

and a one-bit lift as `A^s(w)=2z_s+a_s`. Then

    a_(s+1)=c_s XOR (b_s OR a_s).

If the low trace `b_s` is identically zero, both lifts are periodic. Otherwise there is one recurrent initial lift bit. If

    q=min{s>=0:b_s=1},

then the recurrent lift has preperiod zero and the other lift has preperiod exactly `q+1`.

Therefore universal two-step compensation is false for arbitrary periodic lifts. Do not retry it without common-origin tower structure.

## 5. Exact maximal skip-block ledger

Read `proofs/informal/problem1_maximal_skip_block_ledger.md`.

If a maximal block begins at tower index `n` and contains `k>=1` consecutive skips, transient stripping gives periodic nested lifts

    x_0,...,x_k

followed by first nonperiodic `x_(k+1)`.

The whole block plus its exit residence has exact ledger charge

    B=tau(x_(k+1))-(k+1).

Let

    q_k=min{s>=0:bit_0(A^s(x_k))=1}.

The one-bit classifier gives

    tau(x_(k+1))=q_k+1,

hence

    B=q_k-k.

So local block compensation is exactly the inequality `q_k>=k`.

That inequality is false for arbitrary nested periodic lifts. The exact chain

    1 -> 3 -> 6 -> 13 -> 27 -> 55 -> 111

consists of periodic nested lifts, while the next lift `223` has preperiod one. This gives `k=6`, `q_k=0`, `B=-6`. Thus any successful block theorem must use the shared origin `x_m=A^H(2^m y)`.

## 6. Exact zero-extension / physical-time renormalization

Read `proofs/informal/problem1_zero_extension_time_renormalization.md`.

The packed Rule-30 map satisfies

    T(2^m q)=2^m T(q).

Consequently, for all `n,t>=0`,

    A^t(2^(n+2t)v)=2^n T^t(v).

Using `tau(A^t x)=max(tau(x)-t,0)` gives the exact identity

    tau(2^n T^t(v))
      = max(tau(2^(n+2t)v)-t,0).

Equivalently,

    h_(T^t v)(n)=max(h_v(n+2t)-t,0).

At `n=0`,

    tau(T^t(v))=max(h_v(2t)-t,0).

Thus the even tower subsequence has a sharp pointwise dichotomy between A-periodic physical rows and positive physical-row preperiod.

## 7. Physical-time tail conjugacy

Read `proofs/informal/problem1_physical_time_tail_conjugacy.md`.

For every nonzero finite `v`, the established theorem `h_v(n)->infinity` removes the max branch after any fixed physical restart. Fix `t>=0`. There is `N_t` such that for every `n>=N_t`,

    h_(T^t v)(n)=h_v(n+2t)-t,

hence

    e_(T^t v)(n)=e_v(n+2t)+t.

The residence increments therefore satisfy, eventually exactly,

    delta_(T^t v)(n)=delta_v(n+2t).

So skips, one-step residences, long residences, and their `P-Z` ledger are transported under physical time by deletion of a finite prefix and translation of indices.

In particular,

    limsup e_(T^t v) = t + limsup e_v

in the extended-real sense. Therefore the target `limsup e_v=infinity` and its negation (eventual boundedness above) are invariant under restarting at any fixed physical Rule-30 time.

This also clarifies the role of the pointwise A-periodic branch at `n=0`: an A-periodic physical row can change only a finite prefix of the restarted tower. It cannot create a permanently different asymptotic residence ledger.

## 8. Physical episode ledger telescope — forced birth route fenced

Read `proofs/informal/problem1_physical_episode_ledger_telescope.md`.

For original-cut delays `s_j`, let

    Delta_j=s_(j+1)-s_j.

For every `a<b`, exactly

    sum_(j=a..b-1)(Delta_j-1)
      =(s_b-b)-(s_a-a).

Whenever both endpoint physical delays are positive, the threshold identity
`tau(Y_j)=max(s_j-j,0)` therefore gives

    sum_(j=a..b-1)(Delta_j-1)
      =tau(Y_b)-tau(Y_a).

This closes the tempting idea that a forced local birth can automatically be
counted as an independent positive `P-Z` contribution.

For the pushed TWO-BIT nonreset source profile,

    tau(Y_t),...,tau(Y_(t+6))=2,1,0,0,0,0,1,

so the whole passage through the forced birth has exact signed ledger charge

    1-2=-1.

The forced `beta=1` birth creates a resetting one-bit `t` source at `t+6`.
Its two possible delay triples are `1,1,1` and `1,0,1`, so its complete
immediate two-step passage has charge zero. Therefore the eight-step segment
from the two-bit nonreset source through that resetting passage still has
exact charge `-1`.

For a one-bit nonreset source, if its terminal `beta=1` birth occurs then the
six-step endpoint delays are both one, hence the charge is exactly zero. If
`beta=0`, the terminal delay is zero and no positive charge is forced.

Consequently the separated-birth theorem in
`problem1_nonreset_return_birth_spacing.md` cannot be converted into an
additive positive residence budget merely by summing its forced births.
The internal long residences and skips already telescope into endpoint delay.

## Current preferred target

The previous target "force a restart-local birth and count it as positive ledger gain" is now fenced off.

A viable all-depth mechanism must instead do at least one of the following:

1. force positive endpoint physical delays themselves to increase beyond every bound;
2. control the hidden negative excess `s_j-j` at zero-delay rows, where `tau(Y_j)=0` truncates that information; or
3. construct a genuinely non-telescoping global charge, distinct from the signed residence sum, with bounded reuse on the original finite fringe.

The second option is the most direct next scalar target. At a zero-delay row, define the hidden slack

    g_j=j-s_j >= 0.

The residence ledger across a segment with a zero-delay endpoint depends on this slack, while the physical strip variable forgets it. A useful next theorem would constrain how large `g_j` can become, or how quickly a later FULL source must repay it, using the same complete-core / global-shadow structure. Without such a theorem, births can be locally real but globally absorbed by skipped characteristics.

Do not resume finite sampling merely to estimate asymptotic drift. Do not retry generic nested-lift compensation. Do not sum separated births as if they were independent positive ledger charges. Do not claim a Problem 1 solution without an all-depth contradiction.


## 9. High-effort checkpoint — K=3 periods 8 and 16 eliminated (2026-09-29)

Read `problem1_k3_period8_exit_elimination.md`,
`problem1_period16_doubling_layer_reduction.md`, and
`problem1_k3_period16_exit_elimination.md`.

Finite A-cycle periods are dyadic, so the recent formal period-five candidates
are vacuous. Period 8 is excluded by exact finite-core transport.

Period 16 is now excluded on the ENTIRE temporal-driver domain, not only the
finite-core subset. Among 8,388,480 exact-period-16 drivers with forced prefix
`2221` and the backward exit phase, 8,386,657 hit a FULL contradiction with
a unique period-16 shadow phase. The remaining 1,823 drivers generate 3,647
exact phase branches after carrying both same-period forks and legitimate
16->32 shadow lift doublings. Every branch also contradicts the pushed source
laws; no branch survives beyond physical offset +42.

Therefore every eventual-K=3 `u,h=0` exit on a finite core has

    least complete-core period p >= 32.

Reusable transport:

    b^(n)_s = 2 u_(n-1)(s+n) + u_n(s+n),

    (hat r_1,hat r_2)(v+n)
      = (u_(n+1)(n),u_(n+2)(n)).

Do NOT brute-force p=32 (`4^28` suffixes). The next proof-relevant target is
an all-scale renormalization combining the nested one-bit lift system, the
cyclic/one-bit/repair source automaton, the canonical doubling layer, and the
existing dyadic derivative singularities. The goal is to make the p=8/p=16
emptiness recursive.


## 10. Period-32 canonical-chain finite-depth probe

Read `problem1_k3_period32_canonical_chain_probe.md`.

Do not enumerate `4^28` period-32 driver suffixes. Every finite period-32
core descends from a canonical anti-periodic binary 32->16 layer `q(1-q)`,
so there are only 65,536 starting chains.

Exact finite exhaustion shows that all 65,536 chains have one and only one
period-32 child, with no mergers, through lift depth 1000. Among depths
0..928 there are 118,359 nodes satisfying the K=3 exit prefix `2221` plus
the backward exit phase. Every one violates the pushed source automaton,
with the latest contradiction at physical offset +34.

This is NOT a p=32 theorem because an exit could in principle occur deeper
than lift depth 928. The useful next theorem is all-depth rigidity of these
canonical lift chains plus a uniform bounded source contradiction. Do not
merely increase the finite depth cap.


## 11. Finite-domain zero-return existence and genuine p=32 portals

Read `problem1_finite_lift_zero_return_existence.md`.

The old off-zero-cycle caveat remains valid for arbitrary periodic 2-adic
temporal words, but it is now closed on the actual FINITE A-cycle domain.
A nested fixed-period one-bit lift increases finite bitlength by one at every
step, while its complete p-period temporal code has only `4^p` possibilities
and Theta is injective. Therefore an infinite off-zero same-period lift chain
would repeat a temporal code/state, contradicting strict bitlength growth.

Hence every finite fixed-period connector eventually hits a zero low temporal
column (or, at that zero, the next child forces a period doubling). The
zero-return graph machinery is therefore unconditional on finite A-cycles.

For p=32, the canonical 16->32 parent must be one of the sixteen terminating
period-16 leaf necklaces. Thus the actual finite domain has only 16 canonical
portal necklaces modulo temporal rotation, not the 65,536 arbitrary
anti-periodic starts of the earlier overinclusive probe.

Exact audit of all 16 genuine portal connectors through 10,000,000 lifts:
10,001,374 K=3 exit-prefix/backward-phase occurrences, zero survivors, latest
FULL contradiction +42. No portal hit a zero/fork within that range. The first
portal has now been followed for 1,000,000,000 exact lifts without a zero
return; the structural theorem nevertheless proves that a finite return must
eventually occur.

Do NOT try to prove canonical chains never hit a diagonal/zero condition; on
the finite domain zero events are eventually required. The next useful theorem
is instead a connector-local invariant proving that every K=3 exit occurrence
fails the source automaton within a uniform bounded horizon (empirically <=42),
independent of total connector length.


## 12. Unrestricted period-32 +42 conjecture refuted

Read `problem1_period32_unrestricted_plus42_counterexample.md`.

The driver

    22211221323333032110021130122112

has exact period 32, prefix `2221`, and the exact backward exit phase. Its
nested shadow lifts are unique through the needed window, yet the pushed
source automaton remains valid through +42 and first fails at +44 (a one-bit
source with illegal prefix `23`).

Thus the +42 ceiling observed on ten million lifts of every genuine finite
portal is NOT a consequence of period-32 local algebra alone. The same
driver stays exact period 32 under at least one billion spatial projections,
so it is not in the shallow finite-portal region already audited.

Do not seek a universal +42 lemma on arbitrary period-32 temporal words.
The missing theorem must use finite portal/root-basin ancestry.


## 13. Deep genuine p=32 portal certificates: +42 refuted; first zero return found

Read `proofs/informal/problem1_period32_deep_portal_return_and_source_horizon_counterexamples.md`.

The previously preferred finite-portal target "every genuine p=32 K=3 exit
fails by +42" is FALSE. Exact finite-portal certificates now reach +44, +50,
and +52. In particular:

    portal 3, depth 54,261,234, phase 5
    driver 22211211321100012231222211000103
    first source failure +52.

A 100,000,000-lift scan of all sixteen genuine portals found observed maxima
between +40 and +52; +52 is finite evidence only, not a theorem.

More importantly, portal 13 (parent p16 leaf `0001001111001111`) has its
FIRST zero low-plane return at exact lift depth

    65,154,360.

The returned high plane has canonical necklace

    00000001001101101001100111100001,

weight 13, odd parity, exact period 32. Hence it is a terminal odd p=32 leaf
and has no period-32 child. Therefore this entire new full-period portal
component is a singleton leaf:

    B(0001001111001111)=0.

Do not pursue a universal +42 connector-local source bound. The next concrete
p=32 graph target is to classify the first zero return of the remaining
fifteen p16-leaf portals (or derive a structural discriminator for which
portal components are singleton versus branching).


## 14. Billion-depth genuine p=32 portal census

Read `proofs/informal/problem1_period32_billion_portal_census.md`.

All sixteen genuine period-32 portals have now been advanced exactly through
lift depth 1,000,000,000 or until their first zero low plane.

Two return before the cap:

    portal 13: depth 65,154,360
    portal  5: depth 105,696,243.

Both returned targets are odd, exact-period-32 necklaces, hence terminal.
Therefore both new full-period portal components are singleton leaves:

    B(0001001111001111)=0,
    B(0000100100100101)=0.

The other fourteen portal connectors have no zero return through 10^9 lifts.
This is only a lower bound; return existence is already proved structurally.

This sharply changes the p32 graph target: determine whether more of the
remaining fourteen portals are singleton components, and find a structural
predictor for endpoint parity from the period-16 parent leaf or portal
boundary word. Connector length itself is not such a predictor.


## 15. Pair-XOR period-halving route refuted at 32 -> 16

Read `proofs/informal/problem1_pair_derivative_p32_counterexamples.md`.

The two newly computed genuine terminal p32 leaves are exact counterexamples to
the old `Delta_2` period-halving conjecture. For each p32 leaf, both
rotation-inequivalent adjacent-pair XOR outputs are absent from the complete
set of sixteen terminating p16 necklaces.

Therefore "terminating at 2p => some pair-XOR phase terminates at p" is false
at 32 -> 16. Do not pursue raw decimation or pairwise XOR as the missing
dyadic semiconjugacy.


## 16. Last-reset child formula and static endpoint-parity no-go

Read `proofs/informal/problem1_last_reset_child_and_endpoint_parity_complexity.md`.

For any nonzero parent low plane `b`, choose the last reset phase `r`
before the phase cut. The unique recurrent child seed is exactly

    a_0 = 1 XOR XOR_(s=r..n-1) c_s.

So future deep connector code should not trial both cyclic seeds; the full child
is determined in one forward pass once this suffix parity is known.

The formula was exhaustively checked on all 86,870 parent-plane pairs for
periods 1..8.

A complete lower-scale portal census was also run. For all 128 odd p8 words,
their antiperiodic p16 portal connectors return to 56 odd and 72 even targets;
the longest first return is 214,005 lifts. The returned-target parity function
has no representation as a constant plus cyclic monomial-orbit sums of degree
<=6. An exact degree-7 formula exists, but reusing that same relative-offset
formula at p16 already fails on known p32 singleton portal 13.

Do not fit another low-degree static Boolean score to the p16 leaf word alone.
A viable p->2p classifier must retain connector/half-period auxiliary state or
use a genuinely scale-dependent renormalization. The last-reset formula is the
preferred primitive for building such a multi-step transducer.


## 17. Broadword child transducer and first nontrivial p32 portal trees

Read `proofs/informal/problem1_period32_broadword_portal_tree.md`.

The recurrent child recurrence is affine phase-by-phase:

    a_(s+1) = d_s XOR m_s a_s,
    d=b XOR c,  m=1 XOR b.

Using the exact last-reset seed from run 16, the full 32-phase child can be
computed by five broadword affine-prefix stages at shifts 1,2,4,8,16. A
million deterministic period-32 comparisons against the scalar recurrence
give zero mismatches. Use this transducer for deep p32 connector work.

Four additional genuine portal roots are now resolved:

    portal 0: first return 1,420,791,101 -> even p32 target
    portal 2: first return 1,555,560,444 -> odd p32 leaf
    portal 6: first return 1,255,920,142 -> even p32 target
    portal 7: first return 1,324,488,168 -> odd p32 leaf.

Together with the earlier portals 5 and 13, singleton components are now proved
for portals 2,5,7,13. Portals 0 and 6 genuinely branch.

Exact descendant scans already give

    B(portal 0) >= 3,
    B(portal 6) >= 5.

Since the dyadic leaf theorem gives

    L_32 = 16 + sum B(l),

we now have the rigorous lower bound

    L_32 >= 24.

This is the first exact p32 leaf-count improvement beyond the trivial sixteen
portal components. The preferred next target is a half-period or multi-lift
renormalization of the affine prefix monoid, not a static leaf statistic.


## 18. Complete p32 portal-root census; L32 >= 30; one-lift half-block route fenced off

Read proofs/informal/problem1_period32_complete_portal_root_census.md.

All sixteen genuine period-32 portal roots now have exact first zero returns.
The root split is

    odd / singleton:  2,3,5,7,9,13,14,15
    even / branching: 0,1,4,6,8,10,11,12.

The deepest root is portal 4, whose first zero occurs at depth

    15,565,342,385

and returns to an even exact-period-32 target.

Combining the complete root census with the previously proved descendant
bounds B(portal 0)>=3 and B(portal 6)>=5 gives

    sum B >= 14
    L_32 = 16 + sum B >= 30.

This is rigorous but is only a lower bound; the eight branching p32 portal
trees are not completely enumerated.

The half-period affine recurrence also has an exact block path normal form.
A p-phase block is encoded by (r,q), where r is the first reset position (or
p if none) and q is the seed-zero output path. There are exactly
(p+1)2^p such block path transducers.

For every doubled odd portal with antiperiodic lift x, two lifts have the
universal phase-quotient normal form

    T^2(x,0) ~ (x,1^(2p)).

However, the initial one-lift half-block response is insufficient to decide
portal endpoint parity even on the genuine p32 domain. The genuine portals
with the same initial half-block code have mixed outcomes in every reset class
containing at least two portals.

Do not spend more work classifying p32 portal roots; that census is complete.
Do not use only a static p16 leaf statistic or the initial one-lift half-block
code. The preferred next target is a genuinely multi-lift renormalization
starting from the exact two-lift normal form, or exact descendant comparison
of the newly branching roots 1,4,8,10,11,12 against the existing portal-0
and portal-6 trees.

Reproducers:
experiments/problem1_nonperiodicity/check_period32_complete_portal_roots.cpp
and experiments/problem1_nonperiodicity/check_half_period_block_transducer.py.
Atomic record:
results/problem1/20261002_period32_complete_portal_root_census.json.


## 19. Twisted half-period portal system; deeper p32 trees; L32 >= 43

Read proofs/informal/problem1_twisted_half_period_portal_and_p32_descendants.md.

Pair temporal phases s and s+p. The exact 2p child recurrence becomes a
p-phase four-symbol recurrence with a SWAP boundary after p phases. This is an
exact half-period conjugacy, not the false pair-XOR semiconjugacy.

Starting from the universal two-lift portal normal form (x,1^(2p)), with x
antiperiodic and H(x)_s=(q_s,1-q_s), the next child is governed by the exact
two-bit state

    q=0: (U,D) -> (1-U,1-U)
    q=1: (U,D) -> (0,1-U-D)   over GF(2).

The words 01 and 10 are synchronizing: their two-step maps are constant.
Consequently the third lift is reset-anchored by any change in q and its
paired alphabet excludes 11 entirely. This is an exact three-symbol slice,
verified on all 1,023 odd lower words for p<=10. Later lifts can reintroduce
11, so the three-symbol sector is not claimed invariant.

Exact descendant work should now be used only as a test suite for this
renormalization. It gives:

    B(0)>=3, B(1)>=1, B(4)>=2, B(6)>=5,
    B(8)>=7, B(10)=3, B(11)>=5, B(12)>=1,

hence

    sum B >= 27
    L_32 >= 43.

Portal 10 is fully classified: exactly 3 even internal vertices and 4 odd
leaves. Portal 8 contains an even vertex with TWO even children, so the
hypothesis that every internal p32 vertex has a terminal sibling is false.

Do not continue blind p32 enumeration just to raise the bound. The next
proof-relevant target is a multi-lift return transducer on the twisted paired
system, starting from the synchronized three-symbol third-lift slice, and
testing whether its state can be bounded independently of p or tied to the
finite-support resource in the main Problem 1 argument.

Reproducers:
experiments/problem1_nonperiodicity/check_twisted_half_period_portal.py
and experiments/problem1_nonperiodicity/check_period32_descendant_expansion.cpp.
Atomic record:
results/problem1/20261002_twisted_half_period_and_p32_descendants.json.


## 20. All-depth finite-stack phase quotient; genuine blind-edge obstruction

Read proofs/informal/problem1_portal_multilift_phase_quotient.md.

The half-period construction now extends to EVERY finite number r of spatial
lifts. Pair each 2p temporal word into p half-pairs and write each pair as
(X,X XOR Y). After the universal two-lift normalization, simultaneous
half-swap G removes the antiperiodic prefix phase exactly. If w is the original
odd lower-period leaf, the normalized r-layer stack satisfies

    R_(s+1) = G^(w_s) Phi_0(R_s),
    R_p = R_0.

Thus the twisted 2p boundary has been converted into an ordinary p-cycle
driven directly by w. The update is triangular in spatial depth and is exact
for arbitrary finite r.

For the first two dynamic layers the exact sector is the five-state machine

    A: 0->E, 1->C
    B: 0->D, 1->B
    C: 0->D, 1->B
    D: 0->A, 1->A
    E: 0->A, 1->A.

Every 1** word synchronizes it. There is also the exact parity law

    P(third lift) XOR P(fourth lift) = p mod 2,

so these two lift parities agree at every even dyadic scale.

Adding the fifth lift gives an exact 14-state even-length/odd-weight sector.
It has two blind states where input 0 and 1 produce the same next quotient
state.

This blindness is genuinely proof-relevant. Period-16 leaf portals 5 and 6
have the SAME complete 14-state orbit through the fifth connector lift,
modulo temporal rotation:

    [4,26,51,4,26,51,4,26,51,4,31,36,31,36,26,51].

Their aligned leaf labels are

    portal 5: 1001001010000100
    portal 6: 1011001000000100,

and they differ only at two visits to blind state 51=(1,1,0,0,1,1).
Nevertheless the exact p32 root outcomes are opposite:

    portal 5 -> odd singleton at depth 105,696,243
    portal 6 -> even branch at depth 1,255,920,142.

So an unlabeled shallow multilift orbit cannot decide endpoint parity even on
the genuine p32 domain.

The sixth lift explains how the missing information returns. At blind state
51, if its added deepest pair has difference Q, the next normalized deepest
pair is

    (1 XOR w Q, Q).

When Q=1 it carries the hidden driver bit forward. This is the first explicit
blind-label memory channel.

Exact SCC analysis, with no period cap, gives even-length/odd-weight sector
sizes for r=1..8:

    3, 5, 14, 30, 75, 195, 443, 1168.

There are explicit rotation-inequivalent odd-driver pairs with the same
unlabeled quotient orbit at every r=4..8, so the naive observer does not
stabilize through eight layers.

Finally, zero return has an exact formulation in the projective tower:
the first zero return is the first spatial layer whose pair-track is (0,0) at
EVERY phase; the returned target parity is the XOR of the preceding layer's
Y-track.

The next proof target is no longer the half-period twist. It is the recursive
extension/observer law for blind labels: determine whether hidden driver
information can be charged to a finite resource, or whether first all-zero
track/parity can be computed without constructing an unbounded spatial stack.

Reproducer:
experiments/problem1_nonperiodicity/analyze_portal_multilift_phase_quotient.py
Atomic record:
results/problem1/20261002_portal_multilift_phase_quotient.json.


## 21. Portal 11 completely classified; L32 >= 55

Read proofs/informal/problem1_period32_portal11_complete.md.

The full-period component attached to p16 leaf

    0101111111011111

is now completely resolved. It contains exactly

    17 even internal vertices
    18 odd terminal leaves,

so

    B(portal 11) = 17

exactly. The maximum tree depth is 12. Its 34 child connectors total
107,937,533,586 exact lifts; the deepest edge has
12,479,646,968 lifts.

Combining the exact portal-11 count with the other certified p32 components
gives

    sum B >= 39
    L_32 >= 55.

Portal 11 also kills two naive local-resource bounds. Its old p16 leaf has
weight 13, while B=17, so neither B(l)<=weight(l) nor B(l)<=16 can hold in
general. This does NOT rule out a larger bound tied to the original finite
survivor support.

Use portal 11 as a stress-test fixture for the projective extension/observer
tower from run 20. Any proposed bounded observer should reproduce its 17
internal nodes, two-even-child forks, and 18 terminal parities.

Reproducer:
experiments/problem1_nonperiodicity/check_period32_portal11_complete.cpp
Atomic record:
results/problem1/20261002_period32_portal11_complete.json.


## 22. Genuine p32 roots separate exactly at the sixth connector lift

Read proofs/informal/problem1_genuine_portal_observer_depth.md.

Apply the run-20 unlabeled finite-stack quotient only to the sixteen genuine
p16 leaf portals. The exact orbit counts for dynamic depths r=1..8 are

    distinct orbits: 15,15,15,16,16,16,16,16
    mixed-parity classes: 1,1,1,0,0,0,0,0.

For r=1..3 the sole mixed class is always portals 5 and 6. At r=4, which
includes the sixth connector lift, those two separate and ALL sixteen genuine
root orbits are distinct. They remain distinct through r=8.

Therefore the sixth-lift unlabeled quotient is sufficient to identify every
current genuine p32 root and hence its root endpoint parity. This is a finite
p32-domain fact only; run 20 has arbitrary-driver collisions at r=4..8.

There is no affine GF(2) parity readout from sixth-lift state-visit counts:
the sixteen roots collectively visit 29 quotient states, and Gaussian
elimination on a constant plus those 29 visit-parity features is inconsistent
with the endpoint labels.

So the sixth lift restores the missing portal-5/6 information, but not as a
simple linear counting invariant. Continue with the recursive blind-label
extension law rather than fitting another shallow statistic.

Reproducer:
experiments/problem1_nonperiodicity/analyze_genuine_portal_observer_depth.py
Atomic record:
results/problem1/20261002_genuine_portal_observer_depth.json.


## 23. Blind-label extension law; 8-state blindness automaton; observer depth reaches 10

Read proofs/informal/problem1_blind_label_extension_delay.md.

The recursive blind-label problem now has an exact one-layer law. If an
r-layer quotient transition is blind and a deeper input pair is (P,Q), with
the preceding two pairs (H,K),(L,M), then

    P+ = H XOR (L OR P)
    Q+ = K XOR M XOR Q XOR LQ XOR MP XOR MQ,

and after driver label w the deepest normalized output is

    (P+ XOR w Q+, Q+).

Thus Q+=0 keeps the label hidden and Q+=1 records it in the added layer.

Even better, persistence of blindness across spatial depth is itself only an
8-state regular language. The context is

    (K,L,M)=(Y_(j-2),X_(j-1),Y_(j-1)),

and the next pair (X,Y) is blind-compatible exactly when

    K XOR M XOR Y XOR LY XOR MX XOR MY = 0.

The raw blind-prefix counts have generating function

    (1+x)/(1-x-2x^3)

and recurrence

    b_r=b_(r-1)+2b_(r-3).

There are arbitrarily deep raw blind stacks: (11)^r is blind for every r.
Therefore no universal constant recovery depth follows from local quotient
algebra alone.

Cyclic odd drivers restrict this strongly but not to a fixed shallow depth.
Complete odd-necklace exhaustion gives first injective observer depths

    p:  2  4  6  8 10 12 14 16 18 20 22 24 26 28
    r:  1  1  3  4  4  5  5  8  9  9  9 10 10 10.

So depth 8 already fails at p=18, and depth 9 fails at p=24. The genuine p32
root set separating at r=4 is therefore a real finite-root-basin restriction,
not a generic odd-driver fact.

The next target is to intersect the 8-state blind spatial automaton with
finite portal/root-basin ancestry and seek a support-controlled charge on
blind-context persistence. Do not assume every hidden label reappears after a
universal fixed number of layers.

Reproducer:
experiments/problem1_nonperiodicity/analyze_blind_label_extension_delay.cpp
Atomic record:
results/problem1/20261002_blind_label_extension_delay.json.
