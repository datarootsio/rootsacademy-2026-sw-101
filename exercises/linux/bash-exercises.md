# Bash scripting exercises

Five scripts. Stubs are in `bash/`, and a test runner tells you when each one
is done.

```console
$ cd exercises/linux/bash
$ ./run-tests.sh greet          # one exercise
$ ./run-tests.sh                # all five
```

Reference solutions are in `bash/solutions/`. Check that the runner agrees
with them if you ever doubt a test: `./run-tests.sh --solutions`.

## The rules for all five

Start every file exactly like this:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

And then:

- **Quote every variable.** `"$1"`, not `$1`. A path with a space in it is not
  an edge case, it is Tuesday.
- **Usage errors go to stderr and exit 1.** `echo "usage: ..." >&2; exit 1`.
- **Validate before you act.** If the input directory does not exist, say so
  and stop – do not create it, and do not carry on with an empty variable.
- Run `shellcheck yourscript.sh` before you call it done. If it is not
  installed: `brew install shellcheck`.

---

## 1 – `greet.sh NAME`

Print a greeting that contains the name.

```console
$ ./greet.sh Charlotte
Hello, Charlotte!
$ ./greet.sh
usage: ./greet.sh <name>
$ echo $?
1
```

*Concepts: shebang, `chmod +x`, `$1`, `$#`, `>&2`, exit codes.*

---

## 2 – `count.sh DIRECTORY`

Report how many files, directories and lines of Python a directory contains,
at any depth. Exit 1 if the directory does not exist.

```console
$ ./count.sh ~/linux-playground
files: 20
directories: 10
python lines: 0
```

The three labels are what the tests look for, so keep them exactly as shown.

*Concepts: `find`, `wc -l`, command substitution, `[[ -d ]]`.*

> `wc -l` pads its output with spaces on macOS. `| tr -d ' '` fixes it.

---

## 3 – `backup.sh SOURCE [DESTINATION]`

Create `DESTINATION/YYYY-MM-DD.tgz` containing `SOURCE`. `DESTINATION`
defaults to `/tmp/backups` and should be created if it is missing. Refuse, with
exit 1, if `SOURCE` does not exist.

```console
$ ./backup.sh ~/linux-playground /tmp/mybackups
Backed up /Users/me/linux-playground to /tmp/mybackups/2026-02-14.tgz
```

*Concepts: `${2:-default}`, `$(date +%F)`, `tar -czf`, `mkdir -p`.*

> `tar -czf out.tgz /some/path` stores absolute paths, which is a nuisance to
> unpack. `tar -czf out.tgz -C "$(dirname "$src")" "$(basename "$src")"` stores
> just the directory. Worth knowing once.

---

## 4 – `newproject.sh NAME`

Create a Python project called `NAME`, ready for its first push:

- `src/` and `tests/`
- a `.gitignore` that covers `.venv/`, `__pycache__/`, `*.pyc` and `.env`
- a `README.md` naming the project and saying how to run the tests
- a virtual environment in `.venv`
- a Git repository with one commit containing everything except the ignored
  files

Refuse if `NAME` already exists, and exit 1 with no argument.

```console
$ ./newproject.sh billing
Created billing
$ cd billing && git log --oneline
a3f9c21 Initial project layout
$ git status --short        # nothing – .venv is ignored
```

That last line is the interesting test. If `git status` is dirty, your
`.gitignore` was written after `git add`.

*Concepts: `mkdir -p`, heredocs, `python3 -m venv`, `git init`, ordering.*

---

## 5 – `logstats.sh LOGFILE` (bonus)

Summarise a log. Pipes only – no Python.

```console
$ ./logstats.sh ~/linux-playground/logs/pipeline.log
top errors:
  10 invoice
   4 loader
   1 vat
busiest hour: 09
```

The module is the fourth field of a log line. The hour is the first two
characters of the time.

*Concepts: `grep`, `awk '{print $4}'`, `cut`, `sort | uniq -c | sort -rn`,
`head`.*

---

## Hints

<details>
<summary>1 greet</summary>

```bash
if [[ $# -lt 1 ]]; then
    echo "usage: $0 <name>" >&2
    exit 1
fi

echo "Hello, $1!"
```
`$0` is the script's own name, so the usage line stays correct if the file is
renamed.
</details>

<details>
<summary>2 count</summary>

```bash
files=$(find "$target" -type f | wc -l | tr -d ' ')
```
`find -mindepth 1 -type d` excludes the directory you started from.
For the Python lines: `find "$target" -name '*.py' -exec cat {} + | wc -l`.
</details>

<details>
<summary>3 backup</summary>

```bash
destination="${2:-/tmp/backups}"
mkdir -p "$destination"
archive="$destination/$(date +%F).tgz"
tar -czf "$archive" -C "$(dirname "$source_dir")" "$(basename "$source_dir")"
```
</details>

<details>
<summary>4 newproject</summary>

Order matters: write `.gitignore` **before** `python3 -m venv`, or at least
before `git add`. A heredoc keeps the file readable:

```bash
cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.pyc
.env
EOF
```
The quoted `<<'EOF'` stops the shell expanding anything inside. Use unquoted
`<<EOF` only when you *want* `$name` substituted – as in the README.
</details>

<details>
<summary>5 logstats</summary>

```bash
grep ERROR "$log" | awk '{print $4}' | sort | uniq -c | sort -rn | head -5
cut -d' ' -f2 "$log" | cut -d: -f1 | sort | uniq -c | sort -rn | head -1
```
Two `cut`s: the first takes the time field, the second takes the hour out of
it. `uniq -c` needs sorted input, always.
</details>

---

## When to stop writing bash

Exercise 5 is close to the line. If it had needed to parse a date, compare two
timestamps, or emit JSON, the right answer would have been a 20-line Python
script. Bash is for gluing programs together in order; the moment you need
arithmetic, data structures or a second nested `if`, switch.
