"""Conditionals: branching, comparison chaining.

Fill in each function until running this file prints all-ok.
The reference solution is in solutions/02_conditionals.py – look there only after you have tried.
"""

def convert_temperature(unit, value):
    """Convert between C and F. Returns (value, unit) or None for a bad unit."""
    raise NotImplementedError("your turn")


def divisibility_report(number):
    """One sentence about divisibility by 2 and 3."""
    raise NotImplementedError("your turn")


def largest_of_three(a, b, c):
    """The biggest of three numbers, without max() and without sorting."""
    raise NotImplementedError("your turn")


def fizzbuzz(number):
    """Fizz / Buzz / FizzBuzz / the number itself, as a string."""
    raise NotImplementedError("your turn")


if __name__ == "__main__":
    value, unit = convert_temperature("C", 100)
    assert (round(value), unit) == (212, "F")
    value, unit = convert_temperature("f", 32)
    assert (round(value), unit) == (0, "C")
    assert convert_temperature("K", 0) is None
    print("1 convert_temperature ok")

    assert divisibility_report(6) == "6 divides by both 2 and 3"
    assert divisibility_report(4) == "4 divides by 2"
    assert divisibility_report(9) == "9 divides by 3"
    assert divisibility_report(7) == "7 divides by neither 2 nor 3"
    print("2 divisibility_report ok")

    assert largest_of_three(1, 2, 3) == 3
    assert largest_of_three(9, 2, 3) == 9
    assert largest_of_three(-5, -2, -9) == -2
    print("3 largest_of_three ok")

    assert [fizzbuzz(n) for n in range(1, 16)] == [
        "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8",
        "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz",
    ]
    print("4 fizzbuzz ok")

    print("\nAll conditionals exercises pass.")
