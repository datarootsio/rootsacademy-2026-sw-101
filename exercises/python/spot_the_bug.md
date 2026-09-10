# Spot the bug

Eight snippets. Every one of them is broken, or right for the wrong reason.
All eight are bugs that a real person has shipped – several come from the
course notebook itself.

**How to play.** Teams of two. Four snippets in class, the rest at home.

For each snippet, write down two things *before you run it*:

1. What happens when you run this?
2. What did the author mean?

**Scoring:** 2 points for the diagnosis, 1 point for a fix that a reviewer
would approve. Guessing costs nothing, so guess.

Answers in [solutions/spot_the_bug_answers.md](solutions/spot_the_bug_answers.md).
Read them only after your team has committed to an answer for all eight.

---

## 1

```python
point = (1)
print(type(point), len(point))
```

## 2

```python
x = 0
y = 1
sum = 0

while sum < 50:
    print(sum, end=" ")
    x = y
    y = sum
    sum = x + y

print()
print(sum([1, 2, 3]))
```

The author wanted the Fibonacci numbers from 1 to 50, and then a total.

## 3

```python
names = ["Jean", 3, "Paul", 1]
names.sort()
print(names)
```

## 4

```python
dict = {}
dict["Capital"] = "London"
dict["Food"] = "Fish&Chips"

dictList = []
for key, value in dict.items():
    temp = [key, value]
    dictlist.append(temp)

print(dictList)
```

There is more than one problem here. Find all three.

## 5

```python
def bubble_sort(values):
    for i in range(len(values)):
        for j in range(len(values) - 1):
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
    return values

our_list = [9, 4, 6, 1]
old_list = our_list
new_list = bubble_sort(old_list)

print("original:", our_list)
print("sorted:  ", new_list)
```

The author wanted to keep the original list for comparison.

## 6

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags

print(add_tag("python"))
print(add_tag("git"))
```

## 7

```python
raw = "  Data Roots  \n"
raw.strip()
raw.lower()
print(f"[{raw}]")
```

## 8

```python
scores = {"ada": 90, "alan": 72}

for name in scores:
    if scores[name] < 80:
        del scores[name]

print(scores)
```

---

## Bonus round: no crash, still wrong

These run and print something. That is what makes them dangerous.

```python
# a
prices = [19.99, 5.00, 3.01]
if sum(prices) == 28.00:
    print("exact change")
else:
    print("no exact change")

# b
config = {"retries": 0}
if config.get("retries"):
    print(f"retrying {config['retries']} times")
else:
    print("retries not configured")

# c
def average(numbers):
    return sum(numbers) / len(numbers)

print(average([]))
```
