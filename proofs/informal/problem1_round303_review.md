# Round 303 lead adversarial disposition and missing external review

Status: `partial-proof` for the new all-depth deductions; `refuted` for
the explicitly scoped finite-observation rule; `finite-exhaustive` for
the fixed four-state algebra only. No fresh external review succeeded.
Problem 1 remains OPEN. This is a strategy-reset checkpoint.

## External review provenance

Muse thread 01a07ae9-2411-7281-bc32-c3b8338e4438 was assigned fresh review
of the three exact incoming round-ten main notes and their lead disposition.
It returned an error before writing review text:

    MissingSessionID: Request is missing x-opencode-session and cannot
    be routed efficiently.

The thread was closed. Thus the incoming review debt was NOT discharged.

Muse thread 01a07af4-6793-75f2-8a90-87c5cfc869cc was separately assigned
fresh adversarial review of the new cycle-birth observation no-go, including
its period, valuation, topology, and fixed-fringe quantifiers. It returned
the same MissingSessionID error before writing review text and was closed.

Neither response was a 429; the prescribed 429 paused-retry sequence was
not triggered. MiMo was not in this session's advertised model overrides.
No native reviewer was substituted, no provider configuration was changed,
and no direct-provider request was attempted. No external review file was
produced by either thread. The dispositions below are lead work only.

## Fresh lead adversarial audit of the new result

The reviewed claim is in problem1_cycle_birth_observation_no_go.md. The
main possible fatal flaws and their dispositions were as follows.

1. **Composition order and wraparound.** The drive is shift^2 b. Its
   length-p period reads b_2,...,b_(p-1),b_0,b_1. Thus the two suffix
   factors act BEFORE H_3 and H_g, exactly as displayed. The two-word
   maps H_3 H_1=0 and H_1 H_1=2 were checked from the bit equations as
   well as the table. They force constant complete returns 2 or 3.
   A first-letter exception in the reset language cannot survive a
   constant factor.
2. **Least onset and least period.** The recurrent response starts at
   z=2 or 3. Each first update identifies 2 and 3, making a wrong
   initial 3 coalesce at exactly A-time one. A purported pure period
   would fail at a common multiple with p. Applying Phi to the response
   recovers shift^2 b, so its eventual period is exactly the input's.
3. **Exact dyadic period.** The padding condition p>=max(8,2L) puts
   p/2 in the zero padding, whereas symbol 0 is 3. Every proper divisor
   of the power of two p divides p/2. This proves least period p for
   BOTH words, even when the prescribed prefix has its own repetitions.
   No finite spatial support is inferred from this dyadic period.
4. **Valuations.** The final code symbols differ only in their high bit.
   Theta's low-then-high triangular inversion makes the first spatial
   difference 2p-1. The four-input-offset leading term in A^2 then
   makes the first output difference 2p-5; F shifts it to 2p-3.
   In contrast the cycle completions have low pairs 2 and 3. No carry
   argument about ordinary distances is used.
5. **Actual first injection.** An A-periodic source with low pair 3
   gives a cyclic odd row 2Ax: the periodic scalar drive at its phase
   -1 resets the low bit to 0. This is a phase of the periodic driver,
   not negative actual time. The paired lag distinction is therefore
   a new R_1 in {0,1}, with R_0=0, not a transported old lag.
6. **Topology versus certified clock data.** With only an observed row
   or code, every finite prefix cylinder has both outcomes, so the birth
   predicate is nowhere continuous on the cyclic permitted domain.
   If a certified exact period is supplied separately, reading a full
   period DOES decide the birth. The strategy table and Section 4 were
   clarified before running the checker: the stronger-data statement
   excludes only a uniform observation bound, including a bound that
   ignores the growing period. It does not exclude a p-dependent scan.
7. **Same physical fringe and finite cones.** For sites [-W,R] and times
   through H, every initial left depth used is at most W+H. The bound
   2L>W+H therefore suffices, with the complete initial right fringe
   retained exactly. The constructed sources shadow the chosen FULL
   realization for this finite observation. They need not shadow it
   after that horizon. The two constructed actual time-two rows equal
   F of their sources, because the actual alternating prefix includes
   the first gate and the next even pair.
8. **Infinite quantifiers and finite entry.** There is a new pair of
   sources for each finite observation, not one infinite FULL source.
   Pure periodic coding supplies rational rows, not necessarily finite
   rows. For a cyclic row, finite entry is exactly finite support, and
   that is exactly Phi-nilpotence of its code. The explicit fixed code
   (12)^infinity checks that dyadic period alone is insufficient.
   Neither finite-source density nor an eventual all-physical K=1 bound
   is claimed. No consequence for periods >=3 is asserted.

Disposition: accept the new construction at `partial-proof` scope and
the corresponding finite-observation rule as `refuted` on the stated
domain. Do not promote it to `rigorous-proof` without fresh independent
review. It closes a finite-observation birth route on general cyclic
rows; it does not close the finite-support-specific route or Problem 1.

## Computational verification scope and provenance

The checker independently reconstructs each driven map by enumerating
the unique next symbol solving the two deletion equations. These 16
entries equal the hand table. It also checks the first-step merger of
states 2/3 and the exact nonnilpotent dyadic code Phi(12)=12.

The interior of a period is abstracted to ANY function on four states:
256 functions, two gates, two suffixes, four starting states, giving
4,096 return checks. The table and independently inverted equations
agree in every case. These are not a period, seed, or word enumeration.
The finite check supports the composition identities, not the infinite
physical shadow argument or finite support of any completion.

Invocation, from a small parent to avoid inherited launcher peak RSS:

    python3 - <<'PY'
    import subprocess, sys
    raise SystemExit(subprocess.run([sys.executable,
        'experiments/problem1_nonperiodicity/check_round303_birth_algebra.py'],
        check=False).returncode)
    PY

The atomic record is results/problem1/20260907_round303_birth_algebra.json.
It includes exact parameters, full base Git commit, executed source and
proof/dependency hashes, CPU/software facts, the canonical algebra payload,
timing scope, and limitations. The 10-second wall and 128-MiB memory caps
passed. There was one successful run and no failed scientific run.
Payload SHA256:
524cb6f940adf7e13d20e4e8407e7c702dbc5b63ff5eab769fb99486f2439f61.

The immutable reference hash was checked without editing its source.
This is a simple algebra checker, not a new or optimized Rule 30 backend.
