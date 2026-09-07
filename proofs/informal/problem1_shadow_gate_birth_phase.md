# A cyclic-source birth is an actual/shadow gate disagreement

Status: `partial-proof` for the identities on one fixed actual spacetime;
`finite-exhaustive` only for the listed algebra and fixed controls. Fresh
external review is missing. No autonomous gate/lag/phase quotient, bounded
birth count, or FULL exclusion is proved. Problem1 remains OPEN.

## 0. Admission and exact missing datum

The conditional K=1 episode argument leaves the next birth from a cyclic
even row undetermined by current gate and lag. Round303 shows that arbitrary
finite observations of the actual source cannot decide that birth on the
general cyclic domain. Round304 now supplies a uniquely selected GLOBAL
shadow with the entire original fringe retained. Test whether a local
observable of THAT shadow gives an exact birth criterion, and identify
the full periodic-driver information encoded by this observable.

A positive identity would locate the missing datum inside the same coupled
spacetime, and a failure would invalidate that proposed link. Neither outcome
authorizes more source words or longer observed gate prefixes. This is not
a refitting of the failed actual-observation quotient: the shadow observable
is computed from the whole cycle phase, not from a fixed actual neighborhood.

The proof has two independent routes: direct two-step physical updates and
a quotient of the four-state periodic scan. The fixed test checks their
new Boolean identities and two already known finite cyclic sources. It does
not search for sources or claim their finite continuations are infinite FULL.

## 1. Statement on ONE fixed actual orbit (`partial-proof`)

Keep the entire original nonzero finite row and right fringe, its actual
evolution r, and the global shadow hat r=U^t E(r(0)). Assume FULL, with
c_t=1 at even t and0 at odd t. Let t be an even time at which

    x=Y_t is A-periodic.                            (1)

Only the local FULL consequences through t+3 will enter the proof. No
fringe is reset at t. Define the actual and shadow right-pair zero flags

    u_t=1[(r_1(t),r_2(t))=(0,0)],
    hat u_t=1[(hat r_1(t),hat r_2(t))=(0,0)].        (2)

The actual u_t is the existing gate-u indicator; gate t has u_t=0.
The shadow flag is an observable of the SECOND whole spacetime. It is
not asserted to be an actual permitted gate when that shadow fails FULL.

Then the exact birth law is

    tau(Y_(t+1))=0,
    chi_t:=tau(Y_(t+2))=u_t XOR hat u_t in {0,1}.   (3)

Thus a cyclic-source paired birth occurs exactly when the two right pairs
disagree about being00. In physical-renewal notation R_t=0 and
R_(t+1)=chi_t. No K=1 assumption is needed for this ONE cyclic-source step.

## 2. Direct physical derivation, without a scan return

At time t, cyclicity and the global-shadow theorem imply d_i(t)=0 for
EVERY i<=0. FULL gives r_-1(t)=r_0(t)=1, so the shadow has the same two1s.
At time t+1, all positions<=-1 agree by their input cones. At the center,
the common center1 masks the possibly different right neighbor; both
outputs are1 XOR1=0. Thus all positions<=0 agree at t+1, proving the
first part of(3).

At t+2, all positions<=-1 still agree. The common center at t+1 is0, so
the next center difference is exactly the right-neighbor difference:

    d_0(t+2)=d_1(t+1)
      =(r_1(t) OR r_2(t)) XOR
        (hat r_1(t) OR hat r_2(t))
      =u_t XOR hat u_t.                            (4)

The common old center1 cancels in the calculation of d_1(t+1).
If(4) is0, the whole center-and-left row equals its cyclic representative.
If it is1, only its lowest bit differs. Its common bit at index1 is1,
because FULL has c_(t+2)=1 followed by c_(t+3)=0. One A step erases that
lowest disagreement, while all higher bits already agree with the cyclic
representative. The least delay is therefore exactly1. This proves(3).

For completeness, the existing actual-gate interpretation follows locally.
Write b=Theta(x), so b_0=3 and the permitted gate gives b_1 in {1,2}.
The actual left neighbor at t+1 is b_1 mod2, and the actual right neighbor
at t+1 is1 XOR(r_1(t) OR r_2(t)). Requiring c_(t+2)=1 therefore gives

    r_1(t) OR r_2(t)=b_1 mod2,
    u_t=1[b_1=2].                                 (5)

The higher bit condition b_1 in{1,2} uses the permitted/FULL premise;
it is not inferred from just two center values.

## 3. Which global phase does the shadow flag remember?

Let p be the least period of the PURE code b=Theta(x), and extend that
periodic code to all integer A-times. Negative indices here are virtual
periodic phases, NOT an assertion about the actual prehistory before the
original finite row. Since b_1 is1 or2, p>=2 and the integer

    ell=max{s<0:b_s in {1,2}}                      (6)

exists, with ell>=1-p. Then

    hat u_t = XOR_(s=ell+1..-1) 1[b_s=3],           (7)
    chi_t = 1[b_1=2] XOR
              XOR_(s=ell+1..-1) 1[b_s=3].         (8)

An empty XOR is0. The suffix between the last reset1/2 and phase0 contains
only0s and3s; the flag is precisely the parity of its3s. This is one global
phase bit, with a potentially period-dependent lookback, not a uniform
finite observation of the actual source.

To prove(7), the current shadow cut ending at position2 is

    z=cyc(4x+2r_1(t)+r_2(t)), pi z=x.

Its code w=Theta(z) is a pure periodic pair-lift of b, with

    w_(s+1)=H_(b_s)(w_s),
    H_0=[0,1,3,3], H_1=[3,2,2,2],
    H_2=[2,3,1,1], H_3=[1,0,0,0].

The source contains3 and1 or2, so the existing reset theorem gives a
unique recurrent lift, independent of the two actual appended right bits.
This does not replace those bits in the actual spacetime.
Set Z_s=1[w_s=0]. The EXACT two-state quotient of these four maps is

| input b_s | Z_(s+1) |
| --- | --- |
| 0 | Z_s |
| 1 or2 | 0 |
| 3 | 1 XOR Z_s |

At ell the zero flag resets to0; each later3 flips it and each0 preserves
it. Thus Z_0 is the parity in(7). Since w_0 is the shadow right pair,
Z_0=hat u_t, proving the formula.

For an independent return-map derivation of(8), begin the paired physical
scan with the drive b_2,b_3,... . Just before the final wraparound inputs
b_0=3 and b_1=g, its recurrent state is zero exactly when the flag in(7)
is1. The final maps H_g H_3 send it to2 precisely when
that flag XOR1[g=2] is1; otherwise the recurrent start is3. The actual
start is3, and every H_i coalesces2/3 after one update. This gives the
same exact delay in(3), without the two-step physical-cell calculation.

The old round303 suffix13 has flag1, and suffix11 has flag0, reproducing
its four return alternatives. This is a consistency check, not a repeated
source construction. Finite spatial support does not supply a proved
uniform bound on the backward distance in(6).

## 4. Exact forward transport retains the wider shadow fringe

Write the current shadow right cells as (a,b,c,d)=(hat r_1,...,hat r_4)(t).
At a cyclic source(1), both actual and shadow centers at times t,t+1 are
1,0. The three shadow right cells after one step are

    A=1 XOR(a OR b), B=a XOR(b OR c), C=b XOR(c OR d).

The right pair after the second step is (A OR B, A XOR(B OR C)). It is00
iff A=B=C=0. Solving those conditions gives a=b=1 and c OR d=1. Hence

    hat u_(t+2)=hat r_1(t)*hat r_2(t)*
                       (hat r_3(t) OR hat r_4(t)). (9)

The identical calculation for the actual fringe gives

    u_(t+2)=r_1(t)*r_2(t)*(r_3(t) OR r_4(t)).       (10)

Equation(9) is valid for this transition even if it creates a birth at
t+2, since the two center inputs used were at t and t+1. Reusing(9) at
a noncyclic successor would require its OWN shadow center values; one
must not impose1,0 on that shadow by fiat. Equation(10) keeps the actual
FULL boundary throughout.

These identities retain information beyond the two flags. They do not
prove that arbitrary four-bit assignments are realizable on the admissible
shadow, nor rule out every possible further quotient. The known no-uu
condition is visible as a special case: a00 first pair cannot satisfy the
next flag's a=b=1 condition. That observation does not determine a later
birth or bound the number of gate disagreements.

## 5. Fixed checks and stopping fence

`experiments/problem1_nonperiodicity/check_round305_shadow_gate.py` checks
the sixteen letter/state cases of the NEW zero-indicator quotient and
the sixteen four-bit cases of the NEW forward flag identity. These are
Boolean identity checks, not source or local-neighborhood discovery.
It also checks exactly two fixed finite physical controls:

| source Y_0 | fixed original right half | Y_1 | Y_2 | (u_0,hat u_0) | birth |
| --- | --- | --- | --- | --- | --- |
| 27 | r_1=1, all r_i=0 for i>=2 | 50 | 111 | (0,0) | 0 |
| 55 | all r_i=0 for i>=1 | 100 | 223 | (1,0) | 1 |

The shadow right-pair cuts are cyc(110)=111 and cyc(220)=222, respectively.
Their centers alternate through time3 in these fixed controls, which is
enough for the local law. No infinite FULL continuation is asserted.
Whole-row Boolean-cell physical updates are compared with the independently
packed original-cut bridge, and the named A-cycle certificates are closed
exactly. The two sources and their hand cycles already appear in prior
notes; no additional source is selected or searched.

Admission: a disagreement invalidates the proposed new identity or its
implementation. Agreement is `finite-exhaustive` only on these32 algebra
cases and two fixed controls, not machine verification of the all-depth
FULL theorem. Caps:10 seconds,128MiB, one local CPU, three physical steps
per control,16 A updates per certificate,128KiB output. Atomic provenance
is `results/problem1/20260907_round305_shadow_gate.json`.

The continuing target is the sequence of actual/shadow gate disagreements
at cyclic returns, with the original finite actual fringe and the entire
uniquely selected shadow retained. Formula(7) specifies the missing phase
datum, while(9) displays its wider driver. Neither formula establishes an
autonomous update of the phase bit, eventual agreement of the two flags,
a finite birth budget, or nonexistence of FULL. Do not replace this global
phase bit by an empirically chosen gate prefix.

Dependencies: `problem1_global_cycle_shadow.md` Sections1-4;
`problem1_inverse_scan_reset_language.md` Sections1-2;
`problem1_cycle_birth_observation_no_go.md` Sections1,3;
`problem1_physical_time_cycle_defects.md` Sections1,3;
`problem1_one_bit_strip_return_constraint.md` for the unresolved episode
question to which(3) applies at each cyclic return.
