"""Loops: for, while, range, break, continue.

Fill in each function until running this file prints all-ok.
The reference solution is in solutions/03_loops.py – look there only after you have tried.
"""

import random


def pyramid(rows):
    """Growing-then-shrinking pyramid of stars, as a list of lines."""
    raise NotImplementedError("your turn")


def fibonacci_below(limit):
    """Every Fibonacci number strictly below limit, starting at 1."""
    raise NotImplementedError("your turn")


def guess_count(secret, guesses):
    """How many guesses were needed, and the hint given for each one."""
    raise NotImplementedError("your turn")


def computer_guesses(secret, low=1, high=100):
    """Binary search: the guesses the computer makes to find secret."""
    raise NotImplementedError("your turn")


def play():
    """The interactive version. Not covered by the asserts."""
    raise NotImplementedError("your turn")


if __name__ == "__main__":
    assert pyramid(1) == ["*"]
    assert pyramid(3) == ["*", "**", "***", "**", "*"]
    assert len(pyramid(5)) == 9
    print("1 pyramid ok")

    assert fibonacci_below(50) == [1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fibonacci_below(2) == [1, 1]
    print("2 fibonacci_below ok")

    attempts, hints = guess_count(7, [5, 9, 7])
    assert attempts == 3
    assert hints == ["Higher", "Lower"]
    assert guess_count(7, [1, 2])[0] is None
    print("3-4 guess_count ok")

    assert computer_guesses(1)[-1] == 1
    assert computer_guesses(100)[-1] == 100
    assert all(len(computer_guesses(n)) <= 7 for n in range(1, 101))
    print("5 computer_guesses ok – never more than 7 guesses")

    print("\nAll loops exercises pass. Run play() for the interactive game.")
