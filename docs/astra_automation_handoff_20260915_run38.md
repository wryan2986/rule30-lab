# Astra automation handoff — 2026-09-15 run 38

Branch: `research/astra-next`

## Repository state reviewed

Run started from `516f792c65b0fc440837ab509759da914ad4df7e` (run 37 handoff). No newer work was present. Problem 1 remains open.

Run 37 found exactly one periodic orbit at every bitlength through 400, with power-of-two periods and threshold starts `1,4,9,30,401`.

## New exact theorem

Writing an n-bit state as `x=2u+b`, the quotient evolves autonomously:

`A(x)>>1 = A(u)`.

The added low bit satisfies

`b' = u_1 XOR (u_0 OR b)`.

Thus over a parent cycle C of exact period p:

- if any parent phase has `u_0=1`, that phase resets the child bit, giving exactly one lifted cycle of exact period p;
- if `u_0=0` at every phase, the p-step fiber return is `b -> b XOR S(C)`, where `S(C)=XOR_j (u^(j))_1`;
- if `S(C)=1`, the two lifts join into one exact-period-2p cycle;
- if `S(C)=0`, they form two distinct exact-period-p cycles.

Therefore the observed uniqueness + power-of-two-period phenomenon reduces inductively to one explicit obstruction: prove that whenever the unique finite parent cycle has LSB identically zero, `S(C)=1`.

This also gives an exact interpretation of every period-doubling threshold: it occurs precisely one bitlength after a cycle whose LSB column is identically zero and whose next-bit column has odd XOR parity.

A useful immediate identity for the next run: under the no-reset hypothesis `u_0(t)=0`, the coordinate-0 recurrence forces `u_2(t)=u_1(t)` phasewise. Then the coordinate-1 recurrence gives `u_3(t)=u_1(t+1) XOR u_1(t)`, so the XOR parity of column 3 over a full cycle is automatically zero. The remaining task is to connect finite leading-boundary termination to odd parity of column 1.

## File added

- `proofs/informal/problem1_one_bit_extension_cycle_lifting_theorem.md`

Research commit: `3170763b908b70282e9ef34c63e9bc8c9af6365b`.

## Next target

Attack the parity obstruction on the periodic spacetime cylinder. Under `u_0=0`, set `a(t)=u_1(t)`. Then columns begin `0,a,a,Delta a,...`, and all higher columns are generated recursively by

`u_{i+2}(t)=u_i(t+1) XOR (u_{i+1}(t) OR u_i(t))`.

Prove that a finite word with fixed leading 1 boundary and zero beyond the top cannot arise from an even-parity nonzero periodic `a(t)`. A counterexample would instead produce the first bitlength with two periodic A-orbits and disprove the uniqueness conjecture.