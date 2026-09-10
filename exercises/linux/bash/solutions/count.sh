#!/usr/bin/env bash
# Counts what is in a directory. Reference solution.
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <directory>" >&2
    exit 1
fi

target="$1"

if [[ ! -d "$target" ]]; then
    echo "$0: no such directory: $target" >&2
    exit 1
fi

# wc pads its output on macOS, so strip the spaces.
files=$(find "$target" -type f | wc -l | tr -d ' ')
directories=$(find "$target" -mindepth 1 -type d | wc -l | tr -d ' ')
python_lines=$(find "$target" -name '*.py' -type f -exec cat {} + 2>/dev/null | wc -l | tr -d ' ')

echo "files: $files"
echo "directories: $directories"
echo "python lines: $python_lines"
