# Problem 1 run 315: weighted mixed eight-shift formula

Problem 1 remains open. This continues run 313.

Let Q=qplus, J=j, U=u, and X=x5, with phase t suppressed. Established identities give
Q(t+8)+Q(t)=1+X(t),
J(t+8)=J(t),
U(t+8)+U(t)=J(t)+J(t+2),
and X(t+8)=X(t).

Applying the Boolean product rule directly to the actual weighted mixed term gives

Delta8(Q J U)
 = (1+X) J U
 + Q(t+8) J [J+J(t+2)].

Thus an eight-shift does not by itself eliminate U from the Q-weighted term: the exact surviving high coefficient is (1+X)J. This corrects the tempting but insufficient inference that closure of bare J U immediately closes Q J U after eight steps.

The residual coefficient C=(1+X)J is itself eight-periodic. Therefore

Delta8(C U)=C[J+J(t+2)],

which is entirely low-coordinate. Equivalently a second eight-shift removes the remaining U term. Since Q, J, and U are each 16-periodic, Delta16(Q J U)=0, consistent with this two-stage reduction.

For the other coefficient R=J+J(t+1), also eight-periodic,

Delta8(Q R U)
 = (1+X) R U
 + Q(t+8) R [J+J(t+2)],

and its surviving U coefficient (1+X)R is again eight-periodic, so a second eight-shift removes U.

Conclusion: the actual qplus-weighted mixed sector has a precise two-stage 8-shift descent. One eight-shift leaves only an eight-periodic low coefficient times U; the next removes U entirely. The next calculation should use these formulas when taking the compact run-302 expression through its 16-step comparison, rather than treating qplus as eight-periodic.
