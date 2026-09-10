# Git recovery drills

Nine repositories, each already broken in a way that will happen to you.
They are generated on demand, so you can break them again as often as you
like – there is nothing to be careful about.

```console
$ cd exercises/git/scenarios
$ ./make-scenario.sh list
$ ./make-scenario.sh unstage
Created /tmp/git-drills/unstage

$ cd /tmp/git-drills/unstage
$ cat TASK.md          # the goal
$ cd repo              # the broken repository
$ ...                  # your turn
$ ../check.sh          # did it work?
```

Each scenario directory contains:

| | |
|---|---|
| `TASK.md` | the situation and the goal |
| `repo/` | the repository to fix – `origin` is a local bare repo, so nothing needs network |
| `check.sh` | tells you which parts of the goal you have met |

Generate all nine at once with `./make-scenario.sh all`. Start over on any of
them by running the same command again.

Scenarios live under `/tmp/git-drills` – set `GIT_DRILLS_DIR` to put them
elsewhere.

---

## Work in this order

1. **unstage** – I staged a file I did not mean to include
2. **discard-one** – throw away one file's edits, keep the rest
3. **bad-message** – my last commit message is useless
4. **split-commit** – one commit contains two unrelated changes
5. **wrong-branch** – I committed to `main` instead of a feature branch
6. **deleted-branch** – I deleted a branch that still had commits on it
7. **revert-public** – a bad commit is already on `main`, and pushed
8. **lost-commit** – `reset --hard` threw away work I needed
9. **committed-secret** – I committed a `.env` file

The first five are the ones you will need this month. The last four are the
ones that make people panic.

---

## Before you touch anything

Two commands, every time:

```console
$ git status
$ git log --oneline --graph --all -8
```

You cannot choose the right recovery without knowing where you are. Most
Git disasters are a correct command applied to a misunderstood state.

---

## Hints

Read these after you have tried. One hint per drill, in increasing order of
how much it gives away.

### 1 unstage
- What is the opposite of `git add`? `git status` prints it for you.
- It is `git restore` with a flag.
- <details><summary>Answer</summary>

  ```console
  $ git restore --staged src/invoice.py
  ```
  The file keeps your edits – you only removed it from the next commit.
  </details>

### 2 discard-one
- `git restore` with no flag throws away working-tree changes.
- Name the one file. `git restore .` would take both.
- <details><summary>Answer</summary>

  ```console
  $ git restore src/invoice.py
  ```
  This one is genuinely irreversible: the change was never recorded anywhere.
  When you are not sure, `git stash push -m "maybe rubbish"` instead.
  </details>

### 3 bad-message
- You are replacing the last commit, not adding one.
- `--amend`.
- <details><summary>Answer</summary>

  ```console
  $ git commit --amend -m "Fix VAT rate for Belgian services"
  ```
  New hash, same content. Fine here because nothing was pushed.
  </details>

### 4 split-commit
- Undo the commit but keep the changes in your working tree, then commit
  twice.
- `git reset HEAD~1` (the default `--mixed`) unstages everything.
- <details><summary>Answer</summary>

  ```console
  $ git reset HEAD~1
  $ git add src/invoice.py
  $ git commit -m "Fix the VAT rate for Belgian services"
  $ git add README.md
  $ git commit -m "Document how to run the tests"
  ```
  `git reset --soft HEAD~1` keeps everything staged instead – then
  `git restore --staged README.md` before the first commit. Either is fine.
  </details>

### 5 wrong-branch
- A branch is a pointer. Create one here, then move `main` back.
- Order matters: make the branch *before* you move `main`.
- <details><summary>Answer</summary>

  ```console
  $ git branch feature/vat-free      # or: git switch -c feature/vat-free
  $ git switch main
  $ git reset --hard origin/main
  $ git switch feature/vat-free
  ```
  `reset --hard` is safe here only because everything is committed.
  </details>

### 6 deleted-branch
- `git branch -a` will not show it. The commit still exists; only the name
  is gone.
- Git records every position `HEAD` has held.
- <details><summary>Answer</summary>

  ```console
  $ git reflog
  ...
  9f2a7c1 HEAD@{2}: commit: Test the rounding rule
  $ git branch feature/rounding 9f2a7c1
  ```
  `git reflog --grep-reflog "rounding"` narrows it down if the log is long.
  </details>

### 7 revert-public
- Rewriting is not allowed: three people have pulled this.
- The undo has to be a new commit.
- <details><summary>Answer</summary>

  ```console
  $ git log --oneline -3
  $ git revert <the bad sha>
  $ git push
  ```
  The bad commit stays in the history, which is the point – the record shows
  what happened and what you did about it.
  </details>

### 8 lost-commit
- `git log` shows nothing because the branch no longer points at it. The
  object is still in `.git`.
- Same tool as drill 6.
- <details><summary>Answer</summary>

  ```console
  $ git reflog
  a3f9c21 HEAD@{1}: commit: Add rounding tests
  $ git reset --hard a3f9c21
  ```
  Or `git switch -c rescue a3f9c21` if you would rather look before you leap.
  Reflog entries are kept for 90 days by default, and are local to your clone.
  </details>

### 9 committed-secret
- Nothing is pushed, so this is one commit to fix.
- Stop tracking the file without deleting it, then replace the commit.
- <details><summary>Answer</summary>

  ```console
  $ git rm --cached .env
  $ echo ".env" >> .gitignore
  $ git add .gitignore
  $ git commit --amend --no-edit
  ```
  `git rm --cached` untracks and leaves the file on disk. `git rm` would
  delete it.

  If the secret is in *older* commits, or has been pushed, the order is
  different and the first step is not a Git command:

  1. Rotate the credential. Assume it is compromised.
  2. Tell whoever owns the system.
  3. `git filter-repo --invert-paths --path .env`, then force-push with the
     team's agreement. Everyone re-clones.
  </details>

---

## Two rules that cover almost everything

**If it was committed, you can get it back.** `git reflog` finds the hash;
`git branch <name> <hash>` gives it a name again.

**If it was never committed, no tool can help.** `git restore`,
`git checkout -- .`, `git clean -fd` and `git reset --hard` all destroy
uncommitted work silently. Commit early, or `git stash`, and there is nothing
left that can hurt you.
