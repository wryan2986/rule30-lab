# Astra automation handoff — 2026-09-24 run 247

Problem 1 remains open.

## New result

Run 246's sampled constants are now exact consequences of existing structural lemmas.  The order history

`64 -> 128 -> 256 -> 256`

is exactly run 243's `Q -> 2Q -> 4Q -> 4Q` theorem with `Q=64`, so the base plateau complexity is

`L(X_14)=3*64+2=194`.

Run 242's statewise plateau-after-doubling identity then propagates complexity through each subsequent `D/P` pair:

`L_new = P + L_old + 1`.

Hence

`194 -> 256+194+1 = 451 -> 512+451+1 = 964`.

This proves the run-246 observed values `L(X_16)=451` and `L(X_18)=964` for every state satisfying the corresponding complete full-period histories; they are not merely sampled regularities.

Full proof: `proofs/informal/problem1_run247_exact_complexity_propagation_through_pdpd.md`.

## Next target

Do not spend another run explaining 194/451/964.  The first potentially new obstruction is a history containing consecutive plateaus that cannot be reduced immediately to a `D/D/P` seed plus repeated `D/P` propagation.  The earliest exact order segment is

`O_9=64, O_10=64, O_11=64, O_12=128, O_13=256, O_14=256`.

Analyze the triple-64 plateau, especially the complexity classes of full-period coordinate-11 words and which classes can feed the subsequent 64→128 doubling.  Seek a statewise identity or exact census before attempting larger widths.
