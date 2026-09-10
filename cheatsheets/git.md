# Git – one page

## Once per machine

```console
$ git config --global user.name "Your Name"
$ git config --global user.email "you@example.com"
$ git config --global init.defaultBranch main
$ git config --global pull.rebase true
$ git config --global alias.lg "log --oneline --graph --all -20"
```

## The loop

```console
$ git switch main && git pull
$ git switch -c feature/short-name
  ... edit ...
$ git status
$ git diff                      # unstaged
$ git add -p                    # choose chunk by chunk
$ git diff --staged             # read this before every commit
$ git commit -m "Fix VAT rate for Belgian invoices"
$ git push -u origin feature/short-name
  ... open a pull request, get review, squash and merge ...
```

## Looking around

```console
$ git status                    # where am I
$ git lg                        # the graph
$ git log --oneline -- path     # history of one file
$ git log -S "SOME_TEXT"        # commits that added or removed that text
$ git show <sha>                # one commit in full
$ git blame path                # who last touched each line
$ git diff main..feature/x      # branch against branch
```

## Branches and remotes

```console
$ git branch -a                 $ git switch -c name
$ git switch main               $ git switch -          # previous branch
$ git branch -d name            $ git branch -m newname

$ git fetch                     # download, change nothing – always safe
$ git pull                      # fetch + integrate
$ git merge origin/main         # bring main into your branch
$ git pull --rebase origin main # same, linear history, new hashes
```

`origin/main` is a local bookmark of the server, updated only by `fetch`.

## Conflicts

```
<<<<<<< HEAD
your version
=======
their version
>>>>>>> origin/main
```

Delete all three marker lines, keep the code you want, then:

```console
$ git add <file>                # this is how you say "resolved"
$ git status                    # anything left?
$ git commit
$ git merge --abort             # change of mind, at any point
```

Search for `<<<<<<<` before committing. Run the tests before committing.

## Undo

| Situation | Command |
|---|---|
| edited, not staged | `git restore <file>` |
| staged, not committed | `git restore --staged <file>` |
| untracked files to remove | `git clean -n` then `git clean -fd` |
| put work down for a minute | `git stash push -m "why"` / `git stash pop` |
| last commit message wrong | `git commit --amend -m "..."` |
| forgot a file in the last commit | `git add f && git commit --amend --no-edit` |
| undo commit, keep it staged | `git reset --soft HEAD~1` |
| undo commit, keep the files | `git reset HEAD~1` |
| undo commit, discard the work | `git reset --hard HEAD~1` |
| undo something already pushed | `git revert <sha>` |
| find what you lost | `git reflog` |
| take one commit from elsewhere | `git cherry-pick <sha>` |
| tidy your branch before review | `git rebase -i HEAD~4` |
| find the commit that broke it | `git bisect start / bad / good` |

**If it was committed, `git reflog` can find it.**
**If it was never committed, nothing can.**

## The golden rule

Rewrite history only on a branch nobody else has pulled. On `main`, use
`revert`. When you must force-push your own branch, use
`git push --force-with-lease` – it refuses if the remote moved.

## .gitignore

```
.venv/            __pycache__/      *.pyc
.env              *.pem             credentials.json
.DS_Store         .vscode/          .ipynb_checkpoints/
data/raw/
```

Already tracked? `.gitignore` will not help: `git rm --cached <file>` first.

## Commit messages

```
Fix VAT rate for Belgian invoices        <- under 50 chars, imperative
                                         <- blank line
The rate was hardcoded from the 2019     <- why, not what
pilot. Reads it from config instead.

Closes #418
```

If the subject needs the word "and", it should be two commits.
