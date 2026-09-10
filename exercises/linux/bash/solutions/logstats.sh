#!/usr/bin/env bash
# Summarises a pipeline log. Reference solution.
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <logfile>" >&2
    exit 1
fi

log="$1"

if [[ ! -f "$log" ]]; then
    echo "$0: no such file: $log" >&2
    exit 1
fi

echo "top errors:"
grep ERROR "$log" | awk '{print $4}' | sort | uniq -c | sort -rn | head -5

busiest=$(cut -d' ' -f2 "$log" | cut -d: -f1 | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')
echo "busiest hour: $busiest"
