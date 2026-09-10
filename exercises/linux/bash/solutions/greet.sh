#!/usr/bin/env bash
# Greets someone by name. Reference solution.
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <name>" >&2
    exit 1
fi

echo "Hello, $1!"
