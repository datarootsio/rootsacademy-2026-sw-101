"""Basics: variables, types, f-strings, conversion. Reference solution."""

from math import pi


def circle(radius):
    """Return (area, circumference) of a circle."""
    return pi * radius**2, 2 * pi * radius


def celsius_to_fahrenheit(celsius):
    """Convert using augmented assignment only."""
    value = celsius
    value *= 1.8
    value += 32
    return value


def make_login(first_name, last_name):
    """'Charlotte', 'De Baere' -> 'c.debaere'"""
    initial = first_name.strip()[0].lower()
    surname = last_name.strip().lower().replace(" ", "")
    return f"{initial}.{surname}"


def float_report(a, b):
    """Show the same sum at three precisions."""
    return [f"{a + b:.2f}", f"{a + b:.5f}", f"{a + b:.20f}"]


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
