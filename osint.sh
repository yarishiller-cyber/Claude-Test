#!/usr/bin/env bash
#
# osint.sh — thin wrapper around Sherlock (sherlock-project) for username OSINT.
#
# Sherlock takes a USERNAME (not a photo) and checks ~400 social networks for
# an account with that handle. This wrapper just runs it out of the local
# virtualenv and drops results into ./results/.
#
# Setup (one time):   ./osint.sh --setup
# Usage:              ./osint.sh <username> [<username> ...] [sherlock flags]
# Examples:
#   ./osint.sh torvalds
#   ./osint.sh alice bob --csv
#   ./osint.sh someuser --site GitHub --site Instagram --print-all
#
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$HERE/.venv"
OUTDIR="$HERE/results"

if [[ "${1:-}" == "--setup" ]]; then
  echo "[*] Creating virtualenv at $VENV"
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --upgrade pip -q
  "$VENV/bin/pip" install sherlock-project -q
  echo "[*] Done. Sherlock version: $("$VENV/bin/sherlock" --version | head -1)"
  exit 0
fi

if [[ ! -x "$VENV/bin/sherlock" ]]; then
  echo "[!] Sherlock isn't installed yet. Run: ./osint.sh --setup" >&2
  exit 1
fi

if [[ $# -eq 0 ]]; then
  echo "Usage: ./osint.sh <username> [<username> ...] [sherlock flags]" >&2
  echo "       ./osint.sh --setup    (first-time install)" >&2
  exit 1
fi

mkdir -p "$OUTDIR"
exec "$VENV/bin/sherlock" --folderoutput "$OUTDIR" "$@"
