"""Data structures: lists, dicts, sets, copies. Reference solution."""

from collections import Counter, defaultdict


def largest(numbers):
    """The biggest value, without max() and without sorting."""
    biggest = numbers[0]
    for number in numbers[1:]:
        if number > biggest:
            biggest = number
    return biggest


def grid(width, height, fill="*"):
    """A height x width grid as a list of rows."""
    return [[fill] * width for _ in range(height)]


def render(rows):
    """A grid as printable lines."""
    return [" ".join(row) for row in rows]


def letter_counts(text):
    """How often each character appears."""
    counts = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    return counts


def merge_sum(first, second):
    """Merge two dicts, summing shared keys. Returns sorted [key, value] pairs."""
    merged = dict(first)
    for key, value in second.items():
        merged[key] = merged.get(key, 0) + value
    return [[key, merged[key]] for key in sorted(merged)]


def swap(items, i, j):
    """Exchange two positions in place."""
    items[i], items[j] = items[j], items[i]


def bubble_sort(items):
    """Sorted copy – the caller's list is left alone."""
    result = items.copy()
    for _ in range(len(result)):
        swapped = False
        for i in range(len(result) - 1):
            if result[i] > result[i + 1]:
                swap(result, i, i + 1)
                swapped = True
        if not swapped:
            break
    return result


def by_team(people):
    """[{'name':…, 'team':…}] -> {team: [names]}"""
    grouped = defaultdict(list)
    for person in people:
        grouped[person["team"]].append(person["name"])
    return dict(grouped)


if __name__ == "__main__":
    assert largest([8, 9, 3, 6, 1]) == 9
    assert largest([-4]) == -4
    print("1 largest ok")

    assert grid(3, 2) == [["*", "*", "*"], ["*", "*", "*"]]
    assert render(grid(3, 2)) == ["* * *", "* * *"]
    rows = grid(2, 2)
    rows[0][0] = "x"
    assert rows[1][0] == "*", "each row must be its own list"
    print("2 grid ok")

    assert letter_counts("banana") == {"b": 1, "a": 3, "n": 2}
    assert letter_counts("") == {}
    assert letter_counts("banana") == dict(Counter("banana"))
    print("3 letter_counts ok")

    assert merge_sum({"a": 30, "b": 15}, {"b": 10, "c": 11}) == [
        ["a", 30], ["b", 25], ["c", 11],
    ]
    assert merge_sum({}, {}) == []
    print("4 merge_sum ok")

    original = [9, 4, 6, 1, 4, 2]
    assert bubble_sort(original) == [1, 2, 4, 4, 6, 9]
    assert original == [9, 4, 6, 1, 4, 2], "the original must not change"
    print("5 bubble_sort ok")

    assert by_team([
        {"name": "ada", "team": "data"},
        {"name": "alan", "team": "infra"},
        {"name": "grace", "team": "data"},
    ]) == {"data": ["ada", "grace"], "infra": ["alan"]}
    print("6 by_team ok")

    print("\nAll data structure exercises pass.")
