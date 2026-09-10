# Software Development 101

One-day course for RootsAcademy 2026. Git, Python and the Linux terminal in
six hours, for people who have written a little code and not yet worked on a
team.

## Start here

Open **[slides/index.html](slides/index.html)** in a browser. It has the
timetable, links to the three decks, and the setup check.

```console
$ open slides/index.html          # macOS
$ xdg-open slides/index.html      # Linux
```

## What is in here

```
slides/            three decks plus the hub page – static HTML, no build step
  index.html         the day: timetable, tracks, setup, materials
  git.html           45 slides, runs first
  python.html        131 slides
  linux.html         38 slides
  deck.css           all styling
  tokens.css         colours and typefaces – change the palette here
  deck.js            navigation, the day rail, syntax highlighting

exercises/         self-checking exercises for all three tracks
  git/               nine broken repositories, generated on demand
  python/            nine files of stubs + assertions, and solutions
  linux/             a scavenger-hunt playground and five bash scripts

cheatsheets/       one printable page per track

TRAINER-NOTES.md   timing, what to demo live, where people get stuck
Python 101.ipynb   the original notebook – run cells alongside the deck
```

## Running a deck

| | |
|---|---|
| ← → space | move |
| `o` | contents |
| `f` | fullscreen |
| Print → PDF | one slide per page |

The decks work with no network. Web fonts fail gracefully to system faces.

## Objectives

By the end of the day, participants can:

- use Git in a team's branching workflow, and recover from the mistakes that
  usually stop people;
- write Python scripts using the core language and the four containers,
  deliberately, and split them along the lines they will have to change;
- name and apply DRY, KISS, YAGNI and SOLID without over-applying them, and
  write the tests that make a refactor safe;
- navigate a Linux terminal, compose commands with pipes, and write a small
  bash script that does not surprise them.

Git is taught first so that every exercise afterwards gets committed, pushed
and reviewed, rather than the workflow being covered once at the end.

## Editing

Slides are hand-written HTML. To change one, find its `<section class="slide">`
and edit it. Everything is styled from `slides/deck.css`; the three track
colours and both typefaces are tokens at the top of `slides/tokens.css`.

Content is sized to fit a 16:9 frame with no scrolling – if you add several
lines to a slide, check it still fits before the day.
