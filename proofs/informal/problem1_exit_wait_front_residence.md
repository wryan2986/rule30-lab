# A one-bit exit has an exact complete-driver waiting time

Status: `partial-proof`, with fresh external adversarial review missing.
This is an all-period conditional identity, not an eventual delay bound or
a FULL exclusion. Problem 1 remains OPEN. No new experiment is used.

## 0. Admission

The complete-driver exit-phase formula identifies when a one-bit source
exits, but an exit by itself does not state the amount of new delay. Test
whether its NEXT reset in the same periodic core determines that amount
exactly, including the second physical step. A positive identity translates
the whole-driver constraint into the globally ordered residence intervals;
a failure would mean that a further low-bit residual has been omitted.
No longer source, gate prefix, or waiting-time sample is searched.

## 1. Exact waiting time without a future strip assumption

Use the fixed actual FULL orbit and global E shadow of
`problem1_full_driver_exit_phase.md`. At an even time v suppose

    d_i(v)=0 for i<=-1, d_0(v)=1,
    actual gate u, h=hat r_1(v)=0.                 (1)

Let x=Y_v, z=cyc(x), b=Theta(z), extended with its least period p. The
phase theorem proves that b is RESETTING, so the integer

    L=min{n>=1:b_n in {1,3}}                       (2)

exists. FULL gives b_1=b_2=2: b_1 is the actual u gate, and no-uu forces
the next gate t through H_(b_2)(3). Since b_0=2 as well,

    3<=L<=p-1.                                    (3)

In particular p>=4. The exact local delays and injections are

    (tau_v,tau_(v+1),tau_(v+2))=(1,L,L-1),
    (R_v,R_(v+1))=(L,0).                           (4)

Both physical steps preserve the least eventual clock:

    p(Y_(v+1))=p(Y_(v+2))=p(Y_v)=p.                (5)

These assertions do not assume an eventual K=1, K=2, or K=3 bound.

For the first delay, the physical bridge gives Y_(v+1)=2Az with actual
low bit 0, since Ax=Az. The shadow's low bit there is 1 by the exit table.
The upper row Az is cyclic. Its first reset occurs at A-time L-1, so the
wrong scalar lift has least delay L by the exact one-bit extension law.
This derives the FIRST equality in (4) directly from the full driver.

For the second delay, the two even rows Y_(v+2) and cyc(Y_(v+2)) differ
in exactly bit1, and their low pair symbols are respectively 3 and 1.
Their common upper row is A^2z, with pure code b_2,b_3,... . In the
pair scan the hand transitions are

    H_0: 1->1, 3->3;       H_2: 1->3, 3->1;
    H_1: 1->2, 3->2;       H_3: 1->0, 3->0.        (6)

Thus the two states stay distinct under every preceding 0/2 and coalesce
at the first 1/3, namely input b_L. Input b_2 is used for update number
1, so coalescence occurs at update L-1, not L or L-2. The upper rows
agree throughout. This proves the LEAST second delay L-1 and excludes
an additional residual injection at v+1. Formula (4) now follows from
R_s=tau_(s+1)-max(tau_s-1,0).

Equation (5) also retains the complete core. The first extension is
resetting because b contains 1/3, hence preserves p. Write w for the
pure low trace of the shadow's first right extension at v. Its source
values satisfy w_0=h=0, w_1=1 by b_0=2. Therefore w contains a reset for
the SECOND scalar extension as well. That extension also preserves p.
Physical A-time shifts do not change these least eventual periods.

## 2. The whole initial front residence, not just its first three cells

Use ORIGINAL cuts s_j=tau(L_j(r(0))) and the global front J(u)-u from
`problem1_global_discrepancy_front.md`. Since all three delays in (4)
are positive, the exact threshold identities give

    s_v=v+1,
    s_(v+1)=s_(v+2)=v+L+1.                         (7)

Consequently the complete residence of characteristic v+1 is

    J(u)=v+1 for v+1<=u<v+L+1.                     (8)

In physical coordinates its leftmost discrepancy and spatial depths are

    m(v+k)=1-k, b(Y_(v+k))=k, 1<=k<=L.             (9)

These are EXACT values, independently of the later residence intervals.
The original characteristic v+2 has an empty residence by
(7). The erasing 1 for (8) is at physical cell

    (i,u)=(-L,v+L).                                (10)

Indeed b_n[0]=0 for 1<=n<L and b_L[0]=1; the actual and core A-traces
agree at every n>=1. The physical bridge identifies this word as the
actual cells r_(-n)(v+n), giving the same eraser (10) independently of
the s_j calculation. Immediately BEFORE that eraser acts, the front
itself is one cell to its right, at 1-L.

The general exit therefore marches through precisely L successive
depths before this first erasure. This word alone does not determine the
front after v+L: the rest of the evolved shadow tail
still determines the next visited characteristic. In particular (9)
does not bound the later low-bit delay injections.

## 3. What this says about a strip bound

Under an eventual all-physical bound tau<=K, choose v sufficiently late
for the equivalent b bound too. Every exit (1) must have L<=K, by (4)
or independently by (9). Thus K=1 or K=2 cannot accommodate an exit;
at K=3 every exit must have L=3. This recovers the first part of the
round306 repair profile without extending its local table to larger widths.
It does not prove entry into any strip or complete a K=3 repair.

There is a precise code consequence at a K=3 exit:

    (b_0,b_1,b_2,b_3)=(2,2,2,1).                  (11)

Only the last symbol needs checking. The actual code c at v+2 starts
c_0=3, c_1=1 and c_2=H_(b_3)(1). FULL requires c_2 in {1,2}. Among
the two reset letters available at b_3 when L=3, H_1(1)=2 is permitted
and H_3(1)=0 is not. Therefore b_3=1. This is a symbolic consequence
for an already specified exit, not a new prefix census or an exclusion
of longer L outside a strip assumption.

The backward phase condition from round307 and the forward wait (2)
refer to the SAME periodic word. A finite-support proof must control
their occurrence along the actual sequence of full cores; assigning an
independent backward parity and forward waiting word loses that coupling.
Neither finiteness of each L nor the bound L<=p-1 limits the number of
such events when the clocks grow.

## 4. Complete one-bit passage accounting

For clarity the phase formula and (4) give the following table at any
even source with current discrepancy (1)'s first line. For the t rows,
the first positive reset is immediately b_1=1. The old physical table
gives a center-only defect at the next even row, with its common left
neighbor 1, so its least delay is exactly 1.

| actual gate | h | three delays | two injections |
| --- | --- | --- | --- |
| t | 0 | 1,1,1 | 1,1 |
| t | 1 | 1,0,1 | 0,1 |
| u | 1 | 1,0,0 | 0,0 |
| u | 0 | 1,L,L-1 | L,0 |

All physical clock doublings in such a two-step passage are now classified:
they can occur only on the FIRST step of the u,h=1 row, and exactly
when b is contained in {0,2} with an odd count of 2s per least period.
To see that the second step never doubles, in every case b_0=2 forces
the first-right shadow trace to have consecutive values h,1 XOR h.
It therefore contains 1 and resets its next scalar lift. A resetting
first driver preserves p; a nonresetting one has precisely the imported
odd/even parity alternatives. No eventual strip premise enters this
classification. It describes one passage, not an autonomous passage
sequence or a bound on its repeated supply.

## 5. Verification and limits

The scalar waiting law, global front identities and physical exit table
are explicit dependencies already checked in their recorded scopes. The
four pair transitions (6) also follow directly from the hand H table;
coalescence at an arbitrary L follows by induction, with no sampled wait
or numerical period cutoff. The original-cut proof and the direct A-ray
proof of the eraser (10) are separate offset checks.

Fresh adversarial review is required and currently missing. The new result
has `partial-proof` status. No source, periodic word, waiting-time, clock-tree,
or further-strip experiment is admitted here. The outstanding task remains
global transport or incompatibility on the one original finite-fringe orbit.

Dependencies: `problem1_full_driver_exit_phase.md`;
`problem1_one_bit_shadow_exit.md`;
`problem1_cycle_delay_renewal.md` Sections 1-2;
`problem1_global_discrepancy_front.md` Sections 1-3;
`problem1_physical_time_cycle_defects.md` Sections 1 and 4;
`problem1_full_fringe_temporal_diagonal.md` Section 4.
