# Git games

Three games. The first needs pairs and a shared repository, the other two work
alone or in teams.

---

## Game 1 – Conflict duel

**Pairs, 15 minutes in class, needs the shared course repository**

Two people, one file, the same seven lines, on purpose. The point is not to
avoid the conflict – it is to resolve one without losing anyone's work.

### Setup

Player A creates the battleground on `main` (once, for the pair):

```console
$ git switch main && git pull
$ mkdir -p duel
$ cat > duel/greeting.py <<'PY'
def greet(name):
    return "Hello " + name


if __name__ == "__main__":
    print(greet("world"))
PY
$ git add duel/greeting.py
$ git commit -m "Add a greeting to fight over"
$ git push
```

Player B: `git switch main && git pull`.

Then **both** of you:

```console
$ git switch -c duel/<your-name>
```

### Round 1

Both of you rewrite `greet` in your own style, touching the same lines. Aim
for changes that are both defensible:

- A: use an f-string, and handle an empty name by returning `"Hello there"`.
- B: use an f-string, add a `greeting="Hello"` parameter, and add a type hint.

Commit and push:

```console
$ git add duel/greeting.py
$ git commit -m "Improve the greeting"
$ git push -u origin duel/<your-name>
```

Player A merges first and wins the race:

```console
$ git switch main && git pull
$ git merge duel/<A>
$ git push
```

Player B now has a conflict:

```console
$ git switch duel/<B>
$ git fetch
$ git merge origin/main
CONFLICT (content): Merge conflict in duel/greeting.py
```

**Player B's job:** resolve it so that *both* intentions survive – the empty
name handling *and* the greeting parameter. Then merge to `main` and push.

### Round 2 (take home)

Swap roles. This time make **three commits each** before merging, touching
overlapping lines in each one. Notice how much harder it gets, and how much
of that difficulty came from waiting.

### Scoring

| | |
|---:|---|
| +3 | the resolution keeps both intentions |
| +2 | `python3 duel/greeting.py` still runs afterwards |
| +1 | the merge commit message explains the choice you made |
| −5 | a `<<<<<<<` marker reaches `main` |
| −5 | `git push --force` on `main` |
| −3 | you solved it by taking one side wholesale and deleting the other's work |

### Debrief questions

- What would have prevented the round 2 pain? (Answer: merging `main` into
  your branch daily, and smaller commits.)
- Whose version does `--ours` mean during a merge? During a rebase? (They are
  opposite. This is why people mistrust rebase.)

---

## Game 2 – Git golf

**Solo or teams, take home, use any drill repository as a course**

Nine holes. Reach the described state in the **fewest commands**. Everyone
reveals their solution at the same time; shortest correct answer wins the
hole. Ties are broken by whose history a reviewer would rather read.

A "command" is one line starting with `git`. Editing a file does not count.

| Hole | Par | Get from | To |
|---|---|---|---|
| 1 | 1 | a modified, unstaged file | committed |
| 2 | 1 | on `main` | on a new branch `feature/x`, at the same commit |
| 3 | 1 | three staged files | only one of them staged |
| 4 | 1 | last commit has a typo in the message | message fixed, same content |
| 5 | 2 | two commits at the tip | one commit with both changes |
| 6 | 1 | a commit on `main` you want on a branch | on the branch, `main` clean |
| 7 | 2 | one commit from another branch | copied onto yours, other branch untouched |
| 8 | 1 | half-finished work, need to switch branch now | work saved, tree clean |
| 9 | 2 | a deleted branch's two commits | a branch pointing at them again |

Under par is possible on several holes. `git switch -c` does two things at
once, and so does `git commit -am`.

**House rule:** a one-command solution that loses somebody's work scores zero.

---

## Game 3 – Blame detective

**Teams of two or three, take home**

A repository with real history, one bug, and no idea who put it there. Find
out, using only Git.

### Setup

```console
$ cd exercises/git/scenarios
$ ./make-scenario.sh revert-public
$ cd /tmp/git-drills/revert-public/repo
```

The symptom: `total(100)` returns `100.0`. It should return `121.0`.

### Your questions

1. Which line is wrong?
2. Which commit introduced it – hash, author, date?
3. What did that commit's message claim it was doing?
4. There is a test that should have caught this. Find it, run it, and
   explain how the commit landed anyway.
5. What is the correct fix, given that the commit is already pushed?

### Your tools

```console
$ git blame src/invoice.py           # who last touched each line
$ git log -S "VAT_RATE" --oneline    # commits that added or removed that text
$ git log -p src/invoice.py          # every change to one file, with diffs
$ git show <sha>                     # one commit in full
$ git bisect start                   # binary search, for when the above fails
```

### Deliverable

A three-line incident note, committed to your branch as `INCIDENT.md`:

```
What broke:    <one sentence, with the observable symptom>
Which commit:  <hash> - <author>, <date> - "<subject>"
What we did:   <the fix, and why that fix and not another>
```

That is the note a real on-call engineer writes, and writing it is most of the
skill.

### Going further

On a repository with a longer history, `git bisect` finds the culprit in
`log₂(n)` tests. Try it on the course repository:

```console
$ git bisect start
$ git bisect bad                     # the current commit is broken
$ git bisect good <an old sha>       # this one was fine
# Git checks out the midpoint; you run the test and answer good or bad
$ git bisect good
$ ...
$ git bisect reset                   # always finish with this
```

400 commits, 9 tests, one answer.

---

## Worth an evening

**learngitbranching.js.org** – a visual sandbox where the commit graph moves
as you type real commands. The best 40 minutes you can spend on Git.
