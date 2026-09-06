# Admission: local seams of the activity staircase proof

Status before execution: `inconclusive`. This is a finite local-algebra
verification supporting `problem1_activity_staircase_bound.md`, not a
survivor experiment. Admission precedes both implementations.

Exact hypothesis: for A's cell rule
u_i(t+1)=u_(i+2)(t) XOR (u_(i+1)(t) OR u_i(t)), a zero adjacent pair
over L consecutive times forces the next higher adjacent pair zero
over the first L-1 times. Also the staggered zeros
u_i(t+1)=u_(i+2)(t)=0 force u_i(t)=u_(i+1)(t)=0.
Either failed implication kills the new staircase proof. Agreement
checks only the finite local seams; the all-width induction, disjoint
packing, harmonic limit and actual-survivor limitations require proof
and fresh independent review, not extrapolation.

Check precisely:

1. All eight three-bit neighborhoods, comparing the A output bit and
   the staggered-zero implication. Retain all input/output bits.
2. All sixteen four-bit initial windows for the L=2 rectangle; evolve
   valid cone widths 4,2. When the bottom pair is zero at both times,
   check that the upper pair is zero initially.
3. All sixty-four six-bit initial windows for the L=3 rectangle;
   evolve valid cone widths 6,4,2. When the bottom pair is zero at
   all three times, check that the upper pair is zero at times0,1.

The fourth/fifth/sixth bits are genuinely needed for the declared
local time cones. This is not a larger spatial-orbit census. No other
width, input, history, age interval or numerical claim is admitted.
Previously certified values R(27)=1,R(111)=2 are cited as scope
controls in the proof and are NOT re-executed. Highest-one persistence
is checked by the already hand-derived local input (higher,higher,self)
=(0,0,1); no whole-row orbit is needed.

Primary: packed integers A=T>>2, masking to each valid cone width.
Independent: explicit bit arrays, direct cellwise truth conditions;
no scientific source import or shared computed result between methods.
Both retain complete local trajectories, premise counts, conclusion
counts and per-case verdicts. Integration compares these full payloads.

Bounds per implementation: local one CPU,120 seconds CPU and wall,
1GiB address-space cap; no GPU or network workload. Stop on first
failure or any cap, record failure/inconclusive, and do not enlarge.
Records use atomic same-directory temporary writes, flush/fsync and
replace; retain full Git commit, exact parameters, executed source
and admission snapshots, hashes, software/hardware facts, runtime,
limitations and claimed finite domain. No optimized backend or test
of the immutable reference is involved; record its unchanged hash.

Expected completed status: `finite-exhaustive` only for these eight,
sixteen and sixty-four local cones. Successful checks do not prove
Problem1, exclude a mortal rational actual survivor, or authorize an
activity-level enumeration or first-witness search.
