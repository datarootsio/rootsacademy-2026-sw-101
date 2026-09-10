"""Functions: arguments, returns, recursion.

Fill in each function until running this file prints all-ok.
The reference solution is in solutions/04_functions.py – look there only after you have tried.
"""

from functools import cache


def exponent(a, b):
    """a to the power b."""
    raise NotImplementedError("your turn")


def exponent_no_operator(a, b):
    """Same, using repeated multiplication."""
    raise NotImplementedError("your turn")


def fibonacci(n):
    """The first n Fibonacci numbers, starting 1, 1."""
    raise NotImplementedError("your turn")


def is_palindrome(text):
    """Ignores case, spaces and punctuation."""
    raise NotImplementedError("your turn")


def word_lengths(sentence):
    """Each word mapped to its length."""
    raise NotImplementedError("your turn")


@cache
def fib_recursive(n):
    """The nth Fibonacci number, recursively. @cache is what makes it fast."""
    raise NotImplementedError("your turn")


if __name__ == "__main__":
    assert exponent(3, 2) == 9
    assert exponent(2, 10) == 1024
    assert exponent(5, 0) == 1
    print("1 exponent ok")

    assert exponent_no_operator(3, 3) == 27
    assert exponent_no_operator(7, 1) == 7
    assert exponent_no_operator(9, 0) == 1
    print("2 exponent_no_operator ok")

    assert fibonacci(1) == [1]
    assert fibonacci(8) == [1, 1, 2, 3, 5, 8, 13, 21]
    assert fibonacci(0) == []
    print("3 fibonacci ok")

    assert is_palindrome("A man, a plan, a canal: Panama")
    assert is_palindrome("racecar")
    assert not is_palindrome("dataroots")
    print("4 is_palindrome ok")

    assert word_lengths("keep it simple") == {"keep": 4, "it": 2, "simple": 6}
    assert word_lengths("") == {}
    print("5 word_lengths ok")

    assert fib_recursive(10) == 55
    assert fib_recursive(30) == 832040
    print("6 fib_recursive ok – try it without @cache and time it")

    print("\nAll function exercises pass.")
