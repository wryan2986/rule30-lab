# Problem 1: complete period-32 portal-root census and half-block renormalization boundary

Status: exact first-return classification of all sixteen genuine period-32 portal roots, plus an exact block-transducer lemma and a scoped one-lift no-go. Problem 1 remains OPEN.

## 1. Complete genuine p32 root census

The sixteen genuine period-32 portals are the derivative lifts of the sixteen terminating period-16 leaf necklaces. Starting from each canonical portal pair (x,0), iterate the exact recurrent child map

    a_(s+1) = (b_s XOR c_s) XOR ((1 XOR b_s) a_s)

using the already-verified 32-bit affine-prefix broadword transducer. At every depth the low plane is tested before advancing, so the reported zero is the first zero return, not merely a hit at the stated cap.

All returned targets below have exact rotational period 32.

| portal | p16 leaf | first zero depth | canonical p32 target | parity | weight | root type |
|---:|---|---:|---|---|---:|---|
| 0 | 0000010101000101 | 1,420,791,101 | 00011101011011010111110100111011 | even | 20 | branching |
| 1 | 0011101111101011 | 3,642,025,676 | 00000010010000110010100110011101 | even | 12 | branching |
| 2 | 0101101101111011 | 1,555,560,444 | 00001000111100010010101100101111 | odd | 15 | singleton |
| 3 | 0001010011100101 | 7,470,817,970 | 00011101111110111010110011111001 | odd | 21 | singleton |
| 4 | 0101010110111111 | 15,565,342,385 | 00000010011011110101000001010111 | even | 14 | branching |
| 5 | 0000100100100101 | 105,696,243 | 00000000001001100000010001101101 | odd | 9 | singleton |
| 6 | 0000001001011001 | 1,255,920,142 | 00011010101101110011001100111101 | even | 18 | branching |
| 7 | 0010111001100111 | 1,324,488,168 | 00001000100010100100010010011101 | odd | 11 | singleton |
| 8 | 0001010010001111 | 9,124,240,171 | 00001100101010001000101011010001 | even | 12 | branching |
| 9 | 0000011101010011 | 4,764,407,279 | 00000101101010111111101000010001 | odd | 15 | singleton |
| 10 | 0010101110101101 | 8,857,311,844 | 00001000010000101111011000110111 | even | 14 | branching |
| 11 | 0101111111011111 | 2,846,542,716 | 00010010001101100011011100101001 | even | 14 | branching |
| 12 | 0000110110000111 | 4,421,569,547 | 00001110001000110100101000111011 | even | 14 | branching |
| 13 | 0001001111001111 | 65,154,360 | 00000001001101101001100111100001 | odd | 13 | singleton |
| 14 | 0001111001111111 | 4,794,122,735 | 00000001110110101110100101000001 | odd | 13 | singleton |
| 15 | 0010111100111111 | 4,250,222,543 | 00011011110111111110110110101001 | odd | 21 | singleton |

Therefore the root split is exactly

    singleton / odd:  2,3,5,7,9,13,14,15
    branching / even: 0,1,4,6,8,10,11,12.

So eight genuine portal components terminate immediately and eight enter nontrivial full binary p32 trees.

The deepest root connector is portal 4:

    depth = 15,565,342,385
    target = 00000010011011110101000001010111
    parity = even.

This closes the previously unresolved root census completely.

## 2. Improved rigorous p32 leaf lower bound

The dyadic leaf-portal theorem gives

    L_32 = L_16 + sum_l B(l),    L_16 = 16,

where B(l) is the number of new exact-period-32 even internal vertices in the full-period tree entered through old leaf l.

The previous exact descendant work already proved

    B(portal 0) >= 3,
    B(portal 6) >= 5.

The complete root census now proves that portals

    1,4,8,10,11,12

each have an even full-period root, hence each contributes at least one additional internal vertex. Thus

    sum_l B(l) >= 3 + 5 + 6 = 14,

and therefore

    L_32 >= 30.

This is a rigorous lower bound. It does not claim that any of the eight branching portal trees are complete.

## 3. Exact half-block path-transducer normal form

For a p-phase block of the scalar recurrence

    y_(s+1) = c_s XOR (b_s OR y_s),

let r be the first index with b_r=1, or r=p if no reset occurs. Let q_s, 1<=s<=p, be the trajectory from input seed y_0=0.

Then for either input seed epsilon in {0,1},

    y_s^(epsilon) = q_s XOR epsilon * 1[s <= r],    1 <= s <= p.

Before the first reset, the two inputs remain complements; the reset destroys the input dependence, after which both paths coincide. Hence the entire two-input block path transducer is encoded exactly by the pair

    (r,q) in {0,...,p} x {0,1}^p.

Every such pair is attainable by a suitable choice of b,c, so the exact number of block path transducers is

    (p+1) 2^p.

The companion checker exhaustively reconstructs the path transducer from (r,q) for p<=8 and obtains exactly 4,12,32,80,192,448,1024,2304 states.

This compression is exact, but still exponential in p. A useful renormalization therefore has to exploit the special portal language or multiple spatial lifts; arbitrary half-block dynamics do not collapse to a constant-size state.

## 4. Universal two-lift normalization at a doubled odd portal

Let x be the antiperiodic derivative lift of an odd p-word into period 2p, and start the period-2p connector at (x,0).

The first recurrent child is exactly the all-one word:

    T(x,0) = (1^(2p), x).

With low plane all ones, every phase is a reset, so the next child is a one-phase rotation of complement(x). Antiperiodicity gives

    complement(x) = S^p x.

Therefore, modulo common temporal rotation,

    T^2(x,0) ~ (x, 1^(2p)).

This is an exact all-p identity, not a finite-depth observation. The checker also verifies it on all 1,023 odd words for p=1,...,10.

This gives a cleaner canonical starting state for a genuine multi-lift renormalization: after two forced lifts, the portal has returned to the same antiperiodic low-plane necklace with an all-one high plane.

## 5. One-lift half-block data do not decide endpoint parity

The complete p32 root census closes a tempting simpler route.

For each genuine p32 portal, split the initial antiperiodic word x into two 16-phase halves and encode each half by the exact block path code (r,q) above with c=0. On these sixteen genuine portals the second-half code is always

    (0, 1^16),

while the first-half code is determined solely by its first-reset index r.

Grouping the exact root outcomes gives

    r=2: portals 2 odd, 4 even, 11 even
    r=3: portals 1 even, 7 odd, 10 even, 15 odd
    r=4: portals 3 odd, 8 even, 13 odd, 14 odd
    r=5: portals 5 odd, 12 even
    r=6: portals 0 even, 9 odd
    r=7: portal 6 even.

Every reset class represented by at least two genuine portals contains both endpoint parities. Therefore even the entire one-lift half-block path response of the initial portal does not determine whether its first zero target is odd or even.

There is an independent lower-scale collision as well: two odd p8 portal words have identical initial half-block codes but opposite p16 first-return parity.

This is a scoped no-go. It does not rule out a multi-lift or scale-dependent half-period renormalization.

## 6. Research consequence

The p32 root classification problem is finished. More raw root scanning at period 32 has no value.

The next useful targets are now:

1. exploit the exact two-lift normal form (x,1^(2p)) to derive a genuinely multi-lift half-period state transition that retains enough information to predict the first diagonal endpoint; or
2. expand the six newly discovered branching p32 roots (1,4,8,10,11,12) and compare their descendant trees with the already explored portal-0 and portal-6 trees, looking for a recursive state that survives beyond one lift.

Do not fit another static statistic to the old p16 leaf alone, and do not use only the initial one-lift half-block path code; both routes are now explicitly fenced off.

Reproducers:

    experiments/problem1_nonperiodicity/check_period32_complete_portal_roots.cpp
    experiments/problem1_nonperiodicity/check_half_period_block_transducer.py

Atomic record:

    results/problem1/20261002_period32_complete_portal_root_census.json

Dependencies:

    problem1_period32_broadword_portal_tree.md
    problem1_last_reset_child_and_endpoint_parity_complexity.md
    problem1_dyadic_graph_embedding_and_leaf_portal_theorem.md
    problem1_derivative_lift_antiperiodicity.md
