"""Sugar and advanced concepts: comprehensions, generators, decorators.

Reference solution.
"""

import time
from contextlib import contextmanager
from functools import wraps


def shout_long_names(names, min_length=3):
    """'1: GRACE, 2: ALAN' – the 'spot the sugar' exercise, in one line."""
    return ", ".join(
        f"{i}: {name.upper()}" for i, name in enumerate(names) if len(name) > min_length
    )


def first_n(limit):
    """A generator: yields 0 .. limit - 1 without building a list."""
    number = 0
    while number < limit:
        yield number
        number += 1


def read_chunks(text, size):
    """A generator over slices of a string."""
    for start in range(0, len(text), size):
        yield text[start : start + size]


@contextmanager
def timer(label, sink=None):
    """Times the block and records the label. sink makes it testable."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        if sink is None:
            print(f"{label} took {elapsed:.3f}s")
        else:
            sink.append((label, elapsed))


def counted(func):
    """Counts how often the wrapped function was called."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


@counted
def add(a, b):
    """Adds two numbers."""
    return a + b


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
