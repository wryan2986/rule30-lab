# Composed inverse signs and ordinary predecessor membership

Status: `partial-proof` for the arbitrary-tail sign criteria; `refuted` for
universal positivity from the entire leading-core family and the ordinary
backward-closure simplifications below. Finite comparisons are
`finite-exhaustive`.
Base checkpoint: `d799144d0d109deb0c2567817ec9a67c10b12dc2`.
Problem 1 remains open.

## Critical-path question and admission

The latest decoder checkpoint makes the first inverse positive on sufficiently
deep ordinary frontiers, but leaves the second inverse sign and full ordinary
predecessor membership open. Its leading-core backward-closure counterexample
is not ordinary. Do not promote it to an ordinary-domain counterexample.

Ranked routes (`heuristic`): first decide the exact sign information retained by
a composed inverse transducer; then test a full-membership predecessor argument
on named certificates; finally consider a return-conditioned boundary-sum
inequality if neither inverse route supplies an induction. No wider frontier,
core, or branch-word census is admitted.

The first precise hypothesis is that one of the already certified leading
cores makes both stages of a forced inverse nonnegative, independently of the
lower tail. Fix the eight level-eight heads from the previous checkpoint and
the two previously used bytes 200 and 222. Compute their transfers on the
sixteen pairs of two-bit inverse states. Restrict conclusions to reachable
states after the branch-specific first two bits. Reachability can be decided
on this finite transducer without scanning integers or extending a head atlas.
If sign synchronization fails, find bounded finite-state paths witnessing the
failure, recording the distinction between a core-compatible integer and an
ordinary endpoint.

Either outcome changes the whole-tail argument: synchronization would remove
the second sign obstruction with all lower-tail lengths quantified; mixed
reachable signs would refute that leading-head simplification and require
additional membership information. Finite examples alone do not establish
any occurrence bound or infinite survival/exclusion theorem.

Local computation is limited to one CPU per implementation, 120 seconds and
1 GiB, with atomic JSON, full Git, source/input hashes, hardware/software
facts and timings. Independent Boolean and arithmetic implementations must
agree before adoption. No optimized backend or immutable-reference edit is
needed. The existing examples B_u(27)=7 and B_t(7)=-5 are hand controls.

## Definitions and algebra to verify

Use T(v)=v XOR((v<<1) OR(v<<2)), U=T XOR1 and
P(v)=T(v) XOR1 XOR(2 if v is even else0). For x>=0, x=3 modulo4,
write a=Q^-1(x), b=P^-1(a), and B_q(x)=4b+3.

Above the first two bits the two inverse stages obey

    a_i=x_i XOR(a_(i-1) OR a_(i-2)),
    b_i=a_i XOR(b_(i-1) OR b_(i-2)).

In newest-bit-first order, the states after bits0,1 are

    q=t: (a_1,a_0;b_1,b_0)=(0,1;1,0),
    q=u: (a_1,a_0;b_1,b_0)=(1,0;0,1).

The first inverse's zero tail is already controlled by the previous leading
byte theorem. Once its state is00, the second inverse's terminal state00
gives a nonnegative integer; each of01,10,11 evolves to11 under further zero
input and gives a negative integer. A nonnegative B_q requires b>=0.

For i>=4 the forward composition loses all low-bit generator corrections.
Putting e_j=b_(i-j), one obtains

    x_i = b_i XOR (e_1 OR e_2)
          XOR ((e_1 XOR(e_2 OR e_3))
               OR (e_2 XOR(e_3 OR e_4))).

This is triangular in b_i. Arbitrary following x bits are therefore equivalent
to arbitrary following b bits, with four previous b bits as sufficient memory.
It does not follow that all sixteen pairs of inverse states are reachable;
the relation a=T(b) above the low correction constrains those pairs.

This finite machine decides the sign of one inverse block. It is not a finite
state model of the growing forward orbit and does not decide ordinary
membership or admissibility of an unbounded branch word.

The draft t initialization was corrected before adoption: after the P-inverse
low correction its input bits are (bit0,bit1)=(0,1), so b_1=1, not0.
Muse caught this discrepancy independently using the signed hand control.

## Exact reachable-state and sign classification

Encode (a_1,a_0;b_1,b_0) as 8a_1+4a_0+2b_1+b_0. The pure transition
on input e is obtained by forming a'=e XOR(a_1 OR a_0),
b'=a' XOR(b_1 OR b_0), and replacing the state by (a',a_1;b',b_1).
The reachable set, allowing any lower length l>=2, is exactly

    R={0,3,4,6,7,9,10,12,13,14}.                      (1)

Both branch-specific starting states lie in R, and R is closed under both
inputs. At lower length6, each branch already reaches every member of R.
Equality at all greater lengths follows because the image of R under the
two transitions is R. This finite closure argument proves (1) for every
lower length; it is not an extrapolation from the lengths checked.

For each head, read its ordinary binary expansion from low to high, starting
in the state produced by the l lower bits. The complete transfers send every
one of the sixteen possible incoming states directly to0 or3. These output
states are fixed under a zero tail:0 means a,b both nonnegative,3 means a
nonnegative and b negative. Here none of a,b can be zero in the positive
case, since the large x exceeds Q(P(0)). Thus B_q is positive or negative.

| Head H | Positive / negative over all16 | Negative incoming states in R |
| --- | --- | --- |
| 51292 | 12 / 4 | 0,3 |
| 51431 | 12 / 4 | 0,3 |
| 56937 | 16 / 0 | none |
| 57038 | 12 / 4 | 0,3 |
| 25646 | 12 / 4 | 0,3 |
| 25715 | 8 / 8 | 9,10,12,13,14 |
| 28468 | 16 / 0 | none |
| 28519 | 12 / 4 | 0,3 |
| 200 | 10 / 6 | 3,4,12 |
| 222 | 4 / 12 | 4,6,7,9,10,12,13,14 |

This table is an exact all-lower-tail decision rule (`partial-proof`). In
particular, for every l>=2 and v=3 modulo4 with 0<=v<2^l,

    x=2^l*28468+v  =>  B_t(x)>0 and B_u(x)>0.          (2)

The head56937 has the same property, also a consequence of (2) because
56937=2*28468+1. Using the existing stabilized cores, (2) covers the
ordinary p,k>=19 subfamily with level-eight head56937 and the ordinary
u,k>=18 subfamily with level-eight head28468. It does not cover every
ordinary endpoint and does not establish ordinary predecessor membership.

For the five heads51292,51431,57038,25646,28519, a negative B_q occurs
exactly when the first inverse's last two bits below the head are00.
For head25715 it occurs exactly when the first inverse's highest bit below
the head is1. These are equivalent descriptions of the displayed reachable
state sets, not conditions on a fixed number of original output bits.

The six mixed level-eight heads remain mixed after restricting to reachable
states. Some equal-length witnesses (`refuted`, exact named integers) are:

| H,q,l | Positive x, B_q(x) | Negative x, B_q(x) |
| --- | --- | --- |
| 51292,t,3 | 410339, 102859 | 410343, -383109 |
| 25715,t,3 | 205727, 51291 | 205723, -98837 |
| 200,t,3 | 1603, 331 | 1607, -773 |

The record gives a positive and negative witness for both branches of every
mixed head, all at equal lower length within each pair. These witnesses
refute universal head-family positivity, with no ordinary-membership or
genuine-return assertion. For every l>=6 the full reachable set R is
attained, so every mixed head has both signs at that SAME l in EACH branch.
In particular the obstruction persists at arbitrarily large complexities
with the proper phase parity and beyond the existing stabilization ages;
it is not only a small-width exception to the relaxed head-family claim.

## Verification of the first sign calculation

Muse used Boolean inverse-bit transitions. The lead's independent arithmetic
implementation solves the forward triangular equations bit by bit, including
artificial low boundary values for all16 transfers. It agrees on all160
head/state transfers, all32 named signed witness values, the two initial
states and the reachable sets at lower lengths2..7. All32 truth-table cases
for the order-four forward formula also agree with packed T(T(b)).

The primary preserves its raw JSON and source. Its prose advertises an
additional l<=12 sampling pass that its source does not execute; that claim
is not adopted. The actual witness search stops by l10, and positivity of
the two heads follows from their complete transfer, without further samples.
The original signed-inverse helper has a bit256 cutoff, above every input
used in that run; neither the finite transition table nor the independent
arithmetic implementation has that cutoff.

## Follow-up admission: ordinary membership and the actual gate

If an ordinary x has a last T or U parent y at a sufficiently deep ordinary
level, uniqueness gives Q^-1(x)=y. The previous leading-byte theorem makes
P^-1(y)>0. In particular at k>=9 in p and k>=10 in u, such a representation
ensures at least one positive B. This `partial-proof` leaves P-only final
representations as the possible obstruction to having any positive inverse.
It does not imply that the positive B is itself ordinary.

The source-head test composes a forward P with both inverse branches and
retains the source's existing level-eight head. Its finite state is the two
source bits and the two bits of each of the four inverse streams. This has
at most1024 states and needs no larger leading-core catalogue. A source-head
sign failure alone is still not an ordinary counterexample; an explicit
ordinary word is required.

Muse supplied one such word with x=29203507 and both predecessors negative.
However x=3 modulo16, so its current forced step is undefined. It only
refutes backward positivity on ordinary endpoints ending3 modulo4.

To discriminate the missing gate condition, admit ONLY the81 four-letter
extensions of the SAME existing u,level-eight head25715 followed by P.
These words are contained in the just-executed source-word set; the new
observable is the actual future gate and full predecessor membership. For
each endpoint with a defined current gate, evaluate both exact signed forced
predecessors and their full ordinary membership using the existing recursive
criterion. Track at most16 actual admissible branches of each named endpoint.
Stop at the first qualifying counterexample or this fixed word set, without
adding any core, level or word. A counterexample with a real gate refutes
the corresponding one-step backward claim; absence is only finite evidence.
Neither outcome alone decides an induction restricted to long decoder words.
The same120-second/1-GiB local and atomic-provenance limits apply.

## Source-head refinement and a nongated ordinary counterexample

The forward-P/two-inverse product has174 reachable states after the two low
source bits00, which are exactly the low bits required for P(v)=3 modulo4.
Closure under both following source bits gives all lower lengths. For each
of the eight existing source heads, all174 head transfers followed by48
zero source bits land in fixed states: source and first-inverse tails are0,
and each second-inverse tail is0 or1. Directly checking those states are
fixed, rather than only waiting48 steps, certifies the infinite tail.

For source heads51292 and25646, BOTH second inverses are positive in all174
states. The finitely many l=0,1 cases with P(v)=3 modulo4 pass separately.
The other six source heads have reachable transfers with both signs negative.
These are exact source-head statements (`partial-proof`) for all lower
lengths, not ordinary-membership conclusions or an enlarged core atlas.

An explicit ordinary failure is

    phase u, k13, word from zero: uuuuuututuuup,
    v=6583248, x=P(v)=29203507,
    B_t(x)=-21630965, B_u(x)=-21631001.                (3)

The eight-letter rooted prefix uuuuuutu reaches the existing core25715;
the source then appends tuuu and x appends p. This proves ordinary
membership by direct word replay. Both forced predecessors are negative,
so neither can be an ordinary finite positive predecessor. But x=3 modulo16:
there is NO actual forward forced step here. Equation (3) refutes only the
universal ordinary x=3 modulo4 positivity assertion, not its continuing
subdomain. It also illustrates the distinction between a SOURCE head and
the OUTPUT head in the preceding sign theorem.

## Positive predecessors still need full ordinary membership

The fixed-source follow-up finds its first eligible endpoint on word49 in
the declared order. It has

    phase u, k13, word from zero: uuuuuutuuputp,
    source v=6583240, x=P(v)=29203579,
    actual forced states: 29203579,116608679,467256739,
    complete admissible forced word: tu.             (4)

The last displayed state is3 modulo16, so the orbit stops there. Both ttu
and utu are admissible prepends to tu, but the only two possible predecessors
are

| Prior branch | Q^-1(x) | P^-1 Q^-1(x) | B_q(x) |
| --- | --- | --- | --- |
| t | 6583205 | 1822298 | 7289195 |
| u | 6583206 | 1822305 | 7289223 |

Both are positive, have the correct23-bit width for u,k12, and replay
exactly to x with their required7/11 gates. The complete ordinary membership
recursion nevertheless rejects both. Thus the assertion

    every ordinary endpoint with a current defined forced step has
    an ordinary admissible forced predecessor

is `refuted`. This is a full-membership obstruction with an actual future
gate, separate from the nongated sign obstruction (3).

The lead oracle uses all three unique signed generator inverses, rejecting
negative or wrong-width parents and accepting only the prescribed root1.
It visits36 memo entries for the two targets, without using leading-core
pruning. A rejected node contributes no path; a positive inverse does not
automatically contribute an ordinary parent.

The independent Boolean oracle supplies the same complete36-node rejection
DAG, and the arithmetic verifier checks every node and parent edge. The two
targets share all projected prefixes through u,level8, and all eight of
those prefixes are ordinary, including28473 with rooted word utttttuu.
Thus no rejection by their unaged leading prefixes through level8 is
available. The initially reported16-bit-head compatibility labels are not
rejection certificates: u,level8 has15 bits, and the target's age4 is below
that core's stabilization age10. No aged-head shortcut is used.

Neither (3) nor (4) has a genuine three-return occurrence. Their original
complexity13 is below the u,decoder threshold18, and (4) has only two actual
branches. Consequently the proposed induction on sufficiently deep ordinary
endpoints with long observed decoder words is still unrefuted by these
examples. No finite experiment here is a proof of infinite termination.

## Execution audit and remaining obstruction

The independent arithmetic verifier agrees on all1392 source-product
head/state classifications, all eight supplied core histories and both
negative values in (3). It does not repeat the source-word search.

The record wrapper also retains the separate Boolean witness review and
its supplemental rejection DAG. The portable arithmetic verifier compares
all49 gate-search word rows, both full predecessor graphs and all eight
ordinary projected-prefix certificates, as well as the transfer checks
above. A separate adversarial mathematical review accepted the initial
states, reachable closure, arbitrary-tail sign statements and their
ordinary-versus-head scope distinctions.

The second raw JSON was edited after execution to clarify its gate scope.
Its new internal hash was computed with the original record hash still
inside the edited body. The verifier explicitly reverses those reporting
edits, recovers original run hash
78f0f5eecfd3e6e7a7003e70d2d4604bc25766234adc8e0249f8ef4e8c67dbea,
and verifies the edited body's nested hash. Neither source nor numerical
results changed. The wrapper preserves the received bytes and their own
hash; this is an explicit hash-format correction, not a silently ignored
provenance mismatch.

Records are `results/problem1/20260905_composed_inverse_primary.json` and
`results/problem1/20260905_composed_inverse_independent.json`. The former
contains five executed source/raw-data records with their original timings;
its own runtime is packaging only. To replay portably, extract the latter's
`source_text` to a Python file and run from the checkout root, optionally
setting RULE30_REPLAY_ROOT and RULE30_REPLAY_OUTPUT. No original temporary
files are required. The verification record includes source/input and result
hashes, full Git, software/hardware facts and atomic-write metadata through
its embedded writer; timestamps and timings naturally change on replay.
Fresh final four-file review accepted the checkpoint without corrections;
its isolated replay matched every independent summary and result field,
including both full predecessor graphs and the nested provenance hash.

The second Muse run exceeded the requested method scope: to recover already
available core histories it unnecessarily built root frontiers through
complexity10, and it enumerated suffix words of lengths through4 from the
existing core points instead of using only named membership certificates.
Its raw claims of no frontier construction or word scan are inaccurate.
That computation was stopped; no new frontier conclusions are adopted and
the independent work only replays the supplied words and product table.
The actual source test checked425 source words and105 outputs ending3
modulo4 before finding (3); this is not a search-order or global minimality
claim. The separate gate follow-up used49 words from one fixed81-word set,
with one eligible output. These executed scopes replace the inaccurate
descriptions while preserving the raw records.

The inverse-sign route now has an exact finite criterion and some positive
subfamilies. Three simplifying arguments fail in different scopes: general
leading-core positivity, ordinary positivity without a current gate, and
ordinary backward membership with a short valid continuation. None supplies
the required growing-word induction.

The remaining obstruction is precise (`inconclusive`): retain original phase
and complexity, the full ordinary membership predicate, and the long actual
admissible word simultaneously. A useful next step would be an all-depth
relation for the reachable inverse state conditioned on such a word and an
ordinary generator history, or a direct boundary-return exclusion. The
174-state SOURCE transfer does not track membership, and the16-state sign
machine does not track an unbounded forward schedule. Merely increasing a
head, frontier, suffix-word or decoder cap is not justified. The boundary-sum
route also still lacks a return-conditioned upper bound. B_all, signed
nonvanishing, actual return exclusion, and Problem1 remain open.
