# Exercises

Everything here is self-checking. Nothing needs the network.

Git comes first in the day, so everything you write afterwards can be
committed, pushed and reviewed as you go.

The day is six hours, so each exercise block in class is a taste rather than
the whole thing. Finishing them afterwards is expected, not a sign you fell
behind. Three blocks are take-home by design: the Python classes exercises,
`09_pipeline.py`, and the bash scripts.

## Git

```console
$ cd exercises/git/scenarios
$ ./make-scenario.sh list
$ ./make-scenario.sh unstage
```

Nine repositories, each already broken. Every one comes with a `TASK.md`
describing the goal and a `check.sh` that tells you when you have met it.
They are generated under `/tmp/git-drills` and are completely disposable –
run the generator again to start over.

| | |
|---|---|
| `git-drills.md` | the nine drills, with hints |
| `scenarios/make-scenario.sh` | generates them |
| `git-games.md` | conflict duel, git golf, blame detective |

## Python

```console
$ cd exercises/python
$ python3 01_basics.py
```

Each file has stubbed functions and a block of `assert`s at the bottom. Fill
in a function, run the file, and it tells you which exercise now passes. When
the last line prints, you are done with that file.

`08_design.py` works differently: most of its code already runs, and the
assertions test the *shape* of it. One fails while a business rule is written
in three places, one if you add a format by editing the dispatcher, one while
a dependency is still hard-coded. So it fails before you have changed
anything – that is the exercise, not a broken file.

| | |
|---|---|
| `01_basics.py` | variables, types, f-strings, conversion |
| `02_conditionals.py` | branching, comparison chaining |
| `03_loops.py` | `for`, `while`, `range`, `break` |
| `04_functions.py` | arguments, returns, recursion |
| `05_structures.py` | lists, dicts, sets, copies |
| `06_classes.py` | state, inheritance, dunder methods |
| `07_advanced.py` | comprehensions, generators, context managers, decorators |
| `08_design.py` | DRY, KISS, SRP, OCP, LSP, DIP – six refactorings |
| `09_pipeline.py` | the nightly job, start to finish |
| `spot_the_bug.md` | eight broken snippets – a game, not a file to edit |

Reference solutions: `exercises/python/solutions/`. Look after you have tried,
not before – and then compare, rather than copy.

## Linux

```console
$ cd exercises/linux
$ ./setup-playground.sh
$ cd ~/linux-playground
```

| | |
|---|---|
| `terminal-scavenger-hunt.md` | twelve questions, one command each |
| `bash-exercises.md` | five scripts, with a brief and hints |
| `bash/run-tests.sh` | the test runner: `./run-tests.sh greet` |
| `bash/solutions/` | reference solutions |

---

## Handing in

Work on your own branch and open a pull request when you are done – or when
the day ends, whichever comes first.

```console
$ git switch -c firstname-lastname
$ git add exercises/
$ git commit -m "Solve the Python basics exercises"
$ git push -u origin firstname-lastname
```

Then open a pull request against `main` and leave it open. You will get review
comments, and answering them is the last exercise.

Commit as you go rather than all at once at the end. Small commits with real
messages are themselves part of what is being assessed – and they make the
review useful to you.

## If you get stuck

Fifteen minutes stuck is learning. Ninety is waste.

Before you ask, be able to say two things: what you expected, and what
happened. That sentence solves about half of them on its own.
