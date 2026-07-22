# Public controlled-run provenance

The repository's original controlled-run records under `results/runs/` contain
machine-local executable paths, checkout locations, temporary paths, and
resource-runner metadata. They were intentionally excluded from the public
repository during publication rather than presenting local paths as portable
scientific artifacts.

[`20260722_controlled_run_manifest.json`](20260722_controlled_run_manifest.json)
replaces broken references to those local records with a tracked, path-neutral
manifest. Each entry states:

- the exact finite scope of the claim;
- its status label;
- the original source commit;
- the public analyzer and documentation paths;
- a direct reproduction command;
- the scientific certificate hash;
- the controlled stdout hash when recorded in the research log; and
- any existing tracked result file containing the scientific payload.

The manifest is not a recreation of the omitted operational records. It does
not claim to preserve process telemetry, clean-tree attestations, raw streams,
or temporary checkpoint state. Those details remain local operational evidence.
The public manifest instead provides the information needed to reproduce and
compare the deterministic scientific output.

A source archive produced with `git archive` omits `.git`. Such an archive can
validate source-level algorithms and certificate hashes, but commit existence,
clean-tree state, and history-bound provenance require a full Git clone.
