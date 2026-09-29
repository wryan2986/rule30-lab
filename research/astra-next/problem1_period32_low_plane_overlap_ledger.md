# Problem 1: low-plane overlap ledger on canonical period-32 lift chains

Status: exact algebraic lemma plus invariant triage. This advances the all-depth rigidity reduction in `problem1_period32_child_fork_criterion.md`, but does **not** exclude period 32. Problem 1 remains OPEN.

## 1. Plane recurrence

Write consecutive low bitplanes along a period-preserving lift chain as

    X_s = L_(j-1)(s),
    Y_s = L_j(s),
    Z_s = L_(j+1)(s).

Because the high bitplane of a child is the low bitplane of its parent, the one-bit response recurrence is exactly

    Z_(s+1) = X_s XOR (Y_s OR Z_s).                 (1)

All indices below are cyclic modulo the temporal period (32 in the canonical application).

## 2. Exact mod-2 overlap ledger

Use the Boolean identity

    y OR z = y XOR z XOR (y AND z).

Taking XOR over all phases of (1), cyclic shift leaves `XOR_s Z_s` unchanged on the left. The `Z` parity therefore cancels from the two sides and gives

    XOR_s (Y_s AND Z_s)
      = (XOR_s X_s) XOR (XOR_s Y_s).               (2)

Equivalently, with

    p_j = |L_j| mod 2,
    o_j = <L_j,L_(j+1)> mod 2,

where the bracket is binary dot product mod 2,

    o_j = p_(j-1) XOR p_j.                          (3)

This is an exact all-depth identity for every recurrent one-bit lift, independent of period 32.

It gives a cheap consistency certificate for future symbolic/computational work: every generated triple of low planes must satisfy (2).

## 3. Run formula between reset phases

Whenever `Y_s=1`, equation (1) resets the next child bit independently of its previous value:

    Z_(s+1) = 1 XOR X_s.                            (4)

If a reset occurs at phase `r` (`Y_r=1`) and

    Y_(r+1)=...=Y_(r+k)=0,

then iterating (1) through that zero run gives, for `1 <= m <= k+1`,

    Z_(r+m)
      = 1 XOR X_r XOR X_(r+1) XOR ... XOR X_(r+m-1). (5)

Thus the child plane is determined interval-by-interval by prefix XORs of the preceding plane, with the 1-positions of the current plane acting as reset boundaries.

This is a more local form of uniqueness than the two-initial-state classifier and may be useful for a finite forbidden-pattern proof: a hypothetical diagonal collision `X=Y` forces every reset interval's prefix XOR expression to vanish in the next plane.

## 4. Consequences for a diagonal collision

The previous note established

    Z=0  iff  X=Y

before the first fork/death. Equation (2) adds a necessary parity condition one step earlier. If

    L_(j-1)=L_j=Y,

then applying (3) at index `j-1` gives

    |Y| mod 2
      = p_(j-2) XOR p_(j-1).

Since `p_(j-1)=|Y| mod 2`, cancellation yields

    p_(j-2)=0.                                      (6)

Therefore a fork/death precursor cannot occur unless the plane two steps before the zero child has even Hamming weight.

For the canonical starting layer `q(1-q)`, the initial low plane has weight exactly 16 and the preceding high/low plane is zero, so this parity condition alone does not exclude the canonical family. It is a necessary filter, not the missing rigidity theorem.

## 5. Invariant triage / dead ends

Several tempting scalar strengthenings were checked against the exact canonical recurrence and fail quickly:

- low-plane Hamming-weight parity is **not** fixed along canonical chains;
- low-plane weight is not bounded away from small values by a useful large constant (small nonzero weights occur);
- the already-fenced 16-shift anti-periodicity is not restored after a few lifts.

So a proof based only on weight/parity cannot establish all-depth noncollision. The run formula (5) suggests that the relevant information is the placement of reset phases together with interval prefix XORs of the preceding plane.

## 6. Next proof target

A concrete next target is a finite-state forbidden-diagonal lemma on reset intervals:

> Starting from `(L_-1,L_0)=(0,q(1-q))`, show that recurrence (1), while recurrent and period-preserving, cannot produce `L_(j-1)=L_j`.

Equation (5) reduces each step to XOR constraints on the cyclic gaps between 1s of `L_j`. A useful strengthening would find a gap statistic or interval charge that is inherited by (5) and is incompatible with all interval expressions simultaneously vanishing.

Separately, even all-depth uniqueness would still leave the second required p=32 ingredient: a uniform bounded source-automaton contradiction for every `2221`/backward-phase exit node. The observed `+34` bound remains finite-depth evidence only.
