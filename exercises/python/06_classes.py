"""Classes: state, methods, inheritance, dunder methods.

Fill in each function until running this file prints all-ok.
The reference solution is in solutions/06_classes.py – look there only after you have tried.
"""

from dataclasses import dataclass


class BankAccount:
    """An account that refuses to go below zero."""

    def __init__(self, owner, balance=0):
        raise NotImplementedError("your turn")

    def deposit(self, amount):
        raise NotImplementedError("your turn")

    def withdraw(self, amount):
        raise NotImplementedError("your turn")

    def statement(self):
        raise NotImplementedError("your turn")

    def __repr__(self):
        raise NotImplementedError("your turn")


class SavingsAccount(BankAccount):
    """An account that earns interest."""

    def __init__(self, owner, balance=0, rate=0.02):
        raise NotImplementedError("your turn")

    def add_interest(self):
        raise NotImplementedError("your turn")

    def __repr__(self):
        raise NotImplementedError("your turn")


class Vector:
    """A point in n dimensions."""

    def __init__(self, *components):
        raise NotImplementedError("your turn")

    def __add__(self, other):
        raise NotImplementedError("your turn")

    def __sub__(self, other):
        raise NotImplementedError("your turn")

    def __eq__(self, other):
        raise NotImplementedError("your turn")

    def __len__(self):
        raise NotImplementedError("your turn")

    def __repr__(self):
        raise NotImplementedError("your turn")


@dataclass(frozen=True)
class Point:
    """The same idea as Vector, with the boilerplate deleted."""
    # TODO declare the fields, then delete this line
    pass


if __name__ == "__main__":
    account = BankAccount("Charlotte", 100)
    account.deposit(50)
    assert account.balance == 150
    assert account.withdraw(20) == 130
    try:
        account.withdraw(1000)
    except ValueError as error:
        assert "balance is 130" in str(error)
    else:
        raise AssertionError("an overdraft must raise ValueError")
    assert repr(account) == "BankAccount('Charlotte', 130)"
    print("1 BankAccount ok")

    savings = SavingsAccount("Nico", 1000, rate=0.05)
    savings.add_interest()
    assert savings.balance == 1050
    assert isinstance(savings, BankAccount)
    print("2 SavingsAccount ok")

    assert Vector(1, 2) + Vector(5, 3) == Vector(6, 5)
    assert Vector(5, 3) - Vector(1, 2) == Vector(4, 1)
    assert len(Vector(1, 2, 3)) == 3
    assert repr(Vector(1, 2)) == "Vector(1, 2)"
    print("3 Vector ok")

    assert Point(1, 2) == Point(1, 2)
    assert repr(Point(1, 2)) == "Point(x=1, y=2)"
    try:
        Point(1, 2).x = 9
    except AttributeError:
        pass
    else:
        raise AssertionError("a frozen dataclass must not allow assignment")
    print("4 Point ok – four dunder methods for two lines of code")

    print("\n" + account.statement())
    print("\nAll class exercises pass.")
