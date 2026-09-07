# Round-8 lag sidecar: isolated-scan nonforcing with permitted heads

Status: constructive isolated-step lemma `partial-proof` (hand derivation, no machine run);
orbit-level bounded-preperiod question `inconclusive`; Problem 1 open.
Superseded as an isolated construction by the lead main note
`problem1_bounded_lag_doubling_controls.md` (stronger finite-entry plus actual
D_0 = D_1 = D_2 controls); the scoped isolated-step nonforcing result below is
preserved and no further routes are added here.
Authorization: Round 8 via ASTRA_GOAL delegation; exclusive ownership of this file only.
No experiments run, no census used, no commits made. Lead independently studies
full-boundary reset cones; this note covers only the sidecar question below.

## 0. Exact question

For an infinite permitted G-orbit C_(m+1) = I_3 shift^2 C_m with gate values
C_m(0) = 3 and C_m(1), C_m(2) in {1,2}, with least preperiods T_m and least
eventual periods p_m: does sup_m T_m < infinity force sup_m p_m < infinity?
This note answers only the isolated-step version: a single G-step with these
gate heads admits no period-dependent lower bound on its output onset.
Whether the whole recursion forces the orbit-level implication is untouched:
joint head compatibility across steps could still do so.

Imported (not re-derived): H-table H_0=[0,1,3,3], H_1=[3,2,2,2],
H_2=[2,3,1,1], H_3=[1,0,0,0]; exact reset language; period alternatives
(p or 2p by even/odd swap count); Phi I_a = identity. Write Gs = I_3 shift^2 s.

## 1. Constructive lemma (`partial-proof`)

Lemma A ({0,2} doubling). For every P >= 1, let u = "2" if P = 1, else a
length-P word with a single 2 (e.g. at index 1) and 0 elsewhere; u has least
period P with exactly one 2 (a smaller period would repeat the single 2 at two
distinct residues mod P). Put drive b = (1,2,u^infinity) and source
s = (3,2,b), i.e. s = (3,2,1,2,u^infinity). Then s is permitted
(s_0,s_1,s_2) = (3,2,1), has preperiod <= 4 (s_4.. = u^infinity) and eventual
period P; and c = Gs = I_3 b satisfies c_0 = 3, c_1 = H_1(3) = 2,
c_2 = H_2(2) = 1, so output gate (3,2,1) is permitted. The scan sits in the
{1,3} pair from t = 2 while the drive is P-periodic from t = 2; every length-P
drive window is a cyclic shift of u with odd 2-count, hence a swap (0 is the
identity and 2 the swap on {1,3}). Thus c_{t+P} = swap(c_t), c_{t+2P} = c_t
for t >= 2: onset <= 2. Phi c = b has least eventual period P, making P divide the least eventual period q of c, while the available 2P period makes q divide 2P; the swap excludes q = P, so q is exactly 2P.

Lemma B ({0,3} doubling). For every P >= 1, let v = "3" if P = 1, else a
length-P word with a single 3 at index 0; v has least period P with one 3.
Put b = (2,0,v^infinity) and s = (3,2,b) = (3,2,2,0,v^infinity). Then s is
permitted with head (3,2,2), preperiod <= 4, eventual period P; and c = Gs
satisfies c_0 = 3, c_1 = H_2(3) = 1, c_2 = H_0(1) = 1, output gate (3,1,1).
The output already lies in the recurrent {0,1} pair at t = 1 (state 1), with
c_2 = 1 in the pair and the drive periodic from index 2, so c is 2P-periodic
from onset <= 2 by the odd-3-count swap (0 identity, 3 swap on {0,1}). Phi c = b makes P divide the least eventual period q of c, while the available 2P period makes q divide 2P; the swap excludes q = P, so q is exactly 2P. No onset-3 claim is made; no head-3 entry
argument is used.

These are two gate heads only -- (3,2,1) doubling through {0,2} and (3,1,1)
doubling through {0,3}. No third head and no finite-entry claim are made.

## 2. Isolated-step interpretation

With e_t = [c_t != c_{t+2P}] against the output's own least period 2P, mismatches are confined to t < 2 while 2P is arbitrary (against the input-period shift, c_{t+P} != c_t holds at every tail time t >= 2 by the swap): the swap return is a permutation with
no internal transient, and the gate-permitted drive heads supply exactly the
symbols for pair entry at or before t = 2. Hence the scan/reset/gate lemmas
supply no period-dependent lower bound for the onset of an isolated G-step
with these output heads. That is the whole content: it does not show the
lemmas cannot prove an orbit-level theorem, since the whole recursion -- joint
compatibility of heads (C_m(2), C_m(3)) across all steps -- could still force
bounded periods from bounded preperiods. No infinite orbit is constructed here.
The established infinitely-many-positive-lags count is untouched.

## 3. Dependencies and limitations

Depends on: H-table; reset-language theorem and parity-doubling alternatives;
permitted-gate values; Phi conjugacy for least-period divisibility. Lead
checked the corrected isolated identities; the fresh adversarial review
applies to the stronger main note, not this superseded memo. Limitations:
single G-steps only; source
preperiods <= 4 are available (not least) bounds; says nothing about lag
density, unbounded lag heights, or full-boundary reset cones.
