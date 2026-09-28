# Problem 1 run 324: no pure low temporal primitive for the m/f residual

Problem 1 remains open. Continue from run 323.

Run 323 produced the exact low-coordinate residual F(p,x3,x4,x5,x6). I tested whether F can be removed as a temporal coboundary

    Delta_h G := G_(t+h)+G_t = F_t

for an arbitrary Boolean function G of the same five low coordinates.

The exact restricted one-step map on (p,x3,x4,x5,x6) has two 16-cycles. One of those cycles has odd F parity. Hence every odd h fails immediately, because T^h traverses the same 16-cycle when gcd(h,16)=1.

For h=2, the induced map has four 8-cycles. Their F parities are

    0, 0, 1, 0.

A violating 8-cycle is

    11000 -> 10101 -> 11101 -> 10011
          -> 11001 -> 10100 -> 11100 -> 10010 -> 11000,

where states are ordered (p,x3,x4,x5,x6). Therefore Delta_2 G=F has no solution. The same orbit partition rules out h congruent to 2,6,10,14 mod 16.

For h=4, the induced map has eight 4-cycles. Seven have even F parity and one has odd parity:

    10010 -> 10101 -> 10011 -> 10100 -> 10010

(up to cyclic choice of representative; equivalently the previously checked p=1,x3=0 four-cycle). Thus h congruent to 4 or 12 mod 16 fails.

For h=8, T^8 pairs opposite points of each 16-cycle. On one such pair,

    11000 <-> 11001,

direct substitution in the run-323 ANF gives F(11000)=1 and F(11001)=0. Hence Delta_8 G=F is impossible.

Finally h congruent to 0 mod 16 makes the low-state map the identity, so Delta_h G=0 while F is nonzero.

Therefore:

    BOX: for every integer h, there is no Boolean
         G(p,x3,x4,x5,x6) with Delta_h G = F.

This is an orbit-parity obstruction, not a failure of a polynomial ansatz.

A useful consequence for the next attack is that adding any other pure-low temporal coboundary Delta_h H cannot repair the obstruction: its XOR around every T^h orbit is zero, so the odd orbit parity class of F is unchanged. Therefore a successful recombination with the r/u sector must contribute a genuinely non-coboundary low term after elimination, or must retain at least one additional transported/high variable. Merely rewriting the existing low terms as more temporal differences cannot close the proof.

Next target: return to the complete post-four-step expression, keep the r/u boundary terms before eliminating them, normalize the shifted u phases with runs 308--310, and test whether their full coefficient changes the odd orbit class. Do not continue searching for a pure five-variable primitive of F.
