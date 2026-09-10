#!/usr/bin/env bash
# Makes a dated archive of a directory. Reference solution.
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <source> [destination]" >&2
    exit 1
fi

source_dir="$1"
destination="${2:-/tmp/backups}"

if [[ ! -d "$source_dir" ]]; then
    echo "$0: no such directory: $source_dir" >&2
    exit 1
fi

mkdir -p "$destination"
archive="$destination/$(date +%F).tgz"

tar -czf "$archive" -C "$(dirname "$source_dir")" "$(basename "$source_dir")"
echo "Backed up $source_dir to $archive"
