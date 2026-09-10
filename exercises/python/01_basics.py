"""Basics: variables, types, f-strings, conversion.

Fill in each function until running this file prints all-ok.
The reference solution is in solutions/01_basics.py – look there only after you have tried.
"""

from math import pi


def circle(radius):
    """Return (area, circumference) of a circle."""
    raise NotImplementedError("your turn")


def celsius_to_fahrenheit(celsius):
    """Convert using augmented assignment only."""
    raise NotImplementedError("your turn")


def make_login(first_name, last_name):
    """'Charlotte', 'De Baere' -> 'c.debaere'"""
    raise NotImplementedError("your turn")


def float_report(a, b):
    """Show the same sum at three precisions."""
    raise NotImplementedError("your turn")


if __name__ == "__main__":
    area, circumference = circle(3)
    assert round(area, 4) == 28.2743
    assert round(circumference, 4) == 18.8496
    print("1 circle ok")

    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212
    assert celsius_to_fahrenheit(-40) == -40
    print("2 celsius_to_fahrenheit ok")

    assert make_login("Charlotte", "De Baere") == "c.debaere"
    assert make_login("  nico  ", "Peeters") == "n.peeters"
    print("3 make_login ok")

    rounded, medium, exact = float_report(0.1, 0.2)
    assert rounded == "0.30"
    assert medium == "0.30000"
    assert exact.startswith("0.3000000000000000")
    assert exact != "0.30000000000000000000"   # 0.1 + 0.2 is not 0.3
    print("4 float_report ok")

    print("\nAll basics exercises pass.")
