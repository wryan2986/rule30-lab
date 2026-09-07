# Nonresetting cores return even when their clock does not double

Status: `partial-proof`, with external adversarial review missing. The
eventual statements are conditional on one eventual K=3 FULL orbit;
Section 3 needs only a current even spatial bound at a nonresetting source.
No FULL orbit is constructed or excluded. Problem 1 remains OPEN.
No new experiment is used.

## 0. Admission

The new one-bit phase theorem removes the apparent freedom to choose an
even-parity fork at a lag-one source. Determine whether retaining the entire
driver also classifies the clock-preserving nonresetting passages inside
K=3 repairs. A classification would locate the remaining phase choices and
which cyclic returns the driver marks; failure would leave a further source
case. This is an exact extension from doubling to nonresetting drivers, not
a larger clock tree, source collection, or strip-width sweep.

## 1. A shadow identity independent of FULL and of strip bounds

Fix a finite actual initial row with Y_0>0 and its entire right fringe,
and let Z_t=cyc(Y_t) be its global E shadow cut at the center. Positive
width and the physical bridge give Y_t>0 at every later time. Define

    N_t: the low A-trace of Z_t is identically 0,
    O_t: the low A-trace of Z_t is identically 1.

Then for EVERY physical t>=0,

    N_t iff O_(t+2).                               (1)

For the forward direction, the high A-trace of Z_t cannot also be
identically zero: Theta would then be the zero code and Z_t=0, whereas
positive finite width is preserved. Its first right extension has scalar
trace w_(s+1)=w_s XOR Z_t[1](s), so w visits both values. The next
cyclic extension has scalar recurrence v_(s+1)=w_s OR v_s, whose unique
cyclic response is identically 1. The two actual physical steps include
two A-time shifts, which preserve constancy of this shadow trace. This
proves O_(t+2), whether the first extension preserves or doubles the clock.

Conversely, write Q=Z_(t+2) and suppose its low trace is identically 1.
The A rule at that bit forces Q's bit2 trace to be identically 0:

    1=(A Q_s)[0]=Q_s[2] XOR (Q_s[1] OR 1)
      =Q_s[2] XOR 1.

The phase-correct physical bridge sigma^2 Q=A^2 Z_t now gives N_t.
No backward physical-time extension or FULL condition was used.

## 2. Under eventual K=3, all late nonresetting sources are even

Now assume the one fixed actual orbit is FULL and eventual all-physical
tau<=3. Import round306's eventual even delay bound tau(Y_(2m))<=2.

Suppose N_(t+1) holds at a sufficiently late ODD time, with t even.
The first extension trace w of Z_t is then identically 0 (shifting its
A phase does not change this property). Its scalar rule forces the two
bits of Theta(Z_t)_s to be equal at every s. Thus the complete core code
of Z_t is contained in {0,3}.

But FULL supplies Theta(Y_t)_1 and Theta(Y_t)_2 in {1,2}. Since tau(Y_t)
is at most 2, the second of those symbols already equals its core symbol,
which cannot belong to {0,3}. This contradiction proves

    NOT N_s for every sufficiently late odd s.      (2)

This excludes CLOCK-PRESERVING nonresetting odd extensions as well as
doubling ones. It uses the entire constant-zero core condition, not odd
parity of a flip count. By (1) it also excludes O_s at all sufficiently
late odd times.

## 3. The two even source profiles and their selected phases

For this section it suffices to assume a CURRENT even FULL source with
b(Y_t)<=2 and N_t. No future strip bound is needed for its classification
or return. The eventual K=3 theorem supplies that current bound at every
sufficiently late even source. The source is noncyclic because its actual
center is 1 whereas its shadow center is 0.

Let u be the actual gate-u indicator. FULL fixes actual bits0..3 to
(1,1,u,1 XOR u). Bits>=2 agree with the shadow. The zero low shadow
trace requires its bits1 and2 to be equal, hence shadow bit1=u. There
are exactly the following two conditional profiles:

| actual gate | source (d_-1,d_0) | source delay | shadow right pair (h,k) |
| --- | --- | --- | --- |
| u | (0,1) | 1 | (1,1) |
| t | (1,1) | 2 | (0,1) |

The first row is the one-bit phase theorem. For the second row let
x=Y_t and z=Z_t. Their low bits are respectively (1,1,0,1) and
(0,0,0,1), with all bits>=2 agreeing. Direct A updates give

    (Ax mod4, Az mod4)=(1,2), A^2x=A^2z.            (3)

The equality is not inferred only from the displayed four low bits.
Zero shadow low trace at its second A step forces the shared initial
bit4=0: the shadow's first A bit2 is bit4 XOR 1, so its second A low
bit is bit4. The first A difference is in bits0 and1; its next bit0
difference vanishes and its next bit1 difference is exactly bit4.
Thus both disappear on the second step, proving tau(x)=2 exactly.

For the ACTUAL first-right cut q=2x+a, x's center and left neighbor 1
give (Aq)[0]=0. The actual pair Ax mod4=1 then gives (A^2q)[0]=1.
The upper row A^2z is cyclic and nonresetting, so A^2q is already cyclic.
Projection makes cyc(q)=2z+h. Its scalar trace has first two driver
symbols 0 and 2, so its value after two steps is 1 XOR h. Phase-correct
completion forces h=0. That trace visits both bits, so the unique cyclic
second lift is the constant 1 response, giving k=1. No right bit was
chosen to obtain this phase.

There is a separate paired verification. The actual pair at position1/2
is nonzero because this is gate t. Its first two scan states under the
ACTUAL first symbols 3,1 are 0,3. The prospective cyclic pair state 1
under the CORE first symbols 0,2 also reaches 3 after two steps:

    H_3(a_pair)=0 for a_pair!=0, H_1(0)=3;
    H_0(1)=1, H_2(1)=3.

The state 1 belongs to the cyclic invariant pair {1,3} for the complete
nonresetting core. Matching A^2 images and the common upper row therefore
give cyc(4x+a_pair)=4z+1. State 1 is physical right pair (0,1), as claimed.

In both source profiles the next even row is CYCLIC. To see this without
a future strip premise, the nonresetting first physical step consumes
one unit of the source delay 1 or2, and hence the second extension has
an already cyclic upper row. By (1) its unique recurrent low bit is 1;
the ACTUAL next even center is also 1. This is the correct cyclic lift.
The return has constant-one core low trace and its actual gate is t.
The first physical step has R_t=0; the second also has R_(t+1)=0. It doubles
the clock on the first step exactly when the core high-bit weight per
least period is odd, and otherwise preserves it on both steps.

## 4. Consequences and limits of the classification

Round306's eventual passage decomposition places every two-bit even source
with (d_-1,d_0)=(1,1) at offset4 of one of its six-step repairs. Thus a
late t-gate nonresetting core is such a repair source, additionally meeting
the whole-driver condition N_t. Its selected pair is (0,1), so
the repair is cyclic. The u case is a one-bit return. A cyclic repair
does not conversely imply N_t, and N_t does not imply a doubling: its
high-bit parity may be even. No existence of either parity on the full
infinite domain is asserted.

Equation (1) identifies the distinguished cyclic returns exactly: a late
even row has constant-one core low trace iff its preceding even core is
nonresetting. This marks both genuine clock doublings and clock-preserving
nonresetting returns. Both require a preceding noncyclic episode. More
precisely, at late paired indices put I_m=1[tau(Y_(2m))>0], let B_m count
the 0->1 switches, and let F_m indicate N_(2m) with EVEN high-bit weight
over its least period. Then for a late interval [M,Q),

    sum B_m >= log_2(p(Y_(2Q))/p(Y_(2M)))
                 + sum F_m - I_M + I_Q.            (4)

Indeed every even nonresetting source is a 1->0 switch by Section 3;
its odd-weight cases are exactly the clock doublings, and its even-weight
cases are the F_m. Odd nonresetting sources are absent by Section 2.
The number of all 1->0 switches is sum B_m+I_M-I_Q. This proves (4),
without asserting that every cyclic return is nonresetting. Thus these
clock-preserving returns also require fresh birth supply. No finite-support
upper bound on either count is provided.

The remaining resetting returns and births still depend on their complete
periodic drivers. This classification does not make those drivers finite
in number or bound how often any original ancestor can be reused. Do not
enumerate new source cores, fork positions or longer clock trees from it.

## 5. Verification scope

Equation (1) has independent extension and projection directions. The
odd-source exclusion compares the core at A-time2, where the eventual
even delay bound really guarantees equality. The two-bit phase is derived
by both scalar and paired scans with the actual transient retained. All
displayed finite identities follow directly from the hand A/H rules; no
numerical experiment is needed or run. External review remains missing,
so the assigned status is `partial-proof`.

Dependencies: `problem1_global_cycle_shadow.md`;
`problem1_physical_time_cycle_defects.md` Sections 1 and 4;
`problem1_full_driver_exit_phase.md`;
`problem1_three_bit_exit_repair.md` Sections 2, 3 and 6;
`problem1_full_fringe_temporal_diagonal.md` Section 4.
