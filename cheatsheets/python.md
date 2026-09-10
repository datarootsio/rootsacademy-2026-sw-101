# Python – one page

## Types

```python
5  4.2  1+5j  True  None          # int float complex bool NoneType
"text"  'text'  """multi
line"""

int("42")  float("4.2")  str(42)  list("abc")
type(x)  isinstance(x, int)
```

Falsy: `0  0.0  ""  []  {}  ()  None`. Everything else is truthy.
`is` / `is not` only for `None`, `True`, `False`. Otherwise `==`.

## f-strings

```python
f"{name} is {age}"          f"{age + 1}"
f"{pi:.3f}"        3.142    f"{1234567:,}"     1,234,567
f"{0.916:.1%}"     91.6%    f"{'x':>10}"       right-aligned in 10
f"{count=}"        count=2  – the fastest debugging you own
```

## Containers

| | list | tuple | set | dict |
|---|---|---|---|---|
| | `[1, 2]` | `(1, 2)` | `{1, 2}` | `{"a": 1}` |
| mutable | yes | no | yes | yes |
| ordered | yes | yes | no | yes |
| duplicates | yes | yes | no | keys: no |

`(1)` is an int. `(1,)` is a tuple. `{}` is a dict; `set()` is an empty set.

```python
items[0]  items[-1]  items[1:3]  items[::-1]  items[:]     # slices copy
items.append(x)  .extend([x])  .insert(0, x)  .pop()  .remove(x)
items.sort()          # in place, returns None
sorted(items, key=len, reverse=True)     # new list

d["k"]         # KeyError if missing
d.get("k", 0)  # default instead
d.keys()  d.values()  d.items()
{**d1, **d2}   d1 | d2                   # merge

s1 | s2   s1 & s2   s1 - s2              # union, intersection, difference
```

## Control flow

```python
if 1 < x < 5: ...
elif x > 5:   ...
else:         ...
label = "adult" if age >= 18 else "minor"

for i in range(0, 10, 2): ...            # stops before 10
for i, item in enumerate(items, start=1): ...
for a, b in zip(list_a, list_b): ...
while condition: ...
break  continue
for ... else:        # else runs only if no break
```

## Functions

```python
def area(radius: float, unit: str = "m") -> float:
    """One line saying what it does."""
    return pi * radius**2

def report(*args, **kwargs): ...         # tuple, dict
report(*a_list, **a_dict)                # unpack at the call site
```

Never `def f(items=[])` – the default is created once. Use `None`.

## Comprehensions

```python
[x * x for x in nums]
[x for x in nums if x % 2 == 0]
{w: len(w) for w in words}
{w[0] for w in words}
(x * x for x in nums)                    # generator: lazy
```

One `for` and at most one `if`. Past that, write the loop.

## Classes

```python
class Person:
    def __init__(self, name, age):
        self.name, self.age = name, age

    def __repr__(self):
        return f"Person({self.name!r}, {self.age})"


class Student(Person):
    def __init__(self, name, age, grade):
        super().__init__(name, age)
        self.grade = grade


from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float
```

`__add__ __eq__ __len__ __getitem__ __iter__ __enter__ __repr__ __str__`

## Errors

```python
try:
    value = int(text)
except ValueError:
    ...
else:            # only if nothing was raised
    ...
finally:         # always
    ...

raise ValueError(f"expected a positive number, got {n}")
```

Never a bare `except:`. Read tracebacks bottom-up.

## Files and paths

```python
from pathlib import Path

with open("data.txt") as f:              # closed even if this raises
    for line in f:
        print(line.rstrip())

Path("data").glob("*.csv")
Path("a/b.csv").stem  .suffix  .parent  .exists()
```

## Modules and environments

```python
import math                    from math import pi
import pandas as pd            # never: from x import *

if __name__ == "__main__":     # runs only when executed directly
    main()
```

```console
$ python3 -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
$ pip freeze > requirements.txt
$ ruff format . && ruff check .
```

## Design principles

| | Ask yourself | In Python |
|---|---|---|
| KISS | can I fix this at 02:00? | boring beats clever; no comment needed |
| DRY | must the other copy change too? | one fact, one place – after the third copy |
| YAGNI | who asked for this? | delete the branch nobody takes |
| S | how many people can make me edit this? | one stage per function or module |
| O | can I add a case without editing one? | a dict of handlers, or a callable argument |
| L | would this subclass surprise the caller? | if yes, compose instead of inherit |
| I | what does this actually need? | a one-method `Protocol`, or just a function |
| D | does my logic import `requests`? | pass the reader, clock and client in |

Duplication is cheaper than the wrong abstraction. Every abstraction costs the
reader one jump – make it earn that.

```python
def summarise(rows, rates: Rates, today: date) -> dict: ...

summarise(rows, EcbRates(session), date.today())        # main
summarise(rows, FixedRates("0.90"), date(2026, 1, 5))   # test
```

## Tests

```python
@pytest.mark.parametrize("country,expected", [("BE", "0.21"), ("FR", "0.20")])
def test_vat(country, expected):
    assert vat_for(country) == Decimal(expected)

with pytest.raises(UnknownCountry):
    vat_for("ZZ")
```

`pytest -q` · `-x` first failure · `-k name` select · `--lf` rerun failures

Test rules, parsers and error paths. Not libraries. A fake beats a mock; if a
test needs `mock.patch`, fix the design instead.

## Standard library worth remembering

`pathlib json datetime decimal collections(Counter, defaultdict) re`
`itertools(islice, chain, batched) functools(cache, wraps) csv logging argparse`

## Style

4 spaces. `snake_case` / `PascalCase` / `UPPER_SNAKE`. Lines under 88.
Never shadow `list dict sum str type id input max min`.
