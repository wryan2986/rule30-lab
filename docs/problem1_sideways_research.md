# Problem 1: finite sideways reconstruction research

Status date: 2026-07-21

## Scope and claim status

This work provides a maintained, independently tested engine for exact finite
sideways reconstruction and bounded exhaustive searches. Its search results
have status `finite-exhaustive`: every member of a stated finite set was
checked through a stated finite horizon.

It does **not** prove that the infinite Rule 30 center sequence is not
eventually periodic. Preperiods, periods, and reconstruction depths are
unbounded in Problem 1, while every computation below bounds all three.

## Conventions

The Rule 30 local map is

\[
x_j(t+1)=x_{j-1}(t)\mathbin{\mathsf{xor}}
          \bigl(x_j(t)\mathbin{\mathsf{or}}x_{j+1}(t)\bigr).
\]

An input called a horizon-\(H\) center trace contains exactly

\[
c_0,c_1,\ldots,c_H,
\]

so it has \(H+1\) bits. The engine fixes \(x_j(0)=0\) for every \(j>0\)
and reconstructs exactly

\[
x_{-1}(0),x_{-2}(0),\ldots,x_{-H}(0).
\]

The inverse local equation is

\[
x_{j-1}(t)=x_j(t+1)\mathbin{\mathsf{xor}}
            \bigl(x_j(t)\mathbin{\mathsf{or}}x_{j+1}(t)\bigr).
\]

An empty trace is rejected because it does not contain \(c_0\). A one-bit
trace has horizon zero and reconstructs an empty left prefix.

## Maintained engine and independent checks

[`sideways.py`](../src/python/rule30lab/sideways.py) packs temporal columns
into Python integers, with bit \(t\) storing time \(t\). The initial right
half is evolved in a separate packed spatial representation. If `C` and `R`
are aligned packed traces of a column and its right neighbor, one leftward
step is

```text
L = (C >> 1) XOR (C OR R)
```

followed by an explicit mask for the shortened valid time interval. This is
algorithmically distinct from the immutable supplied implementation, which
stores a two-dimensional byte-array right triangle and loops over individual
cells.

The focused test suite establishes:

- exhaustive agreement with an independently written cell-by-cell triangular
  oracle for every binary center trace through horizon 7 (510 traces);
- exhaustive round trips from independently evolved initial-left words through
  horizon 6 (254 initial configurations);
- exhaustive agreement with the immutable supplied reconstruction for every
  binary trace through horizon 6 (254 traces);
- an all-zero reconstructed left prefix of length 500 for the trusted Rule 30
  center vector `c_0,...,c_500`;
- hand-checked periodic and preperiod-plus-period indexing;
- certificate encode/decode and corruption detection;
- fail-closed horizon, candidate, logical-work, certificate-size, and graph-size
  limits;
- direct-cell agreement for every transition of the width-5 truncated state
  model.

The engine uses a conservative logical-work ledger. For horizon \(H\), one
reconstruction is charged

\[
H^2 + \frac{H(H+1)}2
\]

scalar Boolean site updates, even though packed integer operations execute the
same finite computation faster.

## Exact finite search results

The default deterministic experiment used reconstruction horizon 500. Thus
each candidate supplied `c_0,...,c_500`, and 500 initial-left cells were
eligible to witness exclusion.

### Pure periods 1 through 10

Every fixed-width binary word of every length 1 through 10 was tested. Words
were enumerated by increasing length, then increasing unsigned value in
most-significant-bit-first notation.

Exact result:

- candidate word descriptions: 2,046;
- descriptions with an all-zero reconstructed 500-bit left prefix: 10;
- distinct periodic traces among those descriptions: 1;
- surviving trace: the constant-zero trace, represented by one all-zero word
  at each of the ten tested lengths;
- survivors satisfying the required single-cell condition \(c_0=1\): 0;
- largest first-nonzero witness depth among excluded descriptions: 11;
- certificate payload SHA-256:
  `668d97828f3828932483edd936c1fb527f14c12e9b098f2a39161c65b36cfd6d`.

This reproduces the earlier observation precisely while separating traces
from redundant word descriptions. The constant-zero trace reconstructs zero
because it is the evolution of the all-zero initial configuration; it is not
the required center trace because the single-cell seed has \(c_0=1\).

The worst-case resource ledger charged 767,761,500 logical cell updates for
this exhaustive search.

### Bounded preperiods plus periods

The default extension enumerated every description with preperiod length
\(m=0,1,2,3\) and period length \(p=1,2,3,4,5\), including every binary
preperiod and every binary period word.

Exact result:

- candidate descriptions: 930;
- descriptions with an all-zero reconstructed 500-bit left prefix: 20;
- all 20 are redundant descriptions of the constant-zero trace (one for each
  pair \((m,p)\));
- survivors satisfying \(c_0=1\): 0;
- largest first-nonzero witness depth among excluded descriptions: 10;
- certificate payload SHA-256:
  `a339533bba85ba02e4603395a7b9f88cfee8dbb11fec98a77a02767a6d58a4a0`.

The worst-case resource ledger charged 348,982,500 logical cell updates for
this exhaustive search. This finite box says nothing about descriptions with
\(m>3\), \(p>5\), or a witness first appearing beyond depth 500.

### Compact certificates

Each search emits one unsigned varint in deterministic candidate order:

- `0` means no reconstructed one occurred at depths 1 through \(H\);
- `d >= 1` gives the first nonzero reconstructed depth.

The raw canonical varint stream is SHA-256 hashed and base64 encoded in the
JSON record. It is an exact compact list of finite witnesses rather than only
a summary hash. Survivor descriptions and a first counterexample are also
reported. A deliberately tiny horizon test confirms that the code returns a
counterexample instead of asserting that only zero survives when the finite
claim is false.

## Fixed-width state graph: valid finite scope

For a fixed right-half width \(W\) and a fixed period word of length \(p\), a
node is

\[
(\text{period phase},\text{the }W\text{ right-half bits}).
\]

There are exactly \(p2^W\) nodes, and each has one deterministic successor.
The experiment exhaustively builds this finite functional graph, hashes every
edge, computes indegrees and cycles, and follows the orbit from the all-zero
right state. The default run built all 14 word-description graphs of lengths
1 through 3 at width 4.

This is not a depth-independent finite-state reduction of Problem 1. Its
outer site \(W+1\) is forced to zero at every update. Width \(W=H\) safely
contains the finite causal cone through horizon \(H\), but then the elementary
state bound is \(p2^H\), which grows exponentially with reconstruction depth.
A cycle seen after the artificial outer boundary can influence the region is
only a property of the truncated model.

A de Bruijn-style graph can likewise encode local constraints on a fixed-width
spacetime strip, but its state size grows with the retained strip. No uniform
depth-independent state bound, valid minimization, or finite transducer for the
semi-infinite problem has been established here.

## Reproduction

Run the focused tests:

```bash
cd /home/wryan/rule30-lab
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest \
  -p no:cacheprovider tests/python/test_sideways.py -q
```

Emit the default deterministic JSON:

```bash
cd /home/wryan/rule30-lab
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/run_sideways_search.py \
  > /tmp/rule30-problem1-sideways-default.json
sha256sum /tmp/rule30-problem1-sideways-default.json
```

For the code and parameters recorded on 2026-07-21, the complete formatted
JSON SHA-256 was
`dd800415557f9d84a3f3c40892802a95298308cd793509ba1af60746885a8c4c`.
The run took 0.79 seconds and 21,720 KiB maximum resident memory on the recorded
WSL environment. That timing is an empirical measurement, not part of the
mathematical result.

To select a different finite box, use explicit parameters, for example:

```bash
.venv/bin/python experiments/problem1_nonperiodicity/run_sideways_search.py \
  --horizon 800 --max-period 11 \
  --max-preperiod 4 --eventual-max-period 5
```

The command fails before enumeration if the configured candidate, logical
work, certificate, horizon, or finite-graph bound would be exceeded. Raise a
bound explicitly only after checking the resulting finite workload.

## Current limitations and next theory target

The finite compatibility lemma in
[`problem1_finite_sideways_inversion.md`](../proofs/informal/problem1_finite_sideways_inversion.md)
explains why an all-zero reconstructed finite left prefix characterizes the
corresponding true finite evolution. It does not collapse the infinite family
of eventual-period descriptions.

The strongest computational next step is not merely increasing horizon 500:
all candidates in the current boxes already fail by depth 11. More valuable
directions are increasing preperiod and period bounds, looking for a symbolic
description of first-failure witnesses, and proving a depth-independent
invariant that excludes every nonzero periodic driver. Any such invariant must
avoid assuming a finite state bound that itself grows with reconstruction
depth.
