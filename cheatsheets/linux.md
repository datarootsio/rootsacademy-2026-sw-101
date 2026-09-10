# Linux and bash – one page

## Getting around

```console
$ pwd                    where am I
$ ls -lah                long, hidden, human sizes
$ ls -lt                 newest first
$ cd path   cd ..   cd ~   cd -          (- is the previous directory)
$ tree -L 2              if installed
```

`.` here · `..` up · `~` home · `/` root · `-` previous

**Press Tab.** It completes paths and will not complete what does not exist.

## Looking at files

```console
$ head -20 file          $ tail -20 file        $ tail -f file
$ less file              q quits, / searches, n next, G end
$ cat file               only for small files
$ wc -l file             count lines
$ file mystery           what kind of thing is this
$ stat file              size, dates, permissions
```

## Changing things

```console
$ mkdir -p a/b/c         $ touch file
$ cp src dst             $ cp -r dir/ dst/
$ mv src dst             (also renames)
$ rm file                $ rm -r dir/       no undo, no bin, no confirmation
$ rm -i file             ask first
```

`ls` the pattern before you `rm` it.

## Finding

```console
$ find . -name "*.csv"           by name (quote the pattern)
$ find . -iname "*readme*"       any case
$ find . -type d -name "test*"   directories only
$ find . -size +100M             $ find . -mtime -1        last 24h

$ grep ERROR file                $ grep -i error file
$ grep -n ERROR file             line numbers
$ grep -c ERROR file             count
$ grep -v DEBUG file             invert
$ grep -r "TEXT" src/            recursive
$ grep -A2 -B2 ERROR file        with context
```

`find` looks at names. `grep` looks inside files.

## Pipes and redirection

```console
$ a | b            b reads a's output
$ cmd > file       write (truncates!)      $ cmd >> file    append
$ cmd < file       read from file
$ cmd 2> err.log   errors only             $ cmd > all 2>&1  both
$ cmd 2> /dev/null discard errors
$ cmd | tee file   screen and file
```

0 stdin · 1 stdout · 2 stderr

```console
$ grep ERROR log | awk '{print $4}' | sort | uniq -c | sort -rn | head -5
      filter    →    extract    →   group  →  count  →  rank  →  top 5
```

`uniq` only removes *adjacent* duplicates: it is always `sort | uniq`.

## Text tools

```console
$ sort -rn        reverse numeric      $ uniq -c        count runs
$ cut -d, -f2,5   pick CSV columns     $ tr 'a-z' 'A-Z'
$ sed 's/old/new/g' file               $ awk -F, '{print $2}' file
$ tail -n +2 file                      skip a header row
$ xargs rm                             turn stdin into arguments
```

## Permissions

```
-rwxr-xr-x   type · user rwx · group rwx · other rwx
     r=4  w=2  x=1        on a directory, x means "may enter"
```

```console
$ chmod +x script.sh     $ chmod 755 script.sh
$ chmod 644 file         ordinary file
$ chmod 600 ~/.ssh/id_ed25519    a secret
$ chown user:group file  (needs sudo)
```

`777` is never the fix. Work out which permission is actually missing.

## Processes

```console
$ ps aux | grep python   $ top    $ htop
$ cmd &                  background      $ jobs    $ fg %1
$ kill PID               $ kill -9 PID   $ pkill -f pattern
$ nohup cmd &            survives logout
```

| Ctrl+C | stop this command | Ctrl+D | end of input / log out |
|---|---|---|---|
| **Ctrl+R** | **search history** | Ctrl+A / E | start / end of line |
| Ctrl+L | clear screen | Ctrl+Z | suspend, then `fg` |

## Environment

```console
$ echo $HOME  $PATH      $ env | sort
$ export TOKEN="abc"     this shell only
$ which python3          which one is actually running
$ source ~/.zshrc        reload your config (.bashrc on Linux)
```

Never put a secret in `.bashrc` or in your shell history.

## Bash scripting

```bash
#!/usr/bin/env bash
set -euo pipefail          # e: stop on error  u: no unset vars  pipefail

name="Charlotte"           # no spaces around =
today=$(date +%F)          # command output
count=$((2 + 3))           # arithmetic

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <name>" >&2
    exit 1
fi

target="${2:-/tmp}"        # $2, or a default

if [[ -f "$path" ]]; then ... elif [[ -d "$path" ]]; then ... fi
if [[ "$env" == "prod" ]]; then ... fi
if [[ $count -gt 10 ]]; then ... fi
if grep -q ERROR log; then ... fi

for file in data/*.csv; do echo "$file"; done
for i in {1..5}; do echo "$i"; done
while read -r line; do echo "$line"; done < names.txt

log() { echo "[$(date +%T)] $*" >&2; }

case "${1:-}" in
    start) ... ;;
    stop)  ... ;;
    *) echo "usage: $0 start|stop" >&2; exit 1 ;;
esac
```

| `$0` | script name | `$1 $2` | arguments | `$#` | how many |
|---|---|---|---|---|---|
| `"$@"` | all of them | `$?` | last exit code | `$*` | all, as one string |

**Exit 0 means success.** Anything else is a failure.

**Quote every variable.** `rm $file` with `file="My Report.csv"` deletes two
wrong things. `rm "$file"` does not.

`[[ ]]` not `[ ]`. Run `shellcheck` before you keep a script.

## SSH

```console
$ ssh-keygen -t ed25519 -C "you@laptop"    set a passphrase
$ ssh-copy-id user@host                    install the public key
$ ssh user@host                            $ ssh user@host "df -h"
$ ssh-add ~/.ssh/id_ed25519                type the passphrase once
$ ssh -T git@github.com                    check your GitHub key

$ scp file host:/path/         one file
$ rsync -avz --progress dir/ host:/path/   a directory, resumable
```

```
# ~/.ssh/config
Host etl
    HostName prod-etl-01.example.com
    User charlotte
    IdentityFile ~/.ssh/id_ed25519
```

`chmod 600 ~/.ssh/id_ed25519` and `chmod 700 ~/.ssh` – SSH enforces this.
The private key never leaves your machine.

## Getting help

```console
$ ls --help      $ man ls      $ tldr ls      $ type ls
```
