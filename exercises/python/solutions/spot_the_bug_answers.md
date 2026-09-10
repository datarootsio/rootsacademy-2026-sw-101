# Spot the bug – answers

## 1 – the comma makes the tuple, not the brackets

`(1)` is the integer 1 in ordinary brackets. `TypeError: object of type 'int'
has no len()`.

```python
point = (1,)     # or: point = 1,
```

A one-element tuple always needs the trailing comma. Everywhere else the
brackets are optional: `1, 2` is already a tuple.

## 2 – two bugs: a shadowed builtin and an off-by-one start

It prints `0 1 1 2 3 5 8 13 21 34` – the sequence starts at 0, but the author
asked for Fibonacci *from 1*. Then `sum([1, 2, 3])` raises
`TypeError: 'int' object is not callable`, because `sum` is no longer the
builtin function – it is the integer 55.

```python
current, following = 1, 1
total = 0
while current < 50:
    print(current, end=" ")
    total += current
    current, following = following, current + following
```

Never name a variable `sum`, `list`, `dict`, `str`, `type`, `id`, `input`,
`max` or `min`. The failure shows up far away from the cause, which is what
makes it expensive.

## 3 – Python will not order values it cannot compare

`TypeError: '<' not supported between instances of 'int' and 'str'`.

Sorting needs `<` to work between every pair. Strings and integers have no
defined order relative to each other. Either keep the list homogeneous, or
say explicitly what you want to sort by:

```python
names.sort(key=str)     # compares "3", "Jean", "Paul", "1"
```

Most of the time a mixed list is the real bug: those positions probably mean
different things and want a dict or a class.

## 4 – three problems

1. `dictlist` versus `dictList` – `NameError: name 'dictlist' is not defined`.
   Python is case sensitive and cannot warn you at edit time.
2. `dict = {}` shadows the builtin `dict` for the rest of the file.
3. `temp` exists only to be appended on the next line.

```python
capitals = {"Capital": "London", "Food": "Fish&Chips"}
pairs = [[key, value] for key, value in capitals.items()]
```

Consistent naming is not pedantry – it is how you stop losing ten minutes to
a typo.

## 5 – `old_list = our_list` is not a copy

Both names point at the same list, and `bubble_sort` sorts in place, so
`our_list` is sorted too. Both lines print `[1, 4, 6, 9]`.

```python
old_list = our_list.copy()        # or list(our_list), or our_list[:]
```

Better still, make the function stop mutating its argument:

```python
def bubble_sort(values):
    values = values.copy()
    ...
    return values
```

A function that quietly rewrites the caller's data is a bug waiting for a
second caller.

## 6 – the default is created once, not per call

`['python']` then `['python', 'git']`. The empty list is built when the `def`
line runs, and every call that omits the argument shares it.

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
```

The rule: never use a mutable value (`[]`, `{}`, `set()`) as a default.

## 7 – strings are immutable, so the methods return new ones

Prints `[  Data Roots  ]` with the newline: nothing changed. `raw.strip()`
computed a stripped string and threw it away.

```python
raw = raw.strip().lower()
```

Every string method returns a value. If you are not assigning it, you are not
using it. Same trap with `sorted()`, `.upper()`, `.replace()` and
`list.copy()`.

## 8 – you cannot resize a dict while iterating it

`RuntimeError: dictionary changed size during iteration`.

Iterate over a snapshot, or build the result you want:

```python
scores = {name: score for name, score in scores.items() if score >= 80}
# or
for name in list(scores):
    if scores[name] < 80:
        del scores[name]
```

The same applies to removing items from a list you are looping over – except
there you get no error at all, just silently skipped elements. That version
is worse.

---

## Bonus round

**a – floats do not add up.** `19.99 + 5.00 + 3.01` is
`28.000000000000004`, so the comparison is `False`. Compare with a tolerance,
or hold money as integer cents:

```python
if round(sum(prices), 2) == 28.00:
```

**b – `0` is falsy.** `retries` is configured; it is configured to zero. The
message is wrong. When you mean "was it set at all":

```python
if config.get("retries") is not None:
```

**c – `ZeroDivisionError` on empty input.** It does crash, but only for the
input nobody tested. Decide what the answer should be and say so:

```python
def average(numbers):
    if not numbers:
        raise ValueError("average of an empty sequence is undefined")
    return sum(numbers) / len(numbers)
```
