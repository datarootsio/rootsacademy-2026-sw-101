"""Sugar and advanced concepts: comprehensions, generators, decorators.

Fill in each function until running this file prints all-ok.
The reference solution is in solutions/07_advanced.py – look there only after you have tried.
"""

import time
from contextlib import contextmanager
from functools import wraps


def shout_long_names(names, min_length=3):
    """'1: GRACE, 2: ALAN' – the 'spot the sugar' exercise, in one line."""
    raise NotImplementedError("your turn")


def first_n(limit):
    """A generator: yields 0 .. limit - 1 without building a list."""
    raise NotImplementedError("your turn")


def read_chunks(text, size):
    """A generator over slices of a string."""
    raise NotImplementedError("your turn")


@contextmanager
def timer(label, sink=None):
    """Times the block and records the label. sink makes it testable."""
    raise NotImplementedError("your turn")


def counted(func):
    """Counts how often the wrapped function was called."""
    raise NotImplementedError("your turn")


@counted
def add(a, b):
    """Adds two numbers."""
    raise NotImplementedError("your turn")


if __name__ == "__main__":
    assert shout_long_names(["ada", "grace", "alan", "edsger"]) == (
        "1: GRACE, 2: ALAN, 3: EDSGER"
    )
    assert shout_long_names([]) == ""
    print("1 shout_long_names ok")

    generator = first_n(5)
    assert not isinstance(generator, list), "a generator, not a list"
    assert list(generator) == [0, 1, 2, 3, 4]
    assert list(generator) == [], "a generator is exhausted after one pass"
    assert next(first_n(5)) == 0
    print("2 first_n ok")

    assert list(read_chunks("abcdefg", 3)) == ["abc", "def", "g"]
    print("3 read_chunks ok")

    records = []
    with timer("sleep", sink=records):
        time.sleep(0.01)
    assert len(records) == 1
    assert records[0][0] == "sleep"
    assert records[0][1] >= 0.01
    try:
        with timer("boom", sink=records):
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    assert len(records) == 2, "the timer must record even when the block raises"
    print("4 timer ok")

    assert add(1, 2) == 3
    assert add(3, 4) == 7
    assert add.calls == 2
    assert add.__name__ == "add", "@wraps keeps the original name"
    assert add.__doc__ == "Adds two numbers."
    print("5 counted ok")

    print("\nAll advanced exercises pass.")
