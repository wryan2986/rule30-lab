# Problem 1 run 199 — corrected t+10 front propagation

Status: `partial-proof`. Problem 1 remains OPEN.

Continue only the corrected run-193--198 chain. Run 197 left

    p := r_-5(t+4) = bit_1(A^4 z)

with

    p=0 => m(t+9)=0,  J(t+9)=t+9,
    p=1 => m(t+9)=-1, J(t+9)=t+8.

Run 198 proved that the zero low A-trace does not choose p. Put

    w := A^4 z.

Then

    (w[0],w[1],w[2])=(0,p,p).

This note propagates the corrected front one more row and identifies the next genuinely relevant complete-driver bit.

## 1. A boundary-discrepancy rule

For Rule 30

    F(l,c,r)=l xor (c or r).

Suppose at some row the leftmost discrepancy is at position j, so actual and shadow agree at j-1 and j-2. The only differing input to the update at j-1 is the right input at j. Therefore

    d_(j-1)(next)=1 iff the common center r_(j-1)=0.

This lets us decide whether the front propagates one cell left without knowing the farther-right continuation.

## 2. The p=0 branch is rigid at t+10

From the complete driver

    Y_(t+4)=16 w+7

and the low prefix w=(0,p,p,...), literal Rule-30 propagation for five physical steps gives

    r_-1(t+9)=0                    when p=0.

This identity is independent of every farther-right cell. Since run 197 gives m(t+9)=0 in this branch, the boundary rule implies

    d_-1(t+10)=1.

Hence the corrected p=0 branch has the exact next front

    m(t+10)=-1,
    J(t+10)=t+9.

So characteristic t+9 necessarily has at least a two-row residence: it is the front at physical rows t+9 and t+10.

## 3. The p=1 branch exposes the next driver bit

In the p=1 branch, run 197 gives m(t+9)=-1. The common actual/shadow value immediately to its left is obtained from the same five-step propagation:

    r_-2(t+9)=w[3].

Therefore

    d_-2(t+10)=1 xor w[3].

Consequently

    w[3]=0 => m(t+10)=-2 and J(t+10)=t+8.

If w[3]=1, the discrepancy does not spread to -2; determining whether it remains at -1 or moves right requires the next local discrepancy update and is not asserted here.

The zero low A-trace again constrains but does not choose this bit. Evaluating the next trace equation

    (A^2 w)[0]=0

under (w0,w1,w2)=(0,p,p) gives

    p=0 => w[4]=0,
    p=1 => w[4]=w[3].

Thus on the p=1 branch the two scalar-trace-compatible next prefixes are

    01100...
    01111...

through bit 4. The next branch bit is w[3], not an unconstrained arbitrary physical neighbor.

## 4. Consequence

The corrected front now has one fully rigid branch and one driver-controlled branch:

    p=0: J(t+9)=t+9 and J(t+10)=t+9;
    p=1,w3=0: J(t+9)=t+8 and J(t+10)=t+8;
    p=1,w3=1: J(t+9)=t+8, with the t+10 front still to classify.

This exhibits a repeated pattern: persistence of the global front is selected by successive low bits of the same complete cyclic driver. It does not yet give a finite-support bound on how often such persistence can occur.

No claim from invalidated runs 184--192 is used.

Dependencies: `problem1_run197_corrected_tplus9_front.md`, `problem1_run198_p_is_not_fixed_by_low_trace.md`, and the established Rule-30/A low-bit rule.