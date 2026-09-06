# Joint windows, including the original time seam

Status: `partial-proof` for the inequalities and implications below,
independently reviewed and accepted in scope. The ACTUAL-survivor hypotheses
remain `inconclusive`. No new numerical experiment is admitted.

Review: `problem1_activity_joint_window_review.md`; exact reviewed and
current sources are archived in `results/problem1/20260906_round5_final_audit.json`.

## 1. The transport inequality also permits a=0 (`partial-proof`)

The transport note proves its counting bound for n>=1,a>=n-1,W>=1.
Its a restriction can be weakened to a>=0. Exactly,

    sum_(s=a+2..a+W+n) V_s(x)
      >=sum_(r=0..floor((n-1)/2))ceil(C_n(a,W)/(2r+1))
      >=C_n(a,W)H_n,                                  (1)

for EVERY 2-adic x, n>=1,a>=0,W>=1, where

    C_n(a,W)=sum_(t=a..a+W-1)P_n(t),
    P_n(t)=bit_(2n)(A^t x) OR bit_(2n+1)(A^t x),
    H_n=H_odd(floor((n-1)/2)).

Proof of the extra range, without changing any local lemma. For a
selected j=n,n-2,..., an assigned occurrence lies at an age
s>=a+j+1>=j+1. Thus BOTH indices j,j+1 are present in V_s.
Keep this pair's actual age interval [a+j+1,a+W+n] throughout
the event-assignment count. The selected index pairs are disjoint;
all their counted occurrences lie in the common age interval
[a+2,a+W+n] and occur among its legitimate V terms. Summing their
counts is therefore bounded by the full V sum on that interval.
There is no need to extend any w_j to an age s<j or to assert that
all selected indices exist at the common interval's earliest age.
The preceding proof's extra a restriction only simplified that
enlargement, not the actual counting mechanism. All sums are finite.

## 2. A single anchored window at each offset (`partial-proof`)

Put J_n(x)=C_n(0,n). Equation (1) gives

    R_(2n)(x)>=J_n(x)H_n/(2n-1), n>=1.                (2)

Consequently sup_n J_n(x)H_n/n=infinity implies R(x)=infinity.
The stronger condition limsup_n J_n(x)/n>0 also suffices, since
H_n tends to infinity along every unbounded sequence of n.
Neither condition has been established for an actual survivor;
neither is asserted necessary. In particular the sparse temporal-code
counterexample to fixed-n density does not decide these joint limits.

There is a WEAKER sufficient condition using the independently reviewed
finite-entry theorem and the explicit staircase support bound:

    sup_n J_n(x)=infinity implies R(x)=infinity.        (3)

Proof, with a quantitative contrapositive. Suppose R(x)<=K, K an
integer, and put h=h_V(K), g=g(K). The prior decomposition gives
z=A^h x=pi^h T^h x finite with R(z)<=K and bitlen(z)<=4g+2.
A preserves finite bit length. For n>=2g+1 and t>=h the pair
2n,2n+1 of A^t x=A^(t-h)z is therefore zero. Hence

    J_n(x)<=h for n>=2g+1,
    J_n(x)<=n<=2g for 1<=n<=2g,
    sup_(n>=1)J_n(x)<=max(h_V(K),2g(K)).               (4)

This covers K=0: h=g=0 and all J_n vanish. The implication (3)
uses (4) by contradiction; it does NOT assert that bounded J implies
bounded R. No new finite-entry theorem is being inferred or proved.
For a given K, one exact J_n exceeding the right side of (4) would
already refute R<=K, with no density assumption. Such observations
have not been computed or admitted here.

## 3. Precise remaining target (`inconclusive`)

For ONE FIXED ACTUAL survivor, retain the full fringe recurrence and
prove unbounded J_n, or directly prove that the finite lower bound
in (1) becomes unbounded after division by its W+n-1 ages. Do not
replace the input by its successive forced states: the exact gate
bridge shifts ray depth downward when pulled back and does not apply
to depth-zero boundary events.

The anchored count J_n is determined by a finite original input cone
(its last sampled time is n-1). This observation does not establish
growth or admit a numerical prefix campaign. Any future experiment
must first give a concrete falsifiable consequence of a proposed
FULL-fringe mechanism and state how either outcome changes its proof.
The inequalities above supply a target and exact constants; the
missing mechanism remains the mathematical bottleneck.
