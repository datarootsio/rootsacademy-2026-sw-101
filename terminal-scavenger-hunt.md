# Terminal scavenger hunt

Twelve questions about a directory tree you have never seen, one command each.
Ten minutes in class; finish the rest at home.

```console
$ cd exercises/linux
$ ./setup-playground.sh
Playground ready at ~/linux-playground

$ cd ~/linux-playground
```

## Rules

- **Terminal only.** No editor, no Finder, no file manager, no VS Code sidebar.
- Write down **the command**, not just the answer. The command is the point.
- One command per question. Pipes are one command.
- 1 point for the answer, 1 bonus point for the shortest correct command in
  the room.

Run `./setup-playground.sh` again at any time to reset everything.

---

## The questions

1. How many **files** are there in total, at any depth?
2. How many **directories**, not counting the playground root itself?
3. Which file is the **largest**?
4. How many **lines** does `logs/pipeline.log` have?
5. How many of those lines are **errors**?
6. Which **module** produced the most errors, and how many? <br>
   <span style="opacity:.7">(the module is the fourth field of each log line)</span>
7. How many times does the word **`timeout`** appear in `etc/app.conf`?
8. One script is **executable but empty**. Which?
9. One file is readable **only by its owner**. Which?
10. There are two **hidden** files. Find the one in the deepest directory, and
    read it.
11. `data/raw/invoices.csv` has a header row. How many **data rows** are there,
    and how many **distinct customers**?
12. Which file was **modified most recently**?

### Bonus holes

13. How many invoices are Belgian (`country` is `BE`)?
14. Print the three highest invoice amounts, largest first.
15. Every log line mentioning `timeout`, with its line number, and nothing else.

---

## Answers

Try all twelve before opening this.

<details>
<summary>Show the answer sheet</summary>

Several of these have more than one right command. The one shown is the short
one; if yours produced the same answer, take the point.

**1 – 20 files**
```console
$ find . -type f | wc -l
```
`find` without `-type f` also counts directories.

**2 – 10 directories**
```console
$ find . -mindepth 1 -type d | wc -l
```
`-mindepth 1` is what excludes `.` itself.

**3 – `data/raw/big_export.bin`**
```console
$ ls -S $(find . -type f) | head -1
$ du -a . | sort -rn | head -2      # also fine
```

**4 – 51 lines**
```console
$ wc -l < logs/pipeline.log
```
`wc -l logs/pipeline.log` also prints the filename; `<` gives you the number
alone.

**5 – 15 errors**
```console
$ grep -c ERROR logs/pipeline.log
```

**6 – `invoice`, with 10**
```console
$ grep ERROR logs/pipeline.log | awk '{print $4}' | sort | uniq -c | sort -rn
  10 invoice
   4 loader
   1 vat
```
This pipeline – filter, extract, group, count, rank – is the single most
useful thing in this document. You will use it every week.

**7 – 3 times**
```console
$ grep -c timeout etc/app.conf
```
Careful: `grep -c` counts *lines*, not occurrences. They happen to be equal
here. For true occurrences: `grep -o timeout etc/app.conf | wc -l`.

**8 – `bin/rollback.sh`**
```console
$ find . -type f -perm -u+x -size 0
```
`-size 0` means zero blocks, i.e. empty. `-perm -u+x` means "at least
user-executable".

**9 – `etc/secrets.conf`**
```console
$ find . -type f -perm 600
$ ls -l etc/                        # also fine, if you know where to look
```
Mode 600 is `rw-------`: the mode every private key and credential file
should have.

**10 – `archive/2024/q3/reports/.passphrase`, containing `ROOTSACADEMY-2026`**
```console
$ find . -name ".*" -type f
$ cat archive/2024/q3/reports/.passphrase
```
`ls` hides dotfiles; `ls -a` shows them. `find -name ".*"` finds them at any
depth.

**11 – 240 rows, 17 distinct customers**
```console
$ tail -n +2 data/raw/invoices.csv | wc -l
$ tail -n +2 data/raw/invoices.csv | cut -d, -f2 | sort -u | wc -l
```
`tail -n +2` means "from line 2 onwards" – the standard way to skip a header.
`sort -u` before counting, because `uniq` only removes *adjacent* duplicates.

**12 – `data/clean/TODO.txt`**
```console
$ ls -t $(find . -type f) | head -1
$ find . -type f -newer logs/pipeline.log     # another angle
```

**13 – 80 Belgian invoices**
```console
$ grep -c ",BE$" data/raw/invoices.csv
```

**14**
```console
$ tail -n +2 data/raw/invoices.csv | cut -d, -f3 | sort -rn | head -3
1683.50
1676.50
1669.50
```

**15**
```console
$ grep -n timeout logs/pipeline.log
```
`-n` prefixes the line number. Add `-o` to print only the matching text.

</details>

---

## What to take away

Four commands answered almost every question: `find`, `grep`, `wc` and
`sort | uniq -c`. Add `cut` and `awk '{print $n}'` and you can answer most
questions anyone will ask you about a machine you have just logged into.

Nobody remembers the flags. `man find`, `grep --help`, and – if it is
installed – `tldr find` for the five examples you actually wanted.
