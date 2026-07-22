# Fixed-width Rule 30 transition graphs

This directory contains the explicit DOT edge list for all binary period-word descriptions of lengths 1 through 3 at fixed right-half width 4.

> Warning: These are exact fixed-width graphs with a permanently zero outer boundary. Their state bound grows as period_length * 2**width; they do not establish a depth-independent finite-state model for the semi-infinite Rule 30 reconstruction problem.

Edges are ordered by increasing period length, unsigned MSB-first word, phase, and unsigned right-state.
Integer bit `j-1` stores site `j`; DOT state names display bits most-significant first.

Canonical edge encoding: phase, state, next phase, and next state as fixed-width little-endian unsigned integers. The phase width is `ceil(bit_length(period_length)/8)` and the state width is `ceil(width/8)`, each at least one byte.

- DOT: `fixed_width_periods_1_to_3_width_4.dot` (31492 bytes)
- Graph descriptions: 14
- Explicit nodes/edges: 544
- Canonical graph-set SHA-256: `5afe6043b2da1a5f912bc0ddcd706ab4e1b91c24be086c96eb0fc48b1c6bb5f6`
- File hashes: `SHA256SUMS`

| Period | Nodes | Canonical transition SHA-256 |
|---:|---:|:---|
| `0` | 16 | `b09f61caa2eb171f93174429f1b4637c58f0563f3cb782a1cf9dffb0f7b6498e` |
| `1` | 16 | `065f111fed64ecbc59c606c81cedf921c909232152f9510359a08e3a72346a7c` |
| `00` | 32 | `532e62c992cd39d0c63b87775c9a98667b98f18cfe2f107e66934267a2f63186` |
| `01` | 32 | `26d123d8a57e809a744e75212ea6c2a103055ea8221661df8e73b0fc9d49b5c1` |
| `10` | 32 | `0d16caff5950e5bb68e38ff6ea57d0022afda076e81c82946fbd463e8f363fd1` |
| `11` | 32 | `507daeb58df21f045fd894f73f4eaef0168e483f6c2858b40bb88efb38cec9c5` |
| `000` | 48 | `397bef8027c7707b72ac1c6490b90fc4431c348fdd1524220b9b500e056c8101` |
| `001` | 48 | `e8aa5271af8923a7eaa78dda2ad346065c91170b2af9a9692d86921c5938c2a4` |
| `010` | 48 | `5196540f8d6c61e9d86181e20033e67a32d41d08ff0f6271fca4d9e9ceea06c2` |
| `011` | 48 | `118049427bbabf715a46a0a1d3945f11687cb638fb36646816cd3a4d60f2c741` |
| `100` | 48 | `370915d77076a038c52f04d53aed85be85c1c2307d4076f35679382001e8fc59` |
| `101` | 48 | `e0fec878f9e94acd5e6d641f394fbd4148c153ac72f4708d7f011a529313d9ca` |
| `110` | 48 | `08af43847ab0e0e0305b03a6b0c34f04755323265b7e9a1124ee4aa8ba211da9` |
| `111` | 48 | `f9f1d73ea2fbffe0df74385e6361d767b48e27440d9eefe9dc512a26e72729b8` |
