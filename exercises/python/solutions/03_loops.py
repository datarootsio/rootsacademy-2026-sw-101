"""Loops: for, while, range, break, continue. Reference solution."""

import random


def pyramid(rows):
    """Growing-then-shrinking pyramid of stars, as a list of lines."""
    up = [("*" * n) for n in range(1, rows + 1)]
    down = [("*" * n) for n in range(rows - 1, 0, -1)]
    return up + down


def fibonacci_below(limit):
    """Every Fibonacci number strictly below limit, starting at 1."""
    numbers = []
    current, following = 1, 1
    while current < limit:
        numbers.append(current)
        current, following = following, current + following
    return numbers


def guess_count(secret, guesses):
    """How many guesses were needed, and the hint given for each one."""
    hints = []
    for attempt, guess in enumerate(guesses, start=1):
        if guess == secret:
            return attempt, hints
        hints.append("Lower" if guess > secret else "Higher")
    return None, hints


def computer_guesses(secret, low=1, high=100):
    """Binary search: the guesses the computer makes to find secret."""
    guesses = []
    while low <= high:
        guess = (low + high) // 2
        guesses.append(guess)
        if guess == secret:
            return guesses
        if guess < secret:
            low = guess + 1
        else:
            high = guess - 1
    return guesses


def play():
    """The interactive version. Not covered by the asserts."""
    secret = random.randint(1, 10)
    count = 0
    while True:
        count += 1
        guess = int(input("Guess the number (1-10): "))
        if guess == secret:
            print(f"Correct, it was {secret}, in {count} guesses")
            return
        print("Lower!" if guess > secret else "Higher!")


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
