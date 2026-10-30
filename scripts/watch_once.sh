#!/usr/bin/env bash
# For a scheduled task: one market snapshot + threshold alerts, exit non-zero on alert.
set -euo pipefail
cd "$(dirname "$0")/.."
out=$(python -m yf.cli watch --once 2>&1)
echo "$out"
echo "$out" | grep -q '^ALERT:' && exit 3 || exit 0
