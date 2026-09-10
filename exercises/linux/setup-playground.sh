#!/usr/bin/env bash
# Builds the directory tree used by the terminal scavenger hunt.
# Safe to re-run: it removes and rebuilds the playground.

set -euo pipefail

ROOT="${LINUX_PLAYGROUND:-$HOME/linux-playground}"

rm -rf "$ROOT"
mkdir -p "$ROOT"/{logs,data/raw,data/clean,bin,etc,archive/2024/q3/reports}

# --- logs -------------------------------------------------------------------

{
    for hour in 08 09 10 11 12 13 14; do
        for minute in 03 17 31 44 58; do
            echo "2026-02-14 $hour:$minute:00 INFO  loader     batch accepted"
        done
    done
    for i in 1 2 3 4 5 6 7 8 9; do
        echo "2026-02-14 09:1$i:00 ERROR invoice    connection timeout after 30s"
    done
    for i in 1 2 3 4; do
        echo "2026-02-14 11:2$i:00 ERROR loader     malformed row, skipping"
    done
    echo "2026-02-14 11:59:00 ERROR vat        rate lookup returned nothing"
    echo "2026-02-14 12:00:00 WARN  vat        falling back to 21%"
    echo "2026-02-14 13:07:00 ERROR invoice    connection timeout after 30s"
} > "$ROOT/logs/pipeline.log"

printf 'starting\nready\n' > "$ROOT/logs/startup.log"
: > "$ROOT/logs/empty.log"

# --- data -------------------------------------------------------------------

{
    echo "invoice_id,customer,amount,country"
    for i in $(seq 1 240); do
        echo "INV-$i,customer_$((i % 17)),$((i * 7 + 3)).50,$( [[ $((i % 3)) -eq 0 ]] && echo BE || echo NL )"
    done
} > "$ROOT/data/raw/invoices.csv"

head -60 "$ROOT/data/raw/invoices.csv" > "$ROOT/data/clean/invoices_be.csv"
dd if=/dev/zero of="$ROOT/data/raw/big_export.bin" bs=1024 count=1400 status=none

# --- scripts ----------------------------------------------------------------

cat > "$ROOT/bin/deploy.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "pretending to deploy"
EOF
chmod 755 "$ROOT/bin/deploy.sh"

: > "$ROOT/bin/rollback.sh"
chmod 755 "$ROOT/bin/rollback.sh"          # executable and empty: question 8

cat > "$ROOT/bin/notes.sh" <<'EOF'
#!/usr/bin/env bash
echo "this one is not executable"
EOF
chmod 644 "$ROOT/bin/notes.sh"

# --- config -----------------------------------------------------------------

cat > "$ROOT/etc/app.conf" <<'EOF'
[server]
host = 0.0.0.0
port = 8080
timeout = 30

[database]
host = db.internal
timeout = 5
pool_size = 10

[retry]
attempts = 3
timeout = 45
EOF

cat > "$ROOT/etc/secrets.conf" <<'EOF'
# not a real credential
api_token = not_a_real_token_0000
EOF
chmod 600 "$ROOT/etc/secrets.conf"         # the only 600 file: question 9

# --- hidden and deep --------------------------------------------------------

printf 'nothing to see here\n' > "$ROOT/.hidden_note"
printf 'ROOTSACADEMY-2026\n' > "$ROOT/archive/2024/q3/reports/.passphrase"
printf 'q3 revenue summary\n' > "$ROOT/archive/2024/q3/reports/summary.txt"

for name in alpha beta gamma delta; do
    printf 'placeholder\n' > "$ROOT/archive/2024/$name.txt"
done

cat > "$ROOT/HUNT.md" <<'EOF'
# Terminal scavenger hunt

Twelve questions. One command each – no editors, no Finder, no file manager.

Write down the command you used, not just the answer. Bonus points go to the
shortest correct command.

Questions and the answer sheet: exercises/linux/terminal-scavenger-hunt.md
EOF

# Written last, so it is unambiguously the newest file: question 12.
printf 'remember to rotate the api token\n' > "$ROOT/data/clean/TODO.txt"

echo "Playground ready at $ROOT"
echo "  cd $ROOT && cat HUNT.md"
