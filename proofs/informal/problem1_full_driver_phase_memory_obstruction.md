# The complete cyclic driver and its next phase map do not close

Status: `refuted` for the precisely stated summary update below;
`partial-proof` for its algebraic derivation and scope. The fixed verification
has status `finite-exhaustive` only on its declared inputs. This is a lead
derivation, with fresh external review missing. Problem 1 remains OPEN.

## 0. Admission and distinction from the earlier observation no-go

Round304 constructs a single global cycle shadow from the ORIGINAL finite
row and identifies two bits of transient phase information for one spatial
extension. The next question is whether those bits can be transported when
the ENTIRE cyclic driver is retained, together with the exact least delay.
A positive update would replace repeated access to the original transient
by a precise recurrence for the shadow used in the FULL crossing argument.
A negative answer identifies information which that recurrence loses.

This differs from the round303 finite-observation question: the summary
tested here contains the whole finite integer cyc(y), hence its entire
periodic A-orbit of possibly unbounded period. It is not a finite-state
ansatz. The question is still about sufficiency of a specified summary,
not about existence of every possible compression.

Routes ranked `heuristic`: first falsify this exact full-driver update;
then seek a transport identity retaining the full transient; do not enlarge
a local observer or enumerate more periodic words. The single pair below
is obtained by hand from A(110)=A(112)=100. No source search is needed.

## 1. Exact proposed state and claim (`refuted`)

Let A(y)=(y>>2) XOR ((y>>1) OR y), for finite y>=0. Use the imported
least delay tau(y) and PHASE-CORRECT cyc(y). Define the COMPLETE one-bit
phase map

    F_y(a)=bit_0(cyc(2y+a)), a in {0,1}.             (1)

Deletion commutes with cycle completion, so

    cyc(2y+a)=2cyc(y)+F_y(a).                        (2)

Every Boolean one-input map is affine over GF(2); thus write
F_y(a)=eta_y*a XOR theta_y, with theta_y=F_y(0) and
eta_y=F_y(0) XOR F_y(1). This definition also covers a RESETTING cyclic
driver, where F_y is constant. When the cyclic low trace is always zero,
these are exactly the two bits of round304's transient phase formula.

The proposed summary is

    S(y)=(cyc(y), tau(y), F_y(0), F_y(1)).           (3)

The claim under test is existence of a function H such that, for EVERY
finite y and a in {0,1},

    F_(2y+a)=H(S(y),a).                             (4)

The same counterexample refutes the weaker request to determine only
F_(2y)(0), with the next TWO original attached bits fixed to zero.
It also refutes updating the full S state. Including the least eventual
period adds no information to (3), since the full cyc(y) determines it.

## 2. A hand certificate with the same core AND the same delay

The fixed core cycle and two immediate preimages are

    100 ->111 ->100,
    110 ->100, 112 ->100.                           (5)

For example A(110)=27 XOR127=100 and
A(112)=28 XOR120=100. Hence

    cyc(110)=cyc(112)=111,
    tau(110)=tau(112)=1, p(110)=p(112)=2.            (6)

The pure low trace of111 contains a1. The resetting-lift theorem gives
only ONE cyclic one-bit lift at each phase. Its core is222, as certified by

    222 ->200 ->222.                                (7)

Consequently both F_110 and F_112 are the constant-zero map, independently
of their transient and of the appended bit. Thus

    S(110)=S(112)=(111,1,0,0).                       (8)

Now attach the SAME actual zero bit. The child words are220 and224.
Their exact transient certificates are

    220 ->201 ->223 ->200 ->222 ->200,
    224 ->200 ->222 ->200.                          (9)

In particular both child cores are222; their least delays are3 and1.
The child's common core has identically zero low trace and period2.
Its high trace, starting at phase zero, is1,0,1,0,... . Therefore the
previously hidden transient can now affect the next cyclic phase.

For220 use T=3 in the round304 product formula. The respective low,
high and cyclic-high words through that horizon are

    u=(0,1,1), v=(0,0,1), w=(1,0,1).

There is a reset, and only its last occurrence contributes to the weighted
sum: v_2 XOR u_2=0; also XOR(w)=0. Hence

    (eta_220,theta_220)=(0,0), F_220(a)=0.           (10)

For224 use T=1. Its three bits are (u_0,v_0,w_0)=(0,0,1), so

    (eta_224,theta_224)=(1,1), F_224(a)=a XOR1.     (11)

Equations (8), (10), (11) contradict (4), already at a=0. With a
SECOND attached zero the distinct representatives are

    cyc(440)=444, cyc(448)=445.                      (12)

Both have least period4 on the hand cycle

    400 ->444 ->401 ->445 ->400.                    (13)

They are phase differences on this SAME cycle, not an additional finite
cycle fork or a new clock-growth rigidity counterexample.

## 3. Independent derivation without the product formula

Track just the low scalar response of the lift, using the original rule

    f_(s+1)=v_s XOR (u_s OR f_s), f_0=a.            (14)

For220, the three actual updates give a -> a ->1 ->0. The pure
222 driver through the same horizon flips, does nothing, flips; its net
action is identity. Thus the matching phase is0 for either a, as in(10).

For224, the sole actual update is identity. The pure222 driver at this
phase flips. Matching at time1 therefore requires phase a XOR1, as in(11).
The upper rows match at the stated horizons by (9). This independently
obtains the child phase maps without evaluating the weighted XOR formula.

The mechanism is loss and subsequent exposure of transient information.
The source's resetting cyclic low trace hides that information from F_y.
The next common core has a permutative low trace, and its phase depends on
the child transient. Even knowing the source's exact delay does not recover
that child transient. In this witness the child phase differs on the actual
zero branch, not merely on an unused choice of future boundary bit.

## 4. Fixed verification and scope fence

The fixed checker is
`experiments/problem1_nonperiodicity/check_round305_phase_transport.py`;
its atomic record is
`results/problem1/20260907_round305_phase_transport.json`.
It compares packed and independently written Boolean-cell A on every edge
of the declared closed certificates, then checks scalar OR response versus
the product formula for the two child sources and both input bits.
Horizon checks use T=tau(child) and T+2, to check phase alignment explicitly.
The inputs are ONLY the two original rows110/112, their one-bit children,
the children of220/224, and the displayed cyclic cores. The cycle cap is
16 updates, total wall cap10 seconds, memory cap128MiB, one local worker.

Any failure invalidates the hand certificate or formula implementation.
Agreement verifies only these fixed cases. No larger source, phase,
clock, FULL prefix or neighborhood collection is authorized by the result.

This does not construct an infinite FULL survivor. The source centers of
the hand pair are0; the pair is not offered as two states on one FULL orbit.
There is no refutation of a FULL-conditioned version of (4), which would
need its own justification on that possibly empty domain. Nor does this
rule out augmenting the state by further specified transient information.
It closes precisely the general full-core/exact-delay/one-bit-phase-map
update. A surviving general recurrence must retain information beyond(3),
and a FULL-only recurrence must explicitly prove why FULL supplies it.

Dependencies: the one-bit resetting/permutation lift theorem in
`problem1_physical_time_cycle_defects.md` Section4; phase-correct completion
in `problem1_cycle_completion_defect_transport.md` Section1; the transient
formula in `problem1_global_cycle_shadow.md` Section6. No external literature
deduction or all-depth machine verification is used here.
