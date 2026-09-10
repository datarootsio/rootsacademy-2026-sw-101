"""Conditionals: branching, comparison chaining. Reference solution."""


def convert_temperature(unit, value):
    """Convert between C and F. Returns (value, unit) or None for a bad unit."""
    unit = unit.strip().upper()
    if unit == "C":
        return (9 * value) / 5 + 32, "F"
    if unit == "F":
        return (value - 32) * 5 / 9, "C"
    return None


def divisibility_report(number):
    """One sentence about divisibility by 2 and 3."""
    by_two = number % 2 == 0
    by_three = number % 3 == 0
    if by_two and by_three:
        return f"{number} divides by both 2 and 3"
    if by_two:
        return f"{number} divides by 2"
    if by_three:
        return f"{number} divides by 3"
    return f"{number} divides by neither 2 nor 3"


def largest_of_three(a, b, c):
    """The biggest of three numbers, without max() and without sorting."""
    biggest = a
    if b > biggest:
        biggest = b
    if c > biggest:
        biggest = c
    return biggest


def fizzbuzz(number):
    """Fizz / Buzz / FizzBuzz / the number itself, as a string."""
    if number % 15 == 0:
        return "FizzBuzz"
    if number % 3 == 0:
        return "Fizz"
    if number % 5 == 0:
        return "Buzz"
    return str(number)


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
