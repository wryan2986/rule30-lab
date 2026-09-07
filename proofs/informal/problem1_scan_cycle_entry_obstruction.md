# A valid alternating block can leave the A-periodic core

Status: `refuted` for the two universal shortcuts stated below;
`partial-proof` for the displayed hand identities. No full survivor is
constructed and Problem 1 remains open. No numerical run is used.
Independent hand review accepted after lead audit:
`problem1_inverse_scan_reset_language_review.md`, Sections 7-8.

## 0. Decision and precise hypothesis

The reset-language argument shows that a FULL finite-entry survivor must
have tau_A(W_m)>2m infinitely often, where tau_A is first entry onto an
A-cycle. Before trying to prove that such lateness cannot occur, test the
strong local hypotheses:

1. A permitted forced step from a finite A-periodic state remains
   A-periodic.
2. Appending one zero spatial pair to an A-periodic finite state
   always reaches its A-cycle within two A steps, even when its actual
   next alternating block is valid for the zero right fringe.

Either hypothesis would support a cycle-entry induction on the same full
diagonal. A failing fixed certificate shows why such an induction needs
more of the full future premise. The hand construction below tests these
claims directly; it does not extend a survivor prefix or search a box.

## 1. One exact certificate (`refuted`)

Take x=55. Under A(v)=(v>>2) XOR ((v>>1) OR v),

    A(55)=13 XOR(27 OR55)=13 XOR63=50,
    A(50)=12 XOR(25 OR50)=12 XOR59=55.               (1)

Thus x is an A-periodic state of least period two. Its low four bits
are 7, so it is in the permitted u gate. The forced next state is

    F(55)=4 A^2(55)+3=223.                          (2)

But

    A(223)=55 XOR(111 OR223)=55 XOR255=200,
    A(200)=50 XOR(100 OR200)=50 XOR236=222,
    A(222)=55 XOR(111 OR222)=55 XOR255=200.          (3)

The distinct values 200 and 222 form a two-cycle, and 223 is neither
of them. Therefore tau_A(55)=0 but tau_A(F(55))=1. This refutes
hypothesis 1.

For the actual initial zero right fringe, W_1=4x=220. Directly,

    A(220)=55 XOR(110 OR220)=55 XOR254=201,
    A(201)=50 XOR(100 OR201)=50 XOR237=223.          (4)

Equations (3)-(4) give the entire eventually cyclic orbit

    220 -> 201 -> 223 -> 200 -> 222 -> 200 -> ... .

Its first three states are distinct from both cycle states, so
tau_A(W_1)=3>2, refuting hypothesis 2. The actual center-and-left
row at time 2 is X_1=223. Both D_0=55 mod4 and D_1=223 mod4 are 3,
so the full-fringe criterion proves the center is 1,0,1,0 at times
0,1,2,3. The certificate includes an ACTUAL valid alternating block;
it does not merely pick the branch independently of its right fringe.

There is no infinite survivor here: 223 mod16=15 is outside BOTH
permitted gates. This follows directly from the gate-domain identity
and is not a newly generated actual prefix. In particular the example
does not refute a claim conditioned on FULL for every future block.

## 2. The same certificate in temporal coordinates (`partial-proof`)

The known two-cycle (1) gives b=Theta(55)=(3,2)^infinity. Starting
I_0 from state 0 and reading this exact periodic word yields

    I_0 b = 0,1,3,0,2,0,2,0,2,... .                 (5)

This is a hand consequence of H_3:0->1 and H_2:1->3, followed by
H_3:3->0 and the recurring H_2:0->2, H_3:2->0. Its least preperiod
is three, as in (4). Shifting twice gives

    C_1=Theta(223)=3,0,2,0,2,... .                   (6)

Its exceptional initial 3 precedes the periodic {0,2} response, so
the diagonal lies exactly one time unit before the periodic tail.
This also checks the bit/symbol/time conventions independently of
the packed arithmetic. All displayed infinite continuations follow
from the stated closed cycles, not from extending a finite sample.

## 3. What remains open (`inconclusive`)

Neither example shows tau_A(4^m x)>2m infinitely often for ONE fixed
x, nor refutes eventual entry by 2m. The stronger asymptotic hypothesis
and its FULL-conditioned version remain open. No transient, period,
height, frontier, or candidate census is admitted from this certificate.
