#!/usr/bin/env bash
# Creates a Python project, ready to commit. Reference solution.
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <project-name>" >&2
    exit 1
fi

name="$1"

if [[ -e "$name" ]]; then
    echo "$0: $name already exists" >&2
    exit 1
fi

mkdir -p "$name/src" "$name/tests"
cd "$name"

cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.pyc
.env
.DS_Store
EOF

cat > README.md <<EOF
# $name

## Running locally

    source .venv/bin/activate
    python3 -m pytest
EOF

python3 -m venv .venv

git init -q
git add -A
git commit -qm "Initial project layout"

echo "Created $name"
