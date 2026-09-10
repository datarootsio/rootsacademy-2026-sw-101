"""Functions: arguments, returns, recursion. Reference solution."""

from functools import cache


def exponent(a, b):
    """a to the power b."""
    return a**b


def exponent_no_operator(a, b):
    """Same, using repeated multiplication."""
    result = 1
    for _ in range(b):
        result *= a
    return result


def fibonacci(n):
    """The first n Fibonacci numbers, starting 1, 1."""
    numbers = []
    current, following = 1, 1
    for _ in range(n):
        numbers.append(current)
        current, following = following, current + following
    return numbers


def is_palindrome(text):
    """Ignores case, spaces and punctuation."""
    letters = [char.lower() for char in text if char.isalnum()]
    return letters == letters[::-1]


def word_lengths(sentence):
    """Each word mapped to its length."""
    return {word: len(word) for word in sentence.split()}


@cache
def fib_recursive(n):
    """The nth Fibonacci number, recursively. @cache is what makes it fast."""
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


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
