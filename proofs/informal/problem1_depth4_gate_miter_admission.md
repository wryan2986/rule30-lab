# Admission: exact depth-four gate counterexample miter

Status before execution: CONJECTURE / no experiment result yet.
This targets H_gate, the exact local criterion for affine extension in
`problem1_blind_output_gate_criterion.md`, at the first unproved depth
r=4. It is not a finite-state model of the full Rule-30 prize instance.

Either a witness refutes the general affine layer transport route, or
complete absence of a witness suggests a finite graph certificate for
an all-period depth-four lemma. Neither outcome alone transports an
original-support resource through portal restarts. This is the explicit
whole-tail relevance, rather than a broad larger-period census.

## Exact finite state bound

Two depth-five stacks share the same depth-four state U (eight bits).
Their two added pairs have two bits each. The product has exactly

    2^(8+2+2)=4096

possible states, including transient and invalid cyclic states. Attach
three parity bits for the two drivers and temporal length. The lifted
graph has exactly 32768 vertices. No spatial width, observer depth, or
arbitrary period bound is inferred beyond this fixed observer graph.

At each product state try all four label pairs (a,b). Retain the edge
only if the depth-four outputs coincide. Thus at an upper nonblind state
only a=b is permitted; at an upper blind state all pairs are permitted.
Use exact normalized transitions with fixed boundary pairs (1,0),(0,1).
Update the parity sheet by XOR with (a,b,1).

A bad edge has upper state blind, a=b, and unequal outgoing newest Y
bits. A counterexample needs a product cycle containing a bad edge,
nonzero last upper raw track, even length, and odd weight in BOTH driver
words. The parity target is (1,1,0). Earlier nonzero tracks through depth
three follow from the proved shallow theorem on that odd/even domain;
the recovered witness will independently check all parent tracks anyway.

Search the complete finite graph by strongly connected components.
For a bad edge from (u,0) to (v,h), seek a path from (v,h) to (u,110)
visiting a vertex with nonzero last upper pair. The ordered bits here
mean driver-A parity one, driver-B parity one, temporal parity zero.
Use one documented integer sheet encoding consistently. Only actual
recovered paths certify a counterexample; component membership alone
must not be reported as an explicit witness without path construction.

For two resulting driver words w,z sharing w_s=z_s at the bad phase,
choose another upper blind phase t and form the four words

    w, z, w+e_s+e_t, z+e_s+e_t.

There must be at least three blind phases if same-label gate variation
exists in a complete odd fiber. This is a targeted four-input square,
not enumeration of every label assignment. Validate common upper orbits,
all odd parities, nonzero parents, and nonzero full output XOR directly.

## Controls and stopping

Implement only r=4; do not expand to r=5 or increase an input period
box. Run locally with caps 60 seconds wall, 256 MiB resident memory and
256 KiB output. Stop on the first independently rebuilt counterexample
or a cap. A no-witness result remains an unchecked finite graph result
until a separate verifier and a complete all-period reduction are written.

For an explicit witness, reconstruct scalar cyclic children independently
and replay original two-row temporal updates. Compare the graph's local
transitions against that separate bit-array rule on all local states and
label pairs. Record exact graph/domain counts, ordered search rule,
completed checks, path and input hashes, hardware/software, full base
commit, timings, source hashes and limitations, with atomic output.

Use only the named new checker/result paths assigned to its cheap worker.
Never edit the immutable reference. No new optimized backend, long
first-zero-return traversal, first-witness center scan, remote workload,
or model escalation is admitted.
