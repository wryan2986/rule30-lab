#!/usr/bin/env bash
# =========================================================================
# run_astra_8h.sh — Legacy wrapper for run_astra_supervisor.sh
# =========================================================================
# This script now delegates to the new supervisor.
#   ./run_astra_8h.sh              → 8h soft deadline (default)
#   ./run_astra_8h.sh --hours 16   → 16h soft deadline
#   ./run_astra_8h.sh --continuous → run until stop condition
#
# For direct access to all options, use run_astra_supervisor.sh.
# =========================================================================
exec bash "$(dirname "$0")/run_astra_supervisor.sh" "$@"
