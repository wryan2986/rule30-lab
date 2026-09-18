# Astra automation handoff — run 120

Problem 1 remains OPEN.

Starting branch tip: `9a38d84b4fab93e8a6da07dc5e7c0c2d02aa9407` (`research/astra-next`). No intervening work was found after run119.

## New result

Expanded the exact forcing event requested by run119. For a two-bit nonreset source u=0, the source-time global-shadow cells at positions 0,1,2 are exactly `001`. Those three cells alone force the returned second-right bit to zero two steps later:

    r1(t+1)=f(0,0,1)=1,
    r2(t+1)=f(0,1,a)=1,
    r2(t+2)=f(1,1,*)=0.

Hence the return pair `10`, and therefore the later forced beta=1 birth, is independent of all deeper right-shadow cells. The wider-driver cancellation is a genuine minimal local forcing phenomenon, not merely a quotient artifact.

Recorded in `proofs/informal/problem1_two_bit_birth_forcing_cone_collapses_to_001.md`.

## Stopping fence

Do not expand the local forcing cone farther right in search of a consumed resource: those cells are irrelevant to the forced zero bit. Every admitted two-bit N source carries the same source-relative `001` forcing motif. This does not prove reuse of the same physical/time-zero cells, so it does not kill characteristic charging altogether.

## Next target

Separate minimal forcing from provenance. If continuing the characteristic route, trace the three `001` shadow cells backward through the globally selected shadow to time zero and seek a theorem that successive two-bit N sources have strictly ordered provenance/intercepts or bounded reuse. The burden is now entirely on provenance/history; local Boolean forcing contains no additional source-specific resource.
