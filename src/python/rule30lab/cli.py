"""Primary Rule 30 command-line interface."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence

from . import __version__
from .core import center_bits_cell_array


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rule30", description="Rule 30 research CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subcommands = parser.add_subparsers(dest="command", required=True)

    generate = subcommands.add_parser("generate", help="generate a center-sequence prefix")
    generate.add_argument("--count", type=int, required=True, help="number of bits c_0 onward")
    generate.add_argument(
        "--backend", choices=("python",), default="python", help="verified backend"
    )
    generate.add_argument("--json", action="store_true", help="emit structured JSON")

    subcommands.add_parser("verify", help="run cross-backend reference verification")
    subcommands.add_parser("benchmark", help="run comparable representative benchmarks")
    subcommands.add_parser("balance", help="compute balance and discrepancy")
    subcommands.add_parser("blocks", help="measure finite block frequencies")
    subcommands.add_parser("autocorrelation", help="measure serial autocorrelation")
    subcommands.add_parser("linear-complexity", help="run binary Berlekamp-Massey")
    subcommands.add_parser("period-search", help="search bounded candidate periods")
    subcommands.add_parser("sideways-reconstruct", help="reconstruct a finite left triangle")
    subcommands.add_parser("automaticity-search", help="run finite automaticity diagnostics")
    subcommands.add_parser("predictor-search", help="search finite exact predictors")

    experiment = subcommands.add_parser("experiment", help="run or reproduce an experiment")
    experiment_commands = experiment.add_subparsers(dest="experiment_command", required=True)
    experiment_commands.add_parser("run")
    experiment_commands.add_parser("reproduce")
    return parser


def _generate(args: argparse.Namespace) -> int:
    bits = center_bits_cell_array(args.count)
    bit_string = "".join(str(bit) for bit in bits)
    if args.json:
        payload = {
            "backend": args.backend,
            "bit_order": "c_0_to_c_n_minus_1",
            "bits": bit_string,
            "count": len(bits),
            "sha256_u8": hashlib.sha256(bits).hexdigest(),
        }
        print(json.dumps(payload, sort_keys=True))
    else:
        print(bit_string)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.command == "generate":
        return _generate(args)
    parser.error(f"command {args.command!r} is scaffolded but not implemented yet")
    return 2


if __name__ == "__main__":
    sys.exit(main())
