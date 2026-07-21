# Problem 3A: no exact sublinear algorithm

Candidate statement: no single finite exact algorithm computes `c_n` for every
`n` in time `o(n)`.

Baseline model for repository experiments: deterministic uniform multitape
Turing machine; canonical binary encoding of `n`; one output bit; no advice,
oracle, or unbounded preprocessing; transition count includes input access;
the machine halts for every input. RAM and circuit results must state and prove
their simulation overhead before being transferred to this model.

Status: `inconclusive`. Finite failure to find a shortcut is not a lower bound.
