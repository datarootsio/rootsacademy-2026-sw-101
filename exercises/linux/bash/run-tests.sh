#!/usr/bin/env bash
# Checks the bash exercises. Run with a script name, or with no argument for all.
#
#   ./run-tests.sh greet
#   ./run-tests.sh
#   ./run-tests.sh --solutions      # check the reference solutions instead

set -uo pipefail

cd "$(dirname "$0")"

DIR="."
if [[ "${1:-}" == "--solutions" ]]; then
    DIR="solutions"
    shift
fi

EXERCISES=(greet count backup newproject logstats)
PASSED=0
FAILED=0
SCRIPT=""

ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; PASSED=$((PASSED + 1)); }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$1"; FAILED=$((FAILED + 1)); [[ -n "${2:-}" ]] && printf '      %s\n' "$2"; }

# expect_stdout <description> <substring> <args...>
expect_stdout() {
    local what="$1" needle="$2"; shift 2
    local out flat
    out="$("$SCRIPT" "$@" 2>/dev/null)"
    # Squeeze whitespace: the exercise is the count, not wc's padding.
    flat="$(tr -s '[:space:]' ' ' <<< "$out")"
    if [[ "$flat" == *"$needle"* ]]; then ok "$what"; else bad "$what" "expected to see '$needle', got: ${out:-<nothing>}"; fi
}

# expect_exit <description> <code> <args...>
expect_exit() {
    local what="$1" want="$2"; shift 2
    "$SCRIPT" "$@" >/dev/null 2>&1
    local got=$?
    if [[ $got -eq $want ]]; then ok "$what"; else bad "$what" "expected exit $want, got $got"; fi
}

# expect_stderr <description> <substring> <args...>
expect_stderr() {
    local what="$1" needle="$2"; shift 2
    local err
    err="$("$SCRIPT" "$@" 2>&1 >/dev/null)"
    if [[ "$err" == *"$needle"* ]]; then ok "$what"; else bad "$what" "expected stderr to mention '$needle', got: ${err:-<nothing>}"; fi
}

# --- fixtures ---------------------------------------------------------------

make_tree() {
    local root
    root="$(mktemp -d)"
    mkdir -p "$root/pkg"
    printf 'a\nb\nc\n' > "$root/pkg/one.py"
    printf 'x\ny\n' > "$root/two.py"
    printf 'notes\n' > "$root/readme.txt"
    echo "$root"
}

make_log() {
    local log
    log="$(mktemp)"
    {
        echo "2026-02-14 09:01:00 ERROR invoice    timeout"
        echo "2026-02-14 09:02:00 ERROR invoice    timeout"
        echo "2026-02-14 09:03:00 ERROR invoice    timeout"
        echo "2026-02-14 09:04:00 INFO  loader     ok"
        echo "2026-02-14 11:01:00 ERROR loader     bad row"
        echo "2026-02-14 11:02:00 INFO  loader     ok"
    } > "$log"
    echo "$log"
}

# --- the tests --------------------------------------------------------------

test_greet() {
    expect_stdout "greets by name"            "Charlotte" Charlotte
    expect_exit   "exits 0 with a name"       0           Charlotte
    expect_exit   "exits 1 with no argument"  1
    expect_stderr "prints usage on stderr"    "usage"
}

test_count() {
    local tree; tree="$(make_tree)"
    expect_stdout "counts files"          "files: 3"         "$tree"
    expect_stdout "counts directories"    "directories: 1"   "$tree"
    expect_stdout "counts python lines"   "python lines: 5"  "$tree"
    expect_exit   "exits 1 on a missing directory" 1 "$tree/nope"
    expect_exit   "exits 1 with no argument"       1
    rm -rf "$tree"
}

test_backup() {
    local tree dest; tree="$(make_tree)"; dest="$(mktemp -d)"
    expect_exit "exits 0 on a real directory" 0 "$tree" "$dest"
    if [[ -f "$dest/$(date +%F).tgz" ]]; then
        ok "wrote <destination>/$(date +%F).tgz"
    else
        bad "wrote <destination>/$(date +%F).tgz" "nothing matching that name in $dest"
    fi
    if tar -tzf "$dest/$(date +%F).tgz" 2>/dev/null | grep -q "one.py"; then
        ok "the archive contains the files"
    else
        bad "the archive contains the files" "one.py is not in the archive"
    fi
    expect_exit "exits 1 on a missing source" 1 "$tree/nope" "$dest"
    expect_exit "exits 1 with no argument"    1
    rm -rf "$tree" "$dest"
}

test_newproject() {
    local sandbox; sandbox="$(mktemp -d)"
    local script; script="$(cd "$(dirname "$SCRIPT")" && pwd)/$(basename "$SCRIPT")"
    ( cd "$sandbox" && "$script" demo >/dev/null 2>&1 )
    for path in demo/src demo/tests demo/.gitignore demo/README.md demo/.venv/bin; do
        if [[ -e "$sandbox/$path" ]]; then ok "created $path"; else bad "created $path"; fi
    done
    if git -C "$sandbox/demo" log --oneline >/dev/null 2>&1; then
        ok "made an initial commit"
    else
        bad "made an initial commit" "no git history in demo/"
    fi
    if [[ -n "$(git -C "$sandbox/demo" status --porcelain 2>/dev/null)" ]]; then
        bad "nothing left uncommitted" "git status is not clean – is .venv/ ignored?"
    else
        ok "nothing left uncommitted"
    fi
    expect_exit "exits 1 with no argument" 1
    rm -rf "$sandbox"
}

test_logstats() {
    local log; log="$(make_log)"
    expect_stdout "names the worst module" "invoice"        "$log"
    expect_stdout "counts its errors"      "3"              "$log"
    expect_stdout "reports the busiest hour" "busiest hour: 09" "$log"
    expect_exit   "exits 1 on a missing file" 1 "$log.nope"
    expect_exit   "exits 1 with no argument"  1
    rm -f "$log"
}

# --- driver -----------------------------------------------------------------

run_one() {
    local name="$1"
    SCRIPT="$DIR/$name.sh"
    printf '\n%s.sh\n' "$name"
    if [[ ! -f "$SCRIPT" ]]; then
        bad "$name.sh exists" "create $SCRIPT"
        return
    fi
    if [[ ! -x "$SCRIPT" ]]; then
        bad "$name.sh is executable" "run: chmod +x $SCRIPT"
        return
    fi
    "test_$name"
}

targets=("$@")
if [[ ${#targets[@]} -eq 0 ]]; then
    targets=("${EXERCISES[@]}")
fi

for name in "${targets[@]}"; do
    case " ${EXERCISES[*]} " in
        *" $name "*) run_one "$name" ;;
        *) echo "unknown exercise: $name (try: ${EXERCISES[*]})" >&2; exit 2 ;;
    esac
done

printf '\n%d passed, %d failed\n' "$PASSED" "$FAILED"
[[ $FAILED -eq 0 ]]
