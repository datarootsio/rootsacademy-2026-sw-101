"""Classes: state, methods, inheritance, dunder methods. Reference solution."""

from dataclasses import dataclass


class BankAccount:
    """An account that refuses to go below zero."""

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.log = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(f"deposit must be positive, got {amount}")
        self.balance += amount
        self.log.append(("deposit", amount))
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError(f"withdrawal must be positive, got {amount}")
        if amount > self.balance:
            raise ValueError(f"cannot withdraw {amount}, balance is {self.balance}")
        self.balance -= amount
        self.log.append(("withdraw", amount))
        return self.balance

    def statement(self):
        lines = [f"{self.owner}"]
        for kind, amount in self.log:
            lines.append(f"  {kind:<9} {amount:>8.2f}")
        lines.append(f"  {'balance':<9} {self.balance:>8.2f}")
        return "\n".join(lines)

    def __repr__(self):
        return f"BankAccount({self.owner!r}, {self.balance})"


class SavingsAccount(BankAccount):
    """An account that earns interest."""

    def __init__(self, owner, balance=0, rate=0.02):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        return self.deposit(self.balance * self.rate)

    def __repr__(self):
        return f"SavingsAccount({self.owner!r}, {self.balance}, rate={self.rate})"


class Vector:
    """A point in n dimensions."""

    def __init__(self, *components):
        self.components = components

    def __add__(self, other):
        return Vector(*(a + b for a, b in zip(self.components, other.components)))

    def __sub__(self, other):
        return Vector(*(a - b for a, b in zip(self.components, other.components)))

    def __eq__(self, other):
        return self.components == other.components

    def __len__(self):
        return len(self.components)

    def __repr__(self):
        inner = ", ".join(str(c) for c in self.components)
        return f"Vector({inner})"


@dataclass(frozen=True)
class Point:
    """The same idea as Vector, with the boilerplate deleted."""

    x: float
    y: float


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
