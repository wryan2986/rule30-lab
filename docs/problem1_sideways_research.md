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
- independent cell-by-cell verification of true-prefix/permanent-zero traces
  and their compact first-failure certificate;
- fail-closed horizon, candidate, logical-work, certificate-size, and graph-size
  limits;
- direct-cell agreement for every transition of the width-5 truncated state
  model;
- independent reconstruction of every exported graph edge and canonical hash,
  byte-for-byte determinism checks, and an artifact-output cap.

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

### True prefix followed by a permanent-zero tail

This baseline makes the earlier observation precise. For a listed prefix
length \(L\), the candidate trace is defined for all times by

\[
\tilde c_t =
\begin{cases}
c_t, & 0 \leq t < L,\\
0, & t \geq L,
\end{cases}
\]

where the retained bits come from the trusted center vector. The finite run
uses only \(\tilde c_0,\ldots,\tilde c_{500}\) and reconstructs left depths 1
through 500. The default explicitly tested

\[
L \in \{1,2,4,8,16,32,64,128,256\}.
\]

Exact finite results:

| Retained prefix length \(L\) | First nonzero reconstructed-left depth |
|---:|---:|
| 1 | 1 |
| 2 | 3 |
| 4 | 4 |
| 8 | 8 |
| 16 | 16 |
| 32 | 33 |
| 64 | 64 |
| 128 | 128 |
| 256 | 256 |

All nine listed candidates therefore have finite incompatibility witnesses by
depth 500. The ordered unsigned-varint certificate has 11 bytes and SHA-256
`0f8c7be5f70fbc5333264ca50ddbd2c06fa420c8c021e79f6cd34699f793c0d5`.
The conservative resource ledger charged 3,377,250 logical cell updates.

This does not establish that every true prefix followed by zeros is
incompatible: prefix lengths other than the nine listed values were not part
of this baseline, and a finite reconstruction cannot exclude a witness first
appearing below depth 500. Each nonzero bit above is an exact certificate only
for its one fully specified candidate trace and finite depth.

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

The explicit artifact set contains 544 deterministically ordered edges (one
outgoing edge for each of 544 nodes) across those 14 graphs:

- [`fixed_width_periods_1_to_3_width_4.dot`](../results/problem1/graphs/fixed_width_periods_1_to_3_width_4.dot),
  31,492 bytes, SHA-256
  `df172879dca9235124c7af604372adc4cfa7f67cb7036e4609ea7d4cf975b252`;
- [`README.md`](../results/problem1/graphs/README.md), which records ordering,
  encoding, per-graph transition hashes, and the scope warning, SHA-256
  `c76957c0942999e2ca31a5af2b9cfbe43bb6601669ceb8b4a07e0c2d7959cd6f`;
- [`SHA256SUMS`](../results/problem1/graphs/SHA256SUMS), which checks the DOT
  and README bytes, SHA-256
  `7e845ff2e9ab6480819b32c6b60eef94fafe7a38369bd6c2efd6ca2961c1728c`.

The canonical graph-set digest, computed from ordered graph descriptors and
their canonical binary edge streams, is
`5afe6043b2da1a5f912bc0ddcd706ab4e1b91c24be086c96eb0fc48b1c6bb5f6`.
The artifact directory deliberately contains no JSON side manifest: JSON files
under `results/` are reserved for strict experiment-record envelopes.

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

The current complete formatted default JSON SHA-256 is
`de57a4feef2f5a8fde06873824a4a5114c06f2f0f7a1fac6ae14183e17c2a6d5`.

Reproduce the default true-prefix baseline and regenerate the explicit graph
artifacts with every relevant parameter stated:

```bash
cd /home/wryan/rule30-lab
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/run_sideways_search.py \
  --horizon 500 \
  --max-period 10 \
  --max-preperiod 3 \
  --eventual-max-period 5 \
  --true-prefix-lengths 1,2,4,8,16,32,64,128,256 \
  --graph-width 4 \
  --graph-max-period 3 \
  --export-graphs-dir results/problem1/graphs \
  > /tmp/rule30-problem1-sideways-with-graphs.json
sha256sum /tmp/rule30-problem1-sideways-with-graphs.json
(cd results/problem1/graphs && sha256sum -c SHA256SUMS)
```

The formatted stdout SHA-256 from that exact command is
`9330e80258e5dc57d30e354bfd9e59f86ddc0b31c9071dcc2652a431cdc85875`.
The command atomically replaces only the named DOT, README, and checksum files
after checking the combined artifact-byte cap.

To select a different finite box, use explicit parameters, for example:

```bash
.venv/bin/python experiments/problem1_nonperiodicity/run_sideways_search.py \
  --horizon 600 --max-period 10 \
  --max-preperiod 4 --eventual-max-period 5
```

The command fails before enumeration if the configured candidate, logical
work, certificate, horizon, finite-graph, or graph-artifact byte bound would be
exceeded. Every requested true-prefix length must be positive, strictly
increasing, and at most \(H+1\). Raise a bound explicitly only after checking
the resulting finite workload.

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
