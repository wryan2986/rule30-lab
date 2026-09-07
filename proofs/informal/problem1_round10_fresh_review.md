# Round-ten lead audit and the missing fresh external review

Status: `partial-proof` for the audited mathematical deductions below;
`refuted` for the scoped current-wait bound via the explicit counterfamily;
`finite-exhaustive` for the twelve named computational controls only.
NO fresh external adversarial review was completed. No claim has status
`rigorous-proof`, and Problem 1 remains OPEN. This file records the missing
verification honestly; its filename does not mean a reviewer accepted a proof.

## 1. Exact review provenance and failure boundary

The primary Muse contributor was thread 01a079fc-e3db-7d60-b020-d44d6e2fc3df.
It independently derived the scalar lift identity, explored the strip split,
and implemented the twelve controls. The lead corrected scope overclaims,
the local witness, and provenance details. Its successful corrected run at
04:14:49 UTC was followed by provider 429. The one paused contributor retry,
01a07a1c-fc5f-7841-8d55-db256cdb0955, failed with MissingSessionID. Neither
contributor thread is represented as a fresh main-proof reviewer.

The fresh Muse reviewer 01a07a0a-1bc7-7d21-8fc3-66773ab511fc ended with
provider 429. After a pause, the one retry
01a07a0e-efc3-7d40-aebf-88cba6266fd2 also ended with 429. Neither wrote a
review. The prescribed MiMo fallback
01a07a11-ebc6-7481-9430-ece38b783ad8 failed with HTTP 400: the request lacked
the provider's x-opencode-session routing metadata. A new MiMo session,
01a07a1e-912e-7793-8b8a-e29f34e10976, failed with the same error. All six
threads were closed. No native OpenAI/Codex reviewer was substituted.

An isolated request to the SAME configured opencode-go/mimo-v2.5 provider,
with one fresh session identifier and no configuration edit, was then
refused with HTTP 403, body `error code: 1010`. No review text was returned.
The exact credential-free request, attached source hashes, response and
runner bytes are in results/problem1/20260907_round10_mimo_direct_review.json;
the case-specific runner is experiments/problem1_nonperiodicity/review_round10_mimo.py.
This delegated only mathematical reading, with no simulation or new
scientific input. Provider hardware was not observable. The refusal ended
this access attempt; no access-control bypass was attempted.

One CLI endpoint-inspection command unexpectedly reported its automatic
Codex-launcher backup/shim refresh. The lead did not request a provider
configuration change, install a runner, change the research environment,
or edit the immutable reference. This incidental CLI maintenance is not
presented as part of the mathematical work.

The lead then completed essential local review and provenance corrections.
That work is described below, not relabeled as an independent external
review. A fresh authorized reviewer remains a verification task for the
next session, and this is not a claim of research blocked.

## 2. Scalar lift and physical renewal: independent lead derivation

For z=2y+a, projection sigma A^s z=A^s y is a direct bit identity.
If T=tau(y), it gives tau(z)>=T. At time T, the higher row is periodic.
On its p-cycle the scalar fiber map is a permutation at every phase exactly
when its low-bit drive is zero throughout. The full skew-product map on
those 2p states is then a permutation, so every extension is periodic at
time T. This proves tau(z)=T even if the scalar period doubles.

If a low 1 occurs, the return on the two scalar states contains a constant
factor. Its periodic response is unique. Before the first such factor,
two different bits stay different; after it they agree forever. The first
factor at offset rho acts on the update FROM time rho TO rho+1. Thus a
wrong lift has least delay rho+1, not rho. Adding the inherited T gives
the precise alternatives T and T+rho+1. This independently checks the
phase and the off-by-one in the contributor derivation.

For the physical source y=A Y_t, its least onset is max(tau_t-1,0).
Substitution gives tau_(t+1)=max(tau_t-1,0)+R_t, R_t>=0. The lift bit
is evaluated at inherited A-time T_t, so e_t is the actual bit at physical
position -T_t and time t+1+T_t. It is not generally the current center.

Doubling requires the permutation tail, so R_t=0. Imported FULL lateness
makes the source positive and the drop exactly one. At an EVEN doubling
with tau_t<=2, the next row has onset at most one; its A image is cyclic.
The next scan has drive (v,0), with a recurring 1 in v. Its unique
periodic low response is the CONSTANT 1, independent of phase. The actual
even boundary is 1, proving (8a) and preservation of the newly doubled
period. No statement about subsequent injections follows from this.

Finally max(tau_t-1,0)=tau_t-1[tau_t>0]. Finite summation yields the
budget identity exactly, including N=0. Every doubling consumes one
positive-delay step; hence the injection sum dominates D_N-tau_0.
Clock growth and finiteness of each R_t force infinitely many injections,
but a sequence of finite bounded injections can have an infinite sum.
This is the precise reason the identity does not exclude bounded lag.

Disposition: accepted by the lead at `partial-proof` scope. Fresh external
review is missing; no unbounded-lag or anchored-activity conclusion is accepted.

## 3. Shift tower and highest wait: finite-to-infinite audit

The cyclic zero-extension contradiction uses full-code injectivity, not a
bounded experiment. If all 2^k v were cyclic for a positive finite v,
their widths would escape every finite set of bounded-period cycle states.
The one-bit preserve-or-double classification forces a doubling. At that
source the low trace is zero. The next extension has code (b,0), with b
visiting both bits, and the next zero extension obeys w'=b OR w from w=0.
It is eventually 1 and cannot be purely periodic. This contradicts the
all-cyclic tower. The excluded v=0 case would indeed be a counterexample
if positivity were omitted.

The preperiods tau(2^n x) are nondecreasing by spatial deletion. If bounded
by H, every A^H image is cyclic. For n>=2H, the EXACT identity
A^H(2^n x)=2^(n-2H)T^H(x) supplies an all-cyclic tower for ONE positive
finite integer T^H(x). Injectivity of T prevents zero. Section 1's
contradiction applies, proving divergence with no asserted rate. No
infinite-state pigeonhole principle or interchange of limits is used.

For y_n=2^n*7, deleting n low bits gives 7 and deleting them from its
phase-correct cycle mate gives 6. Their highest disagreement is exactly n,
and the common next bit is 1. The first erasing wait is one for every n,
whereas the full preperiod diverges by the preceding argument. Therefore
no universal FINITE-valued f can bound tau by f of that one wait. This
is an explicit all-depth counterfamily, not a numerical extrapolation.

The physical-time comparison is crucial: the actual row is A^n(2^n*7),
whose onset is max(tau(2^n*7)-n,0). Divergence of the first term says
nothing about this difference. No FULL orbit or actual-lag divergence
has been exhibited.

For the erasure sum, an erased highest bit cannot be recreated by lower
differences. Each stage has a finite wait by the periodic projected-tail
lemma, and then its highest index strictly decreases. There are finitely
many stages. The current highest bit still differs at every time before
its erasing update, so coalescence does not occur earlier than the summed
waits. The empty initial disagreement set gives the empty sum zero. Later
waits must be recalculated on the evolved row; they are not all asserted
to equal one in the counterfamily.

Disposition: accepted by the lead at the stated `partial-proof`/`refuted`
scopes. Fresh external review remains missing. The counterfamily closes
only the proposed scalar local bound, not the actual future-driver route.

## 4. Conditional one-bit strip: return maps and past phases

The hypothesis bounds ALL sufficiently late physical preperiods by one.
Bit-depth transport is needed to deduce that late disagreements occupy
only the center bit. A single tau=1 row does not suffice. At a noncyclic
even row the actual low pair is 3 and its cycle mate's low pair is 2.
Its code is periodic from time one, so shifting by two gives a pure drive.

For a t gate, one full drive period ends in the symbols 2,1. The return
ends in H_1 H_2, which is constant 2. The actual starting state 3 differs,
but every H_i merges 2 and 3 immediately. The least next onset is one.
The period-one case is impossible here because both 2 and 1 occur.

For a u gate, the next actual gate is t by no-uu; hence the first driving
symbol b_2 is 2. A {0,2} drive keeps start 3 recurrent. In the resetting
case the period is at least two and its return ends in H_2 H_2, with
image {1,3}. A wrong periodic start would be 1. The first H_2 keeps the
two starts different, giving next onset at least two, which the global
bound forbids. Thus the next even row is cyclic. This proves the two
transition laws without assuming a finite quotient.

No five t gates occur consecutively, so each lag-one episode ends after
at most five even rows, at the u-source successor. Periodic-source births
are still unclassified and may start more episodes.

For the past constraint, complete the codes periodically before using
negative temporal subscripts. The identity Phi u=shift^2 v is a direct
cycle completion of the actual bridge, with the SAME prior actual row.
On {0,2}, g00=0, g02=2, g20=3, g22=1. If the predecessor were cyclic,
v0=3 would force u_-2,u_-1=2,0 and then v1=2, i.e. an adjacent u gate.
This is forbidden. Its predecessor lag is thus one and its gate t;
v0=2 now forces u_-2,u_-1=0,2. Together with u0,u1,u2=2 this gives
exactly 02222 at phases -2..2. These are phases of a pure periodic code,
not negative actual physical times. It follows that a doubling episode
contains between two and five lag-one even rows. No existence assertion
for a finite cycle with that pattern is made.

Disposition: accepted by the lead at `partial-proof` scope only. The
missing external review is particularly relevant here because this final
return/past argument was derived entirely by the lead.

## 5. Fixed verification and archival qualifications

The only scientific controls are y in {0,2,3,6,7,12}, a in {0,1}.
Two separate orbit algorithms (integer/dictionary and tuple-cell/list
recurrence) agree on all twelve full finite trajectories and repeat states.
All sixteen hand-derived transitions are checked. The checker separates
first cycle entry from phase-correct completion and tests the lift choice
at inherited A-time T. Its current run enforces a 60-second wall cap,
128-MiB address-space cap, orbit caps and fixed-cell padding assertions.

All superseded runs are retained byte-for-byte as snapshots. The initial
checker only reported resource caps; a corrected version enforces them.
The last direct lead launch passed all mathematics but reported an
inherited launcher peak RSS of 199.297 MiB, so caps_ok was FALSE. That
failed record is snapshot4, not discarded. Launching the unchanged
checker from a small Python parent produced the final all-pass record
under the same 128-MiB cap. The exact wrapper command was:

    python3 - <<'PY'
    import subprocess,sys
    raise SystemExit(subprocess.run([sys.executable,
        'experiments/problem1_nonperiodicity/check_round10_delay_renewal.py'],
        check=False).returncode)
    PY

The twelve-control checks verify the scalar formulas, not the all-depth
shift tower, one-bit-strip return law, or the sidecar's general K witness.
Those remain hand proofs with the lead audit above and missing fresh
external review. All runs kept the same scientific inputs. No larger
prefix, period, lag, width, nilpotent-word or source family was searched.
