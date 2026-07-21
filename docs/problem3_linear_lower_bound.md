# Problem 3B: exact linear lower bound

Candidate statement: every finite uniform exact algorithm computing `c_n`
requires `Omega(n)` time in a fixed model.

This is stronger than merely excluding `o(n)` for irregular runtime functions:
`not o(n)` does not by itself imply an eventual positive linear lower bound.
The canonical experimental model and encoding are the same as in
`problem3_sublinear.md` unless a claim explicitly states otherwise.

Status: `inconclusive`. Benchmarks and predictor searches cannot establish a
universal lower bound.
