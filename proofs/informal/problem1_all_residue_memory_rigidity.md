# Rigidity at every finite residue memory

Status: `partial-proof` for the structural all-memory theorem; `refuted`
for the fixed finite-residue-memory universal additive class below;
`finite-exhaustive` for the small independent controls. Fresh Muse review
returned provider429; the lead checked the proof and separate arithmetic
formulations locally. No width sweep or larger rank calculation is used.
Problem1 remains open.
Base: `103579dee7ed81ffea9aae794c86c4893f37603d`.

Round-1 audit addition (2026-09-06):
`problem1_all_memory_triangular_review.md` expands the all-bit slice
bijection, circulation sign and fiber argument, and closes the requested
memory using the explicit rational survivor -7/127. These clarify this
same theorem; no class or experiment is enlarged. The fresh full external
review limitation is retained unless separately discharged in the handoff.

## Quantified target and admission

For every finite b and either ordinary phase root, consider real weights
omega(q mod2^b,g) on original-prefix residue and generator g in{t,u,p}.
The question is whether a weight bounded below over ALL finite ordinary
words can strictly decrease on every prescribed ututut block beginning
at an endpoint50055 modulo65536. This fixes the previously closed16-bit
sublanguage, not a boundary condition at every larger memory.

The proved answer is no for EVERY finite b. The original admission was:
failure of any new identity
would invalidate this generalization and leave only the established b=4
theorem. If the identities and structural proof hold, no larger residue
memory or rank census is justified for this universal additive route.

Admit only the64 small section cases v=0..15,s=0..3; low-bit rotation
controls y=0..63; and the uniform-fiber identity at (b,r)=(2,2),(4,3).
The deliberately too-early case (4,2) is a falsification control for
omitting the condition2r-2>=b. Compare packed arithmetic to independent
cell generators and literal scanner iteration. No ordinary frontier,
new occurrence, wider graph, coefficient search or solver run is admitted.
Local CPU120s, wall180s,1GiB; atomic records with exact inputs, full Git,
sources, hashes, software/hardware and timing. These finite controls do
not prove the all-b theorem; its proof is the algebra below.

## 1. All finite residue graphs are controllable

The generators are permutations modulo every power of2 by bit
triangularity. The exact relations are

    P(T^-1(y)) = 4*(y>>2)+((y-1) mod4),                       (1)
    (T(4v+s)>>2) = G_(S_s)(v),  S=(t,u,p,p).                 (2)

For (1), P(x)=T(x) XOR1 XOR(2 if x is even else0), and T preserves
parity. Thus PT^-1 rotates the two low bits through all four values
and leaves the higher bits fixed. Equation (2) is the four low-bit
sections of T, equivalently A(4v+s)=G_(S_s)(v).

Suppose a function f on residues modulo2^m is invariant under T,U,P.
For m>=2, (1) implies f(4v+s)=h(v), independent of s. Applying T and
using (2) shows h(G_(S_s)(v))=h(v) for every s. Hence h is invariant
under the same three generators modulo2^(m-2). Induction gives constant
f; the m=0 base is trivial and m=1 follows from U toggling the low bit.

The set reachable from ANY chosen root is nonempty and forward closed
under each generator. Since the graph is finite and each generator is
injective, each maps this set onto itself; its indicator is invariant.
It must be the full graph. Therefore every vertex is reachable from every
other vertex at EVERY finite bit width. No finite controllability census
is extrapolated in this argument.

Equation (2) also gives the local scanner intertwining identity

    A(G_g(q)) = G_(S_(G_g(q) mod4))(A(q)).                    (3)

Both phase roots,1 and3, are fixed by A, so literal scanner iteration
retains each root. Equation (3) itself holds at arbitrary prefix states.

## 2. Universal strict decrease forces a scanner coboundary

It suffices to consider b>=4: smaller memories embed by ignoring the
extra residue bits. On residues modulo2^(b+12), let

    d_6(q,g)=omega(A^6(q) mod2^b,S_(A^5(G_g(q)) mod4))
             -omega(q mod2^b,g).                            (4)

This is the complete ORIGINAL-position scalar change after six scanner
passes. The six birth costs depend only on the accepting terminal
residue, by the already proved fixed-age pullback. Accepting residues
are exactly those50055 modulo65536. All graph vertices are reachable
from either root and can reach this nonempty acceptance set, by section1.

Put flow1 on every t and u edge and flow2 on every p edge. This is a
strictly positive circulation. Fixing the lower12 input bits and varying
the upper b bits makes A^6(q) mod2^b uniform by triangularity. For each
input generator the emitted letters have lower-input counts1024,1024,2048.
Thus the count-vector identity C_t+C_u+2C_p=0 from the sixteen-state note
holds at EVERY residue r modulo2^b with the same per-residue triples.
In particular the total d_6 weight of this positive flow is0 for all omega.

If omega has universal strict accepted-block descent, no graph cycle can
have positive d_6 weight: pump it inside an accepted path, keeping the
terminal birth cost fixed. Subtracting a small multiple of any chosen
cycle from the positive zero-weight circulation forces that cycle's weight
to be0, as before. Hence every cycle has weight0. Path sums in this finite
strongly connected graph are endpoint differences: there is a real
function psi on residues modulo2^(b+12) with

    d_6(q,g)=psi(q)-psi(G_g(q)).                             (5)

This step uses universal strict descent over all finite initial histories,
not an infinite forward orbit and not a claim about actual critical cuts.

## 3. Iterate the PURE scanner, not forced continuation

For n>=1 put r=6n and

    Psi_n(q)=sum_(j=0..n-1) psi(A^(6j)(q)).

Equation (3) permits applying (5) to successive transformed edges. The
intermediate costs cancel, giving the exact identity

    omega(A^r(q) mod2^b,S_(A^(r-1)(G_g(q)) mod4))
      -omega(q mod2^b,g) = Psi_n(q)-Psi_n(G_g(q)).           (6)

It is well-defined modulo2^(b+2r). These are iterations of H alone, with
no appended birth letters or prescribed gates. ONLY the original six
actual branches were assumed; no6n-step forced orbit is asserted.

## 4. Uniform lifts erase the original edge in expectation

Choose the multiple r=6n large enough that2r-2>=b. Fix ANY original
residue q0 modulo2^b and any input generator g. Lift q0 uniformly to
residues q modulo2^(b+2r).

Condition on the lower2r input bits. The upper b free bits map
bijectively to A^r(q) mod2^b, independently of the emitted letter.
Within those lower2r bits, condition on the bits below position2r-2.
The two remaining bits are free because2r-2>=b. By triangularity of
A^(r-1)G_g, they map bijectively to its two low output bits. Therefore
the joint distribution of transformed prefix and emitted letter is

    uniform on2^b residues, independently of
    letter probabilities (t,u,p)=(1/4,1/4,1/2),             (7)

independently of q0 and g. The averaging is a finite exact identity at
each fixed b,r, not an asymptotic mixing assumption. The inequality
2r-2>=b is load-bearing; (b,r)=(4,2) need not satisfy (7).

Let

    c=(sum_q [omega(q,t)+omega(q,u)+2omega(q,p)])/(4*2^b).

The average transformed edge cost in (6) is c for EVERY original edge.
Now take any directed cycle in the original2^b-state graph. Lift each
of its edges with equal weight1/2^(2r) on all of its higher-bit lifts.
This is a circulation: each G_g maps a source fiber bijectively onto the
corresponding destination fiber, so conservation lifts vertex by vertex.
The sum of the coboundary on the right of (6) is0. Applying (7) gives

    sum_(edges of original cycle) omega = c*cycle length.   (8)

Every cycle satisfies (8). Strong connectivity then gives a vertex
function phi with

    omega(q,g)=c+phi(q)-phi(G_g(q) mod2^b).                  (9)

This proves rigidity for EVERY finite b, without a rank calculation at
any new width. The b=4 determinant1 is an independent finite consistency
check, not a premise replacing the all-b argument.

## 5. Close the endpoints at the requested memory

For (9), boundedness below over ALL ordinary word lengths forces c>=0.
For b>4, a50055-mod65536 input need not give equal initial and final
residues modulo2^b; that cancellation must NOT be assumed.

Instead use the established schedule-survivor existence theorem in
`problem1_period_two_schedule_survivor.md`, section3. The periodic branch
schedule(ut)^infinity has a unique2-adic survivor X. Shifting two places
does not change its schedule, so uniqueness gives F^2(X)=X, hence F^6(X)=X.
The six initial branches give X=903 mod16384. The verified four-class
terminal table then forces X=50055 mod65536: it is the only one of
those classes with F^6(X)=7 mod16, as required by the initial u gate.

For this b choose the residue a=X mod2^(b+12). By all-width
controllability there exists a FINITE ordinary word from the chosen
phase root whose endpoint x is a modulo2^(b+12). It has the six actual
branches ututut and lies in the fixed50055-mod65536 sublanguage. The
twelve-bit loss bound gives

    F^6(x)=F^6(X)=X=x modulo2^b.

Thus the two phi terms cancel on THIS finite witness, and its prescribed
block change is6c>=0, contradicting universal strict decrease. This does
not make X ordinary, does not give x an infinite forced continuation,
and supplies no uniform bound on the witness word length.

The no-go therefore covers BOTH phase roots and EVERY finite
residue memory. It does not cover an arbitrary finite automaton on
history words, age-dependent weights, a nonlinear potential, or a
restriction coupling elapsed age to original length. Actual-return
exclusion, the whole-tail conjecture and Problem1 remain open.

## 6. Independent finite-congruence derivation of the closed residue

The witness-residue step can also be proved without appealing to an
infinite survivor. Let C=B_u B_t B_u B_t B_u B_t, with the inverse zero
branches from the schedule-survivor note. C increases2-adic agreement by
twelve bits and maps a3-mod4 terminal value into the six-gate cylinder.
Modulo any2^m, repeated application starting at3 becomes fixed after
finitely many iterations, since the valuation of successive differences
increases by twelve each time. Let a=C(a) modulo2^m be the resulting
residue, m=b+12>=16.

The exact identity F^6(C(a))=a and the twelve-bit precision-loss bound
give F^6(a)=a modulo2^b. Its six branches and this equality modulo16
again force a=50055 modulo65536. Controllability then supplies the same
kind of finite ordinary lift x. This finite-congruence argument and the
periodic-survivor argument prove existence of a residue at EACH requested
memory; neither asserts that the residue representative a itself is
ordinary or that one finite x works for all memories.

## 7. Quantifiers, controls and provenance

Precisely: for EVERY finite b, EVERY phase a in{p,u}, and EVERY real
weight table omega on old residues modulo2^b and generators, if W_omega
has one lower bound over ALL finite ordinary words from rho_a, then
there EXISTS a finite ordinary word w with endpoint x=50055 mod65536
whose prescribed six-step ututut block has nonnegative cost change.
The word may depend on b, a and omega; no common word or length bound
is asserted. The proof is by contradiction through rigidity, not by
enumerating such counterexamples.

The independent controls agree on64 section identities,64 low-rotation
identities,60 uniform-fiber groups and3264 individual lifted edges.
Literal cell/scanner iteration verifies9632 local intertwining steps,
including the deliberate too-early control. At b=4,r=2,q0=0,g=t, all16
lifts emit t, whereas unrestricted averaging would predict letter counts
(4,4,8). Thus dropping2r-2>=b is `refuted`; the proof above retains it
and reaches the required age through PURE scanner iteration. No longer
actual forced word is inferred.

Records: `results/problem1/20260906_all_memory_{primary,independent}.json`.
The primary retains the admission snapshot and exact packed controls;
the independent implementation uses cell arithmetic, a different inverse-
bit recurrence, and literal scanner iteration. Source/input hashes, full
Git, exact parameters, hardware/software and timings are retained, with
atomic writes. The largest small-control modulus is1024, below the
already used65536-state graph; no new graph or rank sweep ran. The
2-adic inverse/survivor dependency and the four-class terminal table are
linked by exact input hashes.

A seventh fresh Muse proof-review attempt returned provider429, after
the six old errored threads were closed to clear the concurrency limit.
No model substitution or successful fresh external proof review is
claimed. The lead checked both reachability/section induction and the
uniform lifted-cycle argument, and derived the needed closed residue
both through a periodic survivor and finite inverse-branch iteration.
An eighth final adversarial Muse request in the next goal continuation
also terminated with provider429. The exact terminal status and the
fresh-verification/context handoff are recorded at the top of
ASTRA_HANDOFF.md. No new mathematical computation followed that failure.

The next research step must retain an additional restriction that this
universal class discards: prescribed age relative to ORIGINAL length,
actual near-boundary return information, or a genuinely different
nonlinear/word-state observable. Merely adding more finite residue bits
to a fixed additive potential is now ruled out at every width. This
does not preclude an arbitrary finite automaton on history words or
prove any statement about eventual periodicity of the actual center.
