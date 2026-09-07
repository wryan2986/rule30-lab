# Finite sources with one-step delay, and a refuted symbolic supply

Status: Lemmas 1-2 and the conditional 222 construction (Sec 3) are
`partial-proof` (hand derivations, no sweep). The x=7 instance is hand-verified
exact arithmetic. The k2 Phi-nilpotence chain (Sec 4) is an independent hand
certificate (`partial-proof`). The k3 word verdict (Sec 5) is
`finite-exhaustive`: exactly one fixed 8-word orbit decided by two agreeing
implementations with atomic provenance. The universal one-hole nilpotence
proposal is `refuted` by that certificate. No positive all-k conclusion follows.
Problem 1 remains OPEN. No sweep, census, horizon extension, or doubling-index
extraction was run.

## 0. Admission, corrections and a rejected proposal

The question is whether the round-eight local bounded-lag family can be
made initially finite at arbitrarily large source periods. A construction
would close initially finite support as a proposed local discriminator;
a failure would identify an additional supply condition. The conditional
construction below is exact. Its unbounded-period supply remains unproved.

(a) v1 correction retained: 2^infty IS a finite A-cycle code, Theta(6)=2^infty
since A(6)=1 XOR (3 OR 6)=6. The K_z=1 refutation is scoped to z<4 (only z=3).
(b) Prefix-solve check retained: D triple gives x=7 mod 64; b_3=0 extends to
x=135 mod 256 with A(135)=230, A(230)=206, A(206)=220, whose residues mod4
are respectively2,2,0. These are fixed hand checks, not a source search.
(c) REJECTED proposal (lead fence): the v2 idea of extracting z bitstrings at
the first three doubling indices is explicitly rejected by the lead. It would be
a restart period/candidate census extract and cannot settle the unbounded
property. It is not run and not proposed. The only admitted computation is the
single fixed k3 word test in Sec 5. The lead's global fixed-strip reduction and
the cycle-completion defect-transport note are separate work; neither is
duplicated here.
(d) The preliminary T-inverse side calculation used an incorrect low
constant111 for T^4x (the corrected constant is119). That bypassed claim
is removed from the accepted derivation, rather than used as a dependency.
The original source and record are preserved in the superseded-run archive.

## 1. Finite-x criterion (partial-proof, retained)

Lemma 1. x finite iff Phi^N(Theta(x))=0^infty for some N; nonzero finite-support
words are Phi-immortal (last-nonzero frozen via g(0,0)=0, g(a,0)=3).
Proof. Theta(pi^N x)=Phi^N Theta(x) and Theta is injective, with Theta(0)=0.
For a finite temporal word whose last nonzero time isM, Phi produces3 atM
and zero afterwards; hence no iterate can kill it.
Lemma 2. For s=(prefix_h,u), u=Theta(z) finite, shift^h s=u, with
K_z=min{K:pi^K z=0}: w=Phi^{K_z}(s) lives in 0..h-1, and x is finite iff w=0.
Round 8 has h=4. Doubling-index phase-correct u/z are unique per index.
Here x=Theta^-1(s), and "u=Theta(z) finite" means z is a finite integer,
not that u is eventually zero. To prove Lemma2, commute shift^h past
Phi^{K_z}. The tail vanishes because pi^{K_z}z=0. If the remaining word
is nonzero, Lemma1 prevents its ever vanishing; if zero, x is finite already.

## 2. Scoping for the h=4 prefix s=(3,2,2,0,u) (corrected, retained)

Phi(s)=(1,1,3,g(0,u_0),Phi(u)_0,...). For K_z=1 (finite periodic doubling: only
z=3, u=3^infty) w is nonzero finite-support, so x is infinite. This does
not decide the prefix family for larger K_z. The next construction avoids
any assumption that finite entry or an arbitrary temporal prefix preserves
initial finiteness.

## 3. Finite-source doubling under cyclic 222 (partial-proof; x=7 exact)

Identity: A(4k+2)=A(4k+3) for all k (same >>2 and >>1, bit-0 masked in the OR).
Here k is nonnegative; the finite case is all that is used.
Theorem. Let z be finite A-periodic with u purely periodic over {0,2}, odd 2s
per least period p, and cyclic 222 somewhere mod p. Rebase z'=A^i z there and put
x=z'+1. With zero right half: Theta(x)=(3,u'_1,...), tau=1 exactly, period p;
c=I_3(shift^2 Theta(x)) is the ACTUAL Theta(X_1), starts in {1,3}, tau=0, least
period 2p; D_0=D_1=D_2=3 from head (3,2,2). Lags (1,0).

Proof. Since z' mod4=2, adding1 changes only its low bit, so x is finite
and A(x)=A(z'). Thus Theta(x) differs from the purely periodic rotated
code only at time0, where its3 is outside {0,2}. This proves LEAST onset1
and eventual periodp. Its head(3,2,2) gives all three actual D values by
the original I_0 calculation. In particular D_1=3, together with the
full-fringe bridge, identifies the actual time-two code with the stated c.
The drive shift^2 Theta(x) is purely periodic over{0,2}; c starts at3 in
the invariant pair{1,3}, where0 fixes and2 swaps. The odd count makes
c_(t+p) the other pair member and c_(t+2p)=c_t for EVERY t>=0. Hence c
is purely periodic. Phi(c)=shift^2 Theta(x) makes p divide its least
period, and the available2p makes that period divide2p. The swap excludesp,
so the least period is exactly2p. No D_m for m>=3 is claimed.
Instance: z=6, u=2^infty, x=7, F(7)=27 with A(27)=25, A(25)=27. Finite seed at
p=1. The construction selects {0,2} type; no {0,3} analogue claimed. Unbounded
222 occurrence is NOT claimed (short odd words like (2,0) lack 222).

## 4. One-hole supply: hand g-table and k2 certificate (partial-proof)

Phi uses g(a,b)=(r,s), r=b_0 XOR (a_0 OR a_1), s=b_1 XOR (a_1 OR r), value r+2s
with (low,high) bits. Hand-derived rows, inputs 0..3:
g_0=[0,3,2,1], g_1=[3,0,1,2], g_2=[3,2,1,0], g_3=[3,2,1,0].
(Caution: the lookalike rows [0,3,2,1],[1,2,3,0],[3,2,1,0],[3,2,1,0] in the
fringe note are the scan map h, not g; the audit here uses g throughout.)

k2 word u=(2,2,2,0)^infty, least period 4, three 2s (odd), 222 cyclically.
Independent hand re-derivation, each step (Phi w)_t=g(w_t,w_{t+1}) cyclically:
2220->1132->0212->2213->1221->1120->0133->3203->1310->2233->1001->3030->3131
->2222->1111->0000 (15 steps, every transition re-derived from the rows above).
Hence Phi-nilpotent of index15: z=Theta^{-1}(u) is finite on an A-cycle.
Its base-four digits, low first, are the first symbols in the displayed
chain beforezero:

    (2,1,0,2,1,1,0,3,1,2,1,3,3,2,1).

Their sum is z=467256710, of bit length29. The cycle has least period4
by full-code injectivity. Section3 gives x=z+1=467256711. With cyclic222,
Sec 3 yields a
finite source with tau 1, successor tau 0 doubling 4->8, D triple 3. Second rung
after x=7 (p=1). k1 word (2,0)^infty is Phi-nilpotent (20->32->10->33->00) hence
finite, but has no cyclic 222, so Sec 3 does not apply to it.

## 5. k3 verdict: one-hole supply blocked at k=3 (finite-exhaustive)

Candidate u=(2^7 0)^infty, period 8, seven 2s (odd), 222 present. Hand Phi steps:
22222220 -> 11111132 -> 00000212 -> 00002213 -> 00021223 -> 00221103 -> 02120313
-> ... (6 steps verified; step two ends in 0212 on an 8-word with wraparound
coupling, so no length-halving induction follows). Hand algebra does not settle
nilpotence (orbit in 4^8=65536 words).

Admission was stated by the lead before execution: nilpotence would supply
a finite 222 period-8 cycle hence a Sec-3 control at 8->16; a nonzero repeat
refutes the one-hole all-k supply at k3 while retaining Sec 3 conditionally.
Nilpotence would leave the positive all-k implication unproved. A checked
nonzero repeat does prove this one word never reacheszero, by determinism;
it therefore refutes the universal proposal, without solving Problem1.

Single authorized test, executed after the hand order above. Two independent
implementations (bit-formula vs hand-table literal, 16/16 pairs agree) ran the
fixed 8-word orbit with cap 65536 each, local single thread: BOTH agree on
repeat_nonzero, first repeat word 03033003 first seen at step 286, repeated at
step818, a cycle of length532. All intervening words are nonzero. The
initial run's incomplete provenance was archived before correction at
results/problem1/20260907_round9_superseded_run.json. The SAME input was
then reverified with separate tuple/bit-formula and string/literal-table
representations and separate orbit loops. They agree on the entire819-word
trajectory, including the final repetition. Both also verify the21 frozen
hand transitions above and all16 local g values. Corrected numeric timings,
measured peak memory, enforced120-second/256-MiB limits, complete trajectory,
source bytes, full Git, immutable reference and hashes are in atomic provenance:
results/problem1/20260907_round9_one_hole_control.json (experiment_id
round9_one_hole_control_k3_corrected_verification, full git 28f5570d622ceb50bcd5b9e2f78d9c579e2ed419,
reference SHA 358bdc07..., hardware/software/timings/hashes inside), written via
tmp+fsync+replace by experiments/problem1_nonperiodicity/check_round9_one_hole_control.py.
Outcome: the exact one-hole family u_k=(2^(2^k-1) 0)^infty is BLOCKED at k=3
(refuted as an all-k supply). The Sec3 conditional theorem and its verified
finite-source cases p=1 and p=4 stand. The failed k3 word, despite having
odd2-count and222, does not code a finite integer. No additional undecided
k value was tested. The unbounded-period222 supply remains `inconclusive`;
failure at k3 says nothing about which later family members might die.

Dependencies: full-fringe Secs 1-4, reset-language Sec 2, doubling-lag Secs 1-3,
anchored-entry Secs 1-3, sparse-codes Secs 1-2, gate-bridge Sec2. Review and
lead acceptance are recorded separately in the round-nine handoff and audit.
